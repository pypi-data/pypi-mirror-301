from typing_extensions import Any, Coroutine, TypedDict, NotRequired
from dataclasses import dataclass
import asyncio
from uuid import uuid4
from haskellian import funcs as F, either as E, Either, Left
from kv import KV
from pipeteer import ReadQueue, WriteQueue, Task
import pure_cv as vc
import numpy as np
import robust_extraction2 as re
from dslog import Logger
from moveread.tatr import TableDetector

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

def n_boxes(model: re.ExtendedModel) -> int:
  return model.rows * len(model.block_cols) * 2

@dataclass
class Runner:
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  logger: Logger
  images: KV[bytes]
  descaled_h: int
  model: TableDetector

  @E.do()
  async def extract(self, id: str, task: Input): 
    self.logger(f'Reading image "{task.img}"', level='DEBUG')
    img = (await self.images.read(task.img)).unsafe()
    self.logger(f'Read image "{task.img}"', level='DEBUG')
    mat = vc.decode(img)
    self.logger(f'Detecting...', level='DEBUG')
    cnts = self.model.detect(mat, max_cells=n_boxes(task.model), n_rows=task.model.rows)
    self.logger(f'Detected {len(cnts)} contours', level='DEBUG')
    
    descaled = vc.descale_max(mat, target_max=self.descaled_h)
    h, w = descaled.shape[:2]
    contoured = vc.draw.gradient_contours(descaled, cnts * [w, h])
    contoured = vc.encode(contoured, format='.jpg')
    cont = f'{id}/contoured_{uuid4()}.jpg'
    (await self.images.insert(cont, contoured)).unsafe()
    self.logger(f'Inserted contoured image at "{cont}"', level='DEBUG')

    corners = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    return Ok(contours=cnts, corrected=task.img, contoured=cont, corners=corners)

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
  model: TableDetector

class Extract(Task[Input, Output, Params, Coroutine]):
  Queues = Task.Queues[Input, Output]
  Params = Params
  Artifacts = Coroutine

  def __init__(self):
    super().__init__(Input, Output)

  def run(self, queues: Queues, params: Params):
    return Runner(**queues, **params)()