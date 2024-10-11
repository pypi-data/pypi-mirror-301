from typing_extensions import Literal, TypedDict
from dataclasses import dataclass
from haskellian import either as E
from kv import KV
from pipeteer import GetQueue, ReadQueue, WriteQueue, Task
from pipeteer.queues import ReadError
import pure_cv as vc
import scoresheet_models as sm
from ..util import insert_rescaled

@dataclass(kw_only=True)
class Input:
  img: str
  model: sm.Model

@dataclass
class Selected:
  contours: vc.Contours
  tag: Literal['selected'] = 'selected'

@dataclass
class Recorrect:
  tag: Literal['recorrect'] = 'recorrect'

Output = Selected | Recorrect

@dataclass
class SelectAPI:

  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]

  def items(self):
    return self.Qin.items()
  
  @E.do[ReadError]()
  async def select(self, id: str, grid_coords: vc.Rect):
    inp = (await self.Qin.read(id)).unsafe()
    cnts = sm.contours(inp.model, **grid_coords)
    (await self.Qout.push(id, Selected(contours=cnts))).unsafe()
    (await self.Qin.pop(id)).unsafe()

  @E.do[ReadError]()
  async def recorrect(self, id: str):
    (await self.Qin.read(id)).unsafe()
    (await self.Qout.push(id, Recorrect())).unsafe()
    (await self.Qin.pop(id)).unsafe()

class Params(TypedDict):
  images: KV[bytes]
  descaled_h: int

class Select(Task[Input, Output, Params, SelectAPI]):
  
  Queues = Task.Queues[Input, Output]
  Artifacts = SelectAPI

  def __init__(self):
    super().__init__(Input, Output)

  def push_queue(self, get_queue: GetQueue, params: Params, *, prefix = ()) -> WriteQueue[Input]:
    @E.do()
    async def premap(inp: Input) -> Input:
      rescaled_url, _ = (await insert_rescaled(inp.img, images=params['images'], descaled_h=params['descaled_h'])).unsafe()
      return Input(img=rescaled_url, model=inp.model)
    return super().push_queue(get_queue, params, prefix=prefix).safe_apremap(premap)

  
  def run(self, queues: Task.Queues[Input, Output], params: Params) -> SelectAPI:
    return SelectAPI(**queues)