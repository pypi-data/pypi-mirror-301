from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-q', '--queues', required=True)
  parser.add_argument('--images', required=True, help='Connection string to images')
  parser.add_argument('--url', required=True, help='The server URL')
  parser.add_argument('--height', default=768, type=int, help='Height of descaled images')
  parser.add_argument('-w', '--weights', help='Path to TATR weights file')

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()

  import os
  from dslog import Logger
  queues_path = os.path.join(os.getcwd(), args.queues)
  
  logger = Logger.click().prefix('[PREPROCESS]')
  logger(f'Running preprocessing...')
  logger(f'Images connection string: "{args.images}"')
  logger(f'Queues path: "{queues_path}"')
  
  import asyncio
  from multiprocessing import Process
  from kv import KV, ServerKV, LocatableKV
  import uvicorn
  from fastapi.middleware.cors import CORSMiddleware
  from pipeteer import QueueKV
  from moveread.tatr import TableDetector
  from moveread.pipelines.preprocess import Preprocess, Output

  def get_queue(path, type: type):
    return QueueKV.sqlite(type, queues_path, table='-'.join(['queue', *path]))
  
  images = locatable_imgs = KV[bytes].of(args.images)
  if not isinstance(locatable_imgs, LocatableKV):
    locatable_imgs = images.served(args.url.rstrip('/') + '/images')

  Qout = get_queue(('output',), Output)

  model = TableDetector()
  model.load(args.weights)

  wkf = Preprocess()
  params = Preprocess.Params(logger=logger, images=locatable_imgs, descaled_h=args.height, model=model)
  Qs = wkf.connect(Qout, get_queue, params)
  artifacts = wkf.run(Qs, params)
  artifacts.api.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
  artifacts.api.mount('/images', ServerKV(images))

  ps = {
    id: Process(target=asyncio.run, args=(f,)) for id, f in artifacts.processes.items()
  } | {
    'api': Process(target=uvicorn.run, args=(artifacts.api,), kwargs={'host': args.host, 'port': args.port})
  }
  for id, p in ps.items():
    p.start()
    logger(f'Process "{id}" started at PID {p.pid}')
  for p in ps.values():
    p.join()

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/pipelines/preprocess/dev/demo')
  sys.argv.extend('-q queues.sqlite --images file://images/ --url http://localhost:8000'.split(' '))
  main()