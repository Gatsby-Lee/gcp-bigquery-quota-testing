"""
:author: Gatsby Lee
:since: 2019-12-23
"""

import argparse
import logging
import time
import threading

from google.cloud.bigquery import (
    Client,
    Dataset,
    LoadJobConfig,
    SchemaField,
    Table,
)

LOGGER = logging.getLogger(__name__)
TABLE_NAME = 'loadjob_daily_1000quota_standard'
TABLE_SCHEMA = [
    SchemaField('keyword', 'STRING', mode='REQUIRED'),
]


class FailedInsertingSerpCacheBigQueryException(Exception):
    pass


class ThreadWrapper(threading.Thread):

    def __init__(self, fn, arg_list):
        threading.Thread.__init__(self)
        self.fn = fn
        self._arg_list = arg_list

    def run(self):
        self.fn(*self._arg_list)


def create_table(client, dataset_ref):
    table_ref = dataset_ref.table(TABLE_NAME)
    table_obj = Table(table_ref, schema=TABLE_SCHEMA)
    return client.create_table(table_obj)


def drop_table(client, dataset_ref):
    table_ref = dataset_ref.table(TABLE_NAME)
    client.delete_table(table_ref)


def loadjob_one(client, dataset_ref):
    data = [{'keyword': 'dummy-{}'.format(str(time.time()))}]
    table_ref = dataset_ref.table(TABLE_NAME)
    table_obj = Table(table_ref, schema=TABLE_SCHEMA)
    job_config = LoadJobConfig()
    job_config.schema = TABLE_SCHEMA
    result_obj = client.load_table_from_json(data, table_obj, job_config=job_config)

    sleep_time = 1
    while result_obj.done() is False:
        LOGGER.info('waiting for %s second. data insertion.', sleep_time)
        time.sleep(sleep_time)

    if result_obj.errors:
        error_msg = 'Failed to insert: error_msg=%s' % result_obj.errors
        LOGGER.error(error_msg)
        raise FailedInsertingSerpCacheBigQueryException(error_msg)


def loadjob_infinite(client, dataset_ref, sleep_time=None):
    while True:
        loadjob_one(client, dataset_ref)
        if sleep_time is not None:
            time.sleep(sleep_time)


def loadjob_with_thread(project_name, dataset_name, num_thread, sleep_time=None):
    tlist = []
    for _ in range(num_thread):
        client = Client(project_name)
        dataset_ref = Dataset(client.dataset(dataset_name))
        tw = ThreadWrapper(loadjob_infinite, [client, dataset_ref, sleep_time])
        tw.start()
        tlist.append(tw)

    while len(tlist) > 0:
        tlist = [t for t in tlist if t.isAlive()]
        time.sleep(1)


def _parse_args():
    parser = argparse.ArgumentParser()

    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument('--dataset', required=True)
    base_parser.add_argument('--project', required=True)
    base_parser.add_argument('--num-thread', default=2, type=int)
    base_parser.add_argument('--sleep', type=int)

    cmd_parser = parser.add_subparsers(dest='cmd')
    cmd_parser.requird = True
    cmd_parser.add_parser('create-table', parents=[base_parser])
    cmd_parser.add_parser('drop-table', parents=[base_parser])
    cmd_parser.add_parser('loadjob-one', parents=[base_parser])
    cmd_parser.add_parser('loadjob-with-thread', parents=[base_parser])

    return parser.parse_args()


def _main():
    args = _parse_args()

    _client = Client(args.project)
    _dataset_ref = Dataset(_client.dataset(args.dataset))

    if args.cmd == 'create-table':
        create_table(_client, _dataset_ref)
    elif args.cmd == 'drop-table':
        drop_table(_client, _dataset_ref)
    elif args.cmd == 'loadjob-one':
        loadjob_one(_client, _dataset_ref)
    elif args.cmd == 'loadjob-with-thread':
        loadjob_with_thread(args.project, args.dataset, args.num_thread,
                            args.sleep)


if __name__ == '__main__':
    FORMAT = '%(asctime)s (%(filename)s, %(funcName)s, %(lineno)d) [%(levelname)8s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    _main()
