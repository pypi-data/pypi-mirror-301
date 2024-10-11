from typing_extensions import Literal, TypedDict, NotRequired
from dataclasses import dataclass, field
from uuid import uuid4
from haskellian import either as E
from kv import KV
from pipeteer import GetQueue, ReadQueue, WriteQueue, Task
import robust_extraction2 as re
import pure_cv as vc
from pure_cv import Rotation
from dslog import Logger
from ..util import insert_rescaled

@dataclass(kw_only=True)
class Input:
  img: str
  descaled_img: str = field(default='', kw_only=True)
  size: tuple[int, int] | None = None

@dataclass
class Corrected:
  corners: vc.Corners
  corrected: str
  tag: Literal['corrected'] = 'corrected'

@dataclass
class Rotated:
  rotation: Rotation
  rotated: str
  tag: Literal['rotated'] = 'rotated'

Output = Corrected | Rotated

@dataclass
class CorrectAPI:

  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  images: KV[bytes]
  logger: Logger
  
  def items(self):
    return self.Qin.items()
  
  @E.do()
  async def correct(self, id: str, rel_corners: vc.Corners):
    inp = (await self.Qin.read(id)).unsafe()
    mat = vc.decode((await self.images.read(inp.img)).unsafe())
    w, h = inp.size # type: ignore
    corners = vc.corners.pad(rel_corners * [w, h], padx=0.04, pady=0.04)
    corr_mat = vc.corners.correct(mat, corners)
    corr_img = vc.encode(corr_mat, '.jpg')
    corr = f'{id}/manually-corrected_{uuid4()}.jpg'
    (await self.images.insert(corr, corr_img)).unsafe()
    self.logger(f'Corrected "{inp.img}" to "{corr}"', level='DEBUG')
    next = Corrected(corrected=corr, corners=corners)
    (await self.Qout.push(id, next)).unsafe()
    (await self.Qin.pop(id)).unsafe()
  
  @E.do()
  async def rotate(self, id: str, rotation: Rotation):
    inp = (await self.Qin.read(id)).unsafe()
    mat = vc.decode((await self.images.read(inp.img)).unsafe())
    rot_img = vc.encode(vc.rotate(mat, rotation), '.jpg')
    rot = f'{id}/rotated_{uuid4()}.jpg'
    (await self.images.insert(rot, rot_img)).unsafe()
    self.logger(f'Rotated "{inp.img}" to "{rot}"', level='DEBUG')
    (await self.Qout.push(id, Rotated(rotation=rotation, rotated=rot))).unsafe()
    (await self.Qin.pop(id)).unsafe()

class Params(TypedDict):
  images: KV[bytes]
  descaled_h: int
  logger: Logger

class Correct(Task[Input, Output, Params, CorrectAPI]):

  Input = Input
  Output = Output
  Queues = Task.Queues[Input, Output]
  Params = Params
  Artifacts = CorrectAPI

  def __init__(self):
    super().__init__(Input, Output) # type: ignore

  def push_queue(self, get_queue: GetQueue, params: Params, *, prefix = ()) -> WriteQueue[Input]:
    @E.do()
    async def premap(inp: Input) -> Input:
      rescaled_url, (w, h) = (await insert_rescaled(inp.img, images=params['images'], descaled_h=params['descaled_h'])).unsafe()
      return Input(img=inp.img, descaled_img=rescaled_url, size=(w, h))
    return super().push_queue(get_queue, params, prefix=prefix).safe_apremap(premap)
  
  def run(self, queues: Task.Queues[Input, Corrected | Rotated], params: Params):
    return CorrectAPI(**queues, images=params['images'], logger=params['logger']) # type: ignore