__version__ = '0.0.1'

import os
import sys

from jina.flow import Flow

num_docs = os.environ.get('MAX_DOCS', 500)
data_path = os.path.join('data','character-lines.csv')

def config():
    replicas = 2 if sys.argv[1] == 'index' else 1
    shards = 2 # South park example uses 2

    os.environ['REPLICAS'] = str(replicas)
    os.environ['SHARDS'] = str(shards)
    os.environ['WORKDIR'] = './workspace'
    os.makedirs(os.environ['WORKDIR'], exist_ok=True)
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(65481))

# for index
def index():
    f = Flow.load_config('flows/index.yml')

    with f:
        f.index_lines(filepath=data_path, batch_size=64, read_mode='r', size=num_docs)

    # for search
def search():
    f = Flow.load_config('flows/query.yml')

    with f:
        f.block()


# for test before put into docker
def dryrun():
    f = Flow.load_config('flows/query.yml')

    with f:
        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('choose between "index/search/dryrun" mode')
        exit(1)
    if sys.argv[1] == 'index':
        config()
        index()
    elif sys.argv[1] == 'search':
        config()
        search()
    elif sys.argv[1] == 'dryrun':
        config()
        dryrun()
    else:
        raise NotImplementedError(f'unsupported mode {sys.argv[1]}')
