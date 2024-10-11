from typing_extensions import TypedDict, Any, Coroutine, NotRequired
from dataclasses import dataclass
from pipeteer import Wrapped, Workflow, Task
from fastapi import FastAPI
from dslog import Logger
from kv import LocatableKV
import robust_extraction2 as re
from ._types import BaseInput, BaseCorrected, BaseExtracted, Uncorrected, Corrected, Extracted, Selected, Output
from .pipelines import correct as corr, extract as extr, select as sel, validate as val, preoutput
from ._api import api

@dataclass
class Extract:
  input: Uncorrected | Corrected
  def pre(self) -> extr.Input:
    already_corrected = isinstance(self.input, Corrected)
    img = self.input.corrected if isinstance(self.input, Corrected) else self.input.img
    return extr.Input(model=self.input.model, img=img, already_corrected=already_corrected)

  def post(self, out: extr.Output) -> 'State':
    inp = self.input
    already_corrected = isinstance(inp, Corrected)
    if out.tag == 'left':
      if already_corrected:
        return Select(model=inp.model, img=inp.img, corrected=inp.corrected, corners=inp.corners)
      else:
        return Correct(model=inp.model, img=inp.img, reextract=True)
    else:
      o = out.value
      corners = o.corners if not already_corrected else inp.corners
      assert corners is not None, f'Expected corners to be non-None, after input {inp}'
      return Validate(model=inp.model, img=inp.img, corrected=o.corrected, contours=o.contours, contoured=o.contoured, already_corrected=already_corrected, corners=corners)
    
  @staticmethod
  def new(img: str, model: re.ExtendedModel):
    return Extract(input=Uncorrected(model=model, img=img))


@dataclass
class Correct(BaseInput):
  reextract: bool

  def pre(self) -> corr.Input:
    return corr.Input(img=self.img)
  def post(self, out: corr.Output) -> 'State':
    if out.tag == 'corrected':
      if self.reextract:
        c = Corrected(model=self.model, img=self.img, corrected=out.corrected, corners=out.corners)
        return Extract(input=c)
      else:
        return Select(model=self.model, img=self.img, corrected=out.corrected, corners=out.corners)
    else:
      return Extract.new(img=out.rotated, model=self.model)

@dataclass
class Validate(BaseExtracted):
  already_corrected: bool = False

  def pre(self) -> val.Input:
    return val.Input(contoured=self.contoured)
  def post(self, out: val.Annotation) -> 'State':
    if out == 'correct':
      extr = Extracted(model=self.model, img=self.img, corrected=self.corrected, contours=self.contours, contoured=self.contoured, corners=self.corners)
      return Preoutput(result=extr)
    elif out == 'perspective-correct':
      return Select(model=self.model, img=self.img, corrected=self.corrected, corners=self.corners)
    elif out == 'incorrect':
      if self.already_corrected:
        return Select(model=self.model, img=self.img, corrected=self.corrected, corners=self.corners)
      else:
        return Correct(model=self.model, img=self.img, reextract=not self.already_corrected)

class Select(BaseCorrected):
  def pre(self) -> sel.Input:
    return sel.Input(model=self.model, img=self.corrected)
  def post(self, out: sel.Output) -> 'State':
    if out.tag == 'selected':
      sel = Selected(model=self.model, img=self.img, corrected=self.corrected, contours=out.contours, corners=self.corners)
      return Preoutput(result=sel)
    elif out.tag == 'recorrect':
      return Correct(model=self.model, img=self.img, reextract=False)

@dataclass
class Preoutput:
  result: Selected | Extracted
  def pre(self) -> preoutput.Input:
    return preoutput.Input(result=self.result)
  def post(self, out: Output) -> 'State':
    return out

State = Extract | Correct | Validate | Select | Preoutput | Output
Input = Extract

class Queues(TypedDict):
  extract: Wrapped.Queues
  correct: Wrapped.Queues
  validate: Wrapped.Queues
  select: Wrapped.Queues
  preoutput: Wrapped.Queues

class Pipelines(TypedDict): 
  extract: Wrapped[Extract, Any, extr.Input, Any, Task.Queues, extr.Params, Coroutine]
  correct: Wrapped[Correct, Any, corr.Input, Any, Task.Queues, corr.Params, corr.CorrectAPI]
  validate: Wrapped[Validate, Any, val.Input, Any, Task.Queues, Any, val.ValidateAPI]
  select: Wrapped[Select, Any, sel.Input, Any, Task.Queues, Any, sel.SelectAPI]
  preoutput: Wrapped[Preoutput, Any, preoutput.Input, Any, Task.Queues, preoutput.Params, Coroutine]

@dataclass
class Artifacts:
  api: FastAPI
  processes: dict[str, Coroutine]

class Params(TypedDict):
  logger: Logger
  images: LocatableKV[bytes]
  descaled_h: int
  model_path: str

class Preprocess(Workflow[Input, Any, Queues, Params, Artifacts, Pipelines]): # type: ignore
  Params = Params
  Artifacts = Artifacts
  Queues = Queues
  Input = Input
  Output = Output

  def __init__(self):
    super().__init__({
      'extract': Wrapped.of(Extract, extr.Extract(), Extract.pre, Extract.post),
      'correct': Wrapped.of(Correct, corr.Correct(), Correct.pre, Correct.post),
      'validate': Wrapped.of(Validate, val.Validate(), Validate.pre, Validate.post),
      'select': Wrapped.of(Select, sel.Select(), Select.pre, Select.post),
      'preoutput': Wrapped.of(Preoutput, preoutput.Preoutput(), Preoutput.pre, Preoutput.post),
    })

  def run(self, queues: Queues, params: Params) -> Artifacts:
    logger, images, descaled_h = params['logger'], params['images'], params['descaled_h']
    app = api(
      corr_api=self.pipelines['correct'].run(queues['correct'], corr.Params(images=images, logger=logger.prefix('[CORRECT]'), descaled_h=descaled_h)),
      val_api=self.pipelines['validate'].run(queues['validate'], None),
      sel_api=self.pipelines['select'].run(queues['select'], sel.Params(images=images, descaled_h=descaled_h)),
      images=images, logger=logger.prefix('[API]')
    )
    procs = {
      'extract': self.pipelines['extract'].run(queues['extract'], extr.Params(images=images, logger=logger.prefix('[EXTRACT]'), descaled_h=descaled_h, model_path=params['model_path'])),
      'preoutput': self.pipelines['preoutput'].run(queues['preoutput'], preoutput.Params(images=images, logger=logger.prefix('[PREOUTPUT]'))),
    }
    return Artifacts(api=app, processes=procs)
  