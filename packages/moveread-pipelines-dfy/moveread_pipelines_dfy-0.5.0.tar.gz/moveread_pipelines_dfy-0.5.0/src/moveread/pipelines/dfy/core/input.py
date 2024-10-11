from typing import Callable
from uuid import uuid4
from haskellian import either as E
from kv import KV
from pipeteer import WriteQueue
from dslog import Logger
from chess_pairings import gameId
import robust_extraction2 as re
from moveread.core import Core, Game
from ..spec import Input, GameId

def makeId(game: Game) -> GameId:
  if game.meta is None or game.meta.tournament is None:
    return gameId('tournament', 'a', '1', '1')
  return game.meta.tournament

def make_title(game: Game) -> str:
  gid = makeId(game)
  return f'{gid["tournId"]}: {gid["group"]}/{gid["round"]}/{gid["board"]}'

async def input_all(
  core: Core, Qin: WriteQueue[Input],
  *, images: KV[bytes],
  model_fn: Callable[[Game], tuple[str, re.ExtendedModel]],
  gameId_fn: Callable[[Game], GameId] = makeId,
  title_fn: Callable[[Game], str] = make_title,
  endpoint_fn: Callable[[Game], str | None] = lambda *_: None,
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
    imgs = []
    for imgId, image in game.images:
      id = '-'.join(map(str, imgId))
      url = f'{id}/original_{uuid4()}.jpg'
      img = (await core.blobs.read(image.url)).unsafe()
      (await images.insert(url, img)).unsafe()
      imgs.append(url)
      break

    name, model = model_fn(game)
    task = Input(
      title=title_fn(game), model=model, model_name=name,
      gameId=gameId_fn(game), imgs=imgs, serving_endpoint=endpoint_fn(game)
    )
    (await Qin.push(gameId, task)).unsafe()
    logger(f'Inputted task "{gameId}". Task:', task)