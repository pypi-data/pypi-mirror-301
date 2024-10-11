from haskellian import either as E, promise as P
from kv import KV, ReadError
from moveread.pipelines.preprocess import Output as PreOutput
from moveread.core import Core, Game, Player, Sheet, StylesNA
from ..spec import Output

def output_sheet(out: PreOutput, model: str):
  return Sheet(images=[out.image], meta=Sheet.Meta(model=model))

def output_game(out: Output):
  ann = out.annotations
  styles = StylesNA(pawn_capture=ann.pawn_capture, piece_capture=ann.piece_capture)
  sheets = [output_sheet(img, out.model_name) for img in out.preprocessed_imgs]
  imgs = [out.image.url for out in out.preprocessed_imgs]

  game = Game(
    meta=Game.Meta(pgn=out.pgn, early=out.early, tournament=out.gameId),
    players=[Player(
      meta=Player.Meta(language=ann.lang, end_correct=ann.end_correct, styles=styles, edits=ann.edits),
      sheets=sheets
    )]
  )

  return game, imgs

@E.do[ReadError]()
async def output_one(core: Core, key: str, out: Output, *, blobs: KV[bytes]):
  game, imgs = output_game(out)
  tasks = [blobs.copy(url, core.blobs, url) for url in imgs]
  E.sequence(await P.all(tasks)).unsafe()
  (await core.games.insert(key, game)).unsafe()