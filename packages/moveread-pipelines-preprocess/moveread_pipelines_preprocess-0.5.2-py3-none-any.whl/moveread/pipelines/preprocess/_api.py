from typing import Literal
from dataclasses import dataclass
import asyncio
from pydantic import BaseModel
from kv import LocatableKV
from haskellian import iter as I, either as E, Left, Right
from fastapi import FastAPI, Response, status, Request
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
import numpy as np
import pure_cv as vc
import scoresheet_models as sm
from .pipelines import correct as corr, select as sel, validate as val

@dataclass
class CorrectItem(corr.Input):
  id: str
  tag: Literal['correct'] = 'correct'

  @classmethod
  def of(cls, images: LocatableKV[bytes]):
    def inner(item: tuple[str, corr.Input]) -> CorrectItem:
      id, task = item
      return CorrectItem(img=images.url(task.descaled_img), id=id)
    return inner
  
@dataclass
class SelectItem:
  id: str
  img: str
  model: sm.Model
  tag: Literal['select'] = 'select'

  @classmethod
  def of(cls, images: LocatableKV[bytes]):
    def inner(item: tuple[str, sel.Input]) -> SelectItem:
      id, task = item
      return SelectItem(img=images.url(task.img), id=id, model=task.model)
    return inner

@dataclass
class ValidationItem(val.Input):
  id: str
  tag: Literal['validate'] = 'validate'

  @classmethod
  def of(cls, images: LocatableKV[bytes]):
    def inner(item: tuple[str, val.Input]) -> ValidationItem:
      id, task = item
      return ValidationItem(contoured=images.url(task.contoured), id=id)
    return inner

Item = CorrectItem | SelectItem | ValidationItem
AnnotateResponse = Literal['OK', 'NOT_FOUND', 'BAD_ANNOTATION', 'SERVER_ERROR']

def api(
  *, corr_api: corr.CorrectAPI, val_api: val.ValidateAPI,
  sel_api: sel.SelectAPI, images: LocatableKV[bytes],
  logger = Logger.rich().prefix('[MANUAL API]')
) -> FastAPI:
  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER)
    )
  )

  @app.get('/items')
  async def get_items(r: Request) -> list[Item]:
    tasks = (
      corr_api.items().map(lambda e: e | CorrectItem.of(images)).sync(),
      sel_api.items().map(lambda e: e | SelectItem.of(images)).sync(),
      val_api.items().map(lambda e: e | ValidationItem.of(images)).sync(),
    )
    all = I.flatten(await asyncio.gather(*tasks)).sync()
    errs = list(E.filter_lefts(all))
    if errs != []:
      logger('Errors reading tasks:', *errs, level='ERROR')
    return list(E.filter(all))
  
  class Corners(BaseModel):
    tl: tuple[float, float]
    tr: tuple[float, float]
    br: tuple[float, float]
    bl: tuple[float, float]

  class CorrectParams(BaseModel):
    corners: Corners
  
  @app.post('/correct')
  async def correct(id: str, params: CorrectParams, r: Response) -> bool:
    cs = params.corners
    x = await corr_api.correct(id, np.array([cs.tl, cs.tr, cs.br, cs.bl]))
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error correcting item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  class RotateParams(BaseModel):
    rotation: corr.Rotation
  
  @app.post('/rotate')
  async def rotate(id: str, params: RotateParams, r: Response) -> bool:
    x = await corr_api.rotate(id, params.rotation)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error rotating item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  class SelectParams(BaseModel):
    gridCoords: vc.Rect
  
  @app.post('/select')
  async def select(id: str, params: SelectParams, r: Response) -> bool:
    x = await sel_api.select(id, params.gridCoords)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error selecting item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  @app.post('/recorrect')
  async def recorrect(id: str, r: Response) -> bool:
    x = await sel_api.recorrect(id)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error recorrecting item {id}', x.value, level='ERROR')
      r.status_code = status.HTTP_400_BAD_REQUEST
    return ok
  
  @app.post('/annotate')
  async def annotate(id: str, annotation: val.Annotation, r: Response) -> AnnotateResponse:
    match await val_api.annotate(id, annotation):
      case Right():
        return 'OK'
      case Left(err):
        if err.reason == 'inexistent-item':
          r.status_code = status.HTTP_404_NOT_FOUND
          return 'NOT_FOUND'
        elif err.reason == 'bad-annotation':
          r.status_code = status.HTTP_400_BAD_REQUEST
          return 'BAD_ANNOTATION'
        else:
          logger(f'Error annotating item {id}', err, level='ERROR')
          r.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
          return 'SERVER_ERROR'
  
  return app