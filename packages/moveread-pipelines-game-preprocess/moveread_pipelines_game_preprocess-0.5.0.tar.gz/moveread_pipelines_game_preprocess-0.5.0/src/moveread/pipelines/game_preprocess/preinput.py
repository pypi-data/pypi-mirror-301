from typing_extensions import TypedDict, Coroutine
import asyncio
from kv import KV
from haskellian import either as E
from pipeteer import Task
from dslog import Logger
import moveread.pipelines.preprocess as pre
from ._types import Input, Game

class Params(TypedDict):
  games: KV[Game]
  imgGameIds: KV[str]
  logger: Logger

class Preinput(Task[Input, pre.Input, Params, Coroutine]):
  Queues = Task.Queues[Input, pre.Input]
  Params = Params
  Artifacts = Coroutine

  def __init__(self):
    super().__init__(Input, pre.Input)

  async def run(self, queues: Queues, params: Params):
    Qin, Qout = queues['Qin'], queues['Qout']
    games, imgGameIds, logger = params['games'], params['imgGameIds'], params['logger']
      
    @E.do()
    async def input_one():
      gameId, task = (await Qin.read()).unsafe()
      logger(f'Processing "{gameId}"', level='DEBUG')
      imgIds = [f'{gameId}/{i}' for i in range(len(task.imgs))]
      (await games.insert(gameId, Game(model=task.model, imgIds=imgIds))).unsafe()
      E.sequence(await asyncio.gather(*[
        imgGameIds.insert(imgId, gameId)
        for imgId in imgIds
      ])).unsafe()
      E.sequence(await asyncio.gather(*[
        Qout.push(imgId, pre.Input.new(model=task.model, img=img))
        for imgId, img in zip(imgIds, task.imgs)
      ])).unsafe()
      (await Qin.pop(gameId)).unsafe()
      logger(f'Pushed tasks from "{gameId}"', level='DEBUG')

    while True:
      try:
        r = await input_one()
        if r.tag == 'left':
          logger(r.value, level='ERROR')
          await asyncio.sleep(1)
      except Exception as e:
        logger('Unexpected exception:', e, level='ERROR')
        await asyncio.sleep(1)
