from typing_extensions import Any, Coroutine, TypedDict, NotRequired
from dataclasses import dataclass
import asyncio
from uuid import uuid4
from haskellian import funcs as F, either as E, Either, Left
from kv import KV
from pipeteer import ReadQueue, WriteQueue, Task
import pure_cv as vc
import robust_extraction2 as re
from dslog import Logger

@dataclass
class Input:
  model: re.ExtendedModel
  img: str
  already_corrected: bool

@dataclass
class Ok:
  corners: vc.Corners | None
  contours: vc.Contours
  corrected: str
  contoured: str

Output = Either[Any, Ok]

@dataclass
class Runner:
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  logger: Logger
  images: KV[bytes]
  descaled_h: int

  @E.do()
  async def extract(self, id: str, task: Input): 
    img = (await self.images.read(task.img)).unsafe()
    mat = vc.decode(img)
    res = re.extract(mat, task.model, autocorrect=not task.already_corrected).unsafe()
    corr_mat, cnts, corners = res['corr_img'], res['cnts'], res['corners']
    corrected = vc.encode(corr_mat, format='.jpg')
    contoured = F.pipe(
      vc.draw.contours(corr_mat, cnts, color=(0, 0, 255)), # type: ignore
      vc.descale_max(target_max=self.descaled_h),
      vc.encode(format='.jpg'),
    )
    corr = f'{id}/corrected_{uuid4()}.jpg'
    cont = f'{id}/contoured_{uuid4()}.jpg'
    await asyncio.gather(
      self.images.insert(corr, corrected).then(E.unsafe),
      self.images.insert(cont, contoured).then(E.unsafe),
    )
    self.logger(f'Inserted corrected image at "{corr}"', level='DEBUG')
    self.logger(f'Inserted contoured image at "{cont}"', level='DEBUG')
    return Ok(contours=cnts, corrected=corr, contoured=cont, corners=corners)

  @E.do()
  async def run_one(self):
    id, inp = (await self.Qin.read()).unsafe()
    self.logger(f'Extracting "{id}": "{inp.img}" ({inp.model})')
    try:
      res = await self.extract(id, inp)
    except Exception as e:
      res = Left(f'Unexpected exception: {e}')
    (await self.Qout.push(id, res)).unsafe()
    self.logger(f'Extracted "{id}": {"OK" if res.tag == "right" else f"ERR: {res.value}"}')
    (await self.Qin.pop(id)).unsafe()

  async def __call__(self):
    while True:
      try:
        e = await self.run_one()
        if e.tag == 'left':
          self.logger(e.value, level='ERROR')
          await asyncio.sleep(1)
        else:
          await asyncio.sleep(0)
      except Exception as e:
        self.logger('Unexpected exception:', e, level='ERROR')
        await asyncio.sleep(1)

class Params(TypedDict):
  images: KV[bytes]
  logger: Logger
  descaled_h: int

class Extract(Task[Input, Output, Params, Coroutine]):
  Queues = Task.Queues[Input, Output]
  Params = Params
  Artifacts = Coroutine

  def __init__(self):
    super().__init__(Input, Output)

  def run(self, queues: Queues, params: Params):
    return Runner(**queues, **params)()