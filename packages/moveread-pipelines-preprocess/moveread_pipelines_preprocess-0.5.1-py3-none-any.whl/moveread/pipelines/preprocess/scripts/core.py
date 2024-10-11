from typing import Callable
from uuid import uuid4
from haskellian import either as E
from kv import KV
from dslog import Logger
from pipeteer import WriteQueue
import robust_extraction2 as re
from moveread.core import Core, Game
from moveread.pipelines.preprocess import Input

async def input_core(
  core: Core, Qin: WriteQueue[Input],
  *, images: KV[bytes],
  model_fn: Callable[[Game], 're.ExtendedModel'],
  num_games: int | None = None, shuffle: bool = True,
  logger = Logger.rich().prefix('[CORE INPUT]')
):
  """Input all images from `core` into `Qin` tasks
  - Actually, only images with `version == 0`
  - `model_fn`: determines the scoresheet model of each task
  - `state_fn`: determines an arbitrary tuple of JSON-serializable data to attach to each task
  """
  games = await core.games.keys().map(E.unsafe).sync()
  if shuffle:
    import random
    random.shuffle(games)
  for gameId in games[:num_games]:
    game = (await core.games.read(gameId)).unsafe()
    for imgId, image in game.images:
      id = '-'.join([gameId, *map(str, imgId)])
      url = f'{id}/original_{uuid4()}.jpg'
      img = (await core.blobs.read(image.url)).unsafe()
      (await images.insert(url, img)).unsafe()
      task = Input.new(model=model_fn(game), img=url)
      await Qin.push(id, task)
      logger(f'Inputted task "{id}". Task:', task)
      break