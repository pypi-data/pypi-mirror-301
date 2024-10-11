from typing_extensions import Coroutine, TypedDict
from dataclasses import dataclass
import asyncio
import os
from haskellian import either as E
from kv import KV
from pipeteer import ReadQueue, WriteQueue, Task
from dslog import Logger
import pure_cv as vc
from moveread.core import Image
from .._types import Selected, Extracted, Output

@dataclass
class Input:
  result: Selected | Extracted

@dataclass
class Runner:
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  images: KV[bytes]
  logger: Logger
    
  @E.do()
  async def extract_boxes(self, contours: vc.Contours, img: bytes) -> list[bytes]:
    mat = vc.decode(img)
    h, w = mat.shape[:2]
    boxes = vc.extract_contours(mat, contours * [w, h])
    out = []
    for box in boxes:
      try:
        out.append(vc.encode(box, '.jpg'))
      except:
        ...
    return out

  
  @E.do()
  async def store_boxes(self, output: Selected | Extracted) -> Output:
    """Extracts boxes and stores results into `Image.Meta`s"""
    img = (await self.images.read(output.img)).unsafe()
    cnts = vc.corners.unwarp_contours(output.contours, output.corners)
    image = Image(url=output.img, meta=Image.Meta(
      boxes=Image.BoxContours(contours=cnts, relative=True),
      source='robust-extraction' if output.tag == 'extracted' else 'manual',
      perspective_corners=output.corners
    ))
    boxes = (await self.extract_boxes(cnts, img)).unsafe()
    urls = [f'{os.path.splitext(image.url)[0]}/boxes/{ply}.jpg' for ply, _ in enumerate(boxes)]
    insertions = await asyncio.gather(*[self.images.insert(url, box) for url, box in zip(urls, boxes)])
    E.sequence(insertions).unsafe()
    self.logger(f'Inserted {len(boxes)} boxes: {", ".join(urls[:2])}, ...', level='DEBUG')
    return Output(image=image, boxes=urls)

  @E.do()
  async def delete_blobs(self, id: str, output: Extracted | Selected):
    keys = await self.images.keys().map(E.unsafe).sync()
    def delete(blob: str) -> bool:
      return blob.startswith(id) and blob != output.img and blob != output.corrected and not 'boxes' in blob
    delete_blobs = list(filter(delete, keys))
    deletions = await asyncio.gather(*[self.images.delete(blob) for blob in delete_blobs])
    E.sequence(deletions).unsafe()
    self.logger(f'Deleted {len(delete_blobs)} images: {delete_blobs}', level='DEBUG')
    

  @E.do()
  async def run_one(self):
    id, inp = (await self.Qin.read()).unsafe()
    self.logger(f'Processing "{id}"', level='DEBUG')
    next = (await self.store_boxes(inp.result)).unsafe()
    (await self.delete_blobs(id, inp.result)).unsafe()
    (await self.Qout.push(id, next)).unsafe()
    (await self.Qin.pop(id)).unsafe()
    self.logger(f'Outputted "{id}')

  async def __call__(self):
    while True:
      try:
        r = await self.run_one()
        if r.tag == 'left':
          self.logger(r.value, level='ERROR')
          await asyncio.sleep(1)
      except Exception as e:
        self.logger('Unexpected exception:', e, level='ERROR')
        await asyncio.sleep(1)

class Params(TypedDict):
  logger: Logger
  images: KV[bytes]

class Preoutput(Task[Input, Output, Params, Coroutine]):
  Queues = Task.Queues[Input, Output]
  Params = Params
  Artifacts = Coroutine

  def __init__(self):
    super().__init__(Input, Output)

  def run(self, queues: Task.Queues[Input, Output], params: Params):
    return Runner(**queues, **params)()
