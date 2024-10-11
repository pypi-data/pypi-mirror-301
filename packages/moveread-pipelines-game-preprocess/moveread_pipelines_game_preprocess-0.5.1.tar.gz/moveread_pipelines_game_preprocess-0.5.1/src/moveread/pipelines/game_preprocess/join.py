from typing_extensions import TypedDict, Coroutine
import asyncio
from kv import KV
from haskellian import either as E
from pipeteer import Task
from dslog import Logger
import moveread.pipelines.preprocess as pre
from ._types import Game, Output

class Params(TypedDict):
  buffer: KV[dict[str, pre.Output]]
  games: KV[Game]
  imgGameIds: KV[str]
  logger: Logger

class Join(Task[pre.Output, Output, Params, Coroutine]):
  Queues = Task.Queues[pre.Output, Output]
  Params = Params
  Artifacts = Coroutine

  def __init__(self):
    super().__init__(pre.Output, Output)

  async def run(self, queues: Queues, params: Params):
    Qin, Qout = queues['Qin'], queues['Qout']
    buffer, games, imgGameIds, logger = params['buffer'], params['games'], params['imgGameIds'], params['logger']
      
    @E.do()
    async def run_one():
      imgId, result = (await Qin.read()).unsafe()
      logger(f'Processing "{imgId}"', level='DEBUG')
      gameId = (await imgGameIds.read(imgId)).mapl(lambda err: f'Error reading image "{imgId}" gameId: {err}').unsafe()
      logger(f'Received "{imgId}" for "{gameId}"', level='DEBUG')
      game, received = await asyncio.gather(
        games.read(gameId).then(lambda e: e.mapl(lambda err: f'Error reading buffered game: {err}').unsafe()),
        buffer.read(gameId).then(E.get_or({})),
      )

      received_now = dict(received) | { imgId: result }
      receivedIds = set(imgId for imgId, _ in received_now.items())
      requiredIds = set(game.imgIds)
      logger('Received:', receivedIds, 'Required', requiredIds, level='DEBUG')

      if receivedIds == requiredIds:
        next = [received_now[id] for id in game.imgIds]
        (await Qout.push(gameId, next)).unsafe()
        _, e = await asyncio.gather(
          games.delete(gameId).then(E.unsafe),
          buffer.delete(gameId),
        )
        if e.tag == 'left' and e.value.reason != 'inexistent-item':
          e.unsafe()
        logger(f'Joined results for {gameId}')
      else:
        (await buffer.insert(gameId, received_now)).unsafe()
      
      (await imgGameIds.delete(imgId)).unsafe()
      (await Qin.pop(imgId)).unsafe()

    while True:
      try:
        r = await run_one()
        if r.tag == 'left':
          logger(r.value, level='ERROR')
          await asyncio.sleep(1)
      except Exception as e:
        logger('Unexpected exception:', e, level='ERROR')
        await asyncio.sleep(1)
        