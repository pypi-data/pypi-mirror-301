from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-d', '--db-path', required=True)
  parser.add_argument('--images', required=True)
  parser.add_argument('--url', required=True, help='The server URL')

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()


  import os
  from dslog import Logger
  db_path = os.path.join(os.getcwd(), args.db_path)
  
  logger = Logger.click().prefix('[GAME PREPROCESS]')
  logger(f'Running preprocessing...')
  logger(f'Images conn str: "{args.images}"')
  logger(f'DB path: "{db_path}"')
  
  import asyncio
  from multiprocessing import Process
  from kv import KV, SQLiteKV, LocatableKV, ServerKV
  from pipeteer import QueueKV
  import uvicorn
  from fastapi.middleware.cors import CORSMiddleware
  import moveread.pipelines.preprocess as pre
  from moveread.pipelines.game_preprocess import GamePreprocess, Output, Game

  images = KV[bytes].of(args.images)
  if not isinstance(images, LocatableKV):
    if not args.url:
      raise ValueError('Provide a LocatableKV (--images) or a base URL (--url)')
    images = images.served(args.url.rstrip('/') + '/images')

  def get_queue(path, type: type):
    return QueueKV.sqlite(type, db_path, table='-'.join(['queues', *path]))
  
  Qout = get_queue(('output',), Output)
  wkf = GamePreprocess()

  params = GamePreprocess.Params(
    logger=logger, images=images,
    buffer=SQLiteKV.at(db_path, dict[str, pre.Output], table='buffer'),
    games=SQLiteKV.at(db_path, Game, table='games'),
    imgGameIds=SQLiteKV.at(db_path, str, table='game-ids'),
    descaled_h=512
  )

  Qs = wkf.connect(Qout, get_queue, params)
  artifs = wkf.run(Qs, params)
  artifs.api.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
  artifs.api.mount('/images', ServerKV(images))

  ps = {
    id: Process(target=asyncio.run, args=(f,)) for id, f in artifs.processes.items()
  } | {
    'api': Process(target=uvicorn.run, args=(artifs.api,), kwargs={'host': args.host, 'port': args.port})
  }
  for id, p in ps.items():
    p.start()
    logger(f'Process "{id}" started at PID {p.pid}')
  for p in ps.values():
    p.join()
  

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/3.game-preprocess/')
  sys.argv.extend('-q demo/queues.sqlite --images demo/images/'.split(' '))
  main()