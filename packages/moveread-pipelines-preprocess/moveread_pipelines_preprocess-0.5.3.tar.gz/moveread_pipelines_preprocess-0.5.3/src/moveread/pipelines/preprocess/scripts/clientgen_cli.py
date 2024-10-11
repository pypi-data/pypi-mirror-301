from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-o', '--output', help="Path to the typescript package's base folder", required=True)
  args = parser.parse_args()

  import sys
  from openapi_ts import generate_client
  from moveread.pipelines.preprocess._api import api

  app = api(corr_api={}, val_api={}, sel_api={}, images={}) # type: ignore
  spec = app.openapi()
  generate_client(spec, args.output, logstream=sys.stderr, args={
    '--client': '@hey-api/client-fetch',
    '--services': '{ asClass: false }',
    '--schemas': 'false'
  })

if __name__ == '__main__':
  main()