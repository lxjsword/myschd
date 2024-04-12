#!/usr/bin/env python
# coding:utf-8

# **********************************************************
# * Author        : ryanxjli
# * Email         : ryanxjli@tencent.com
# * Create time   : 2022-07-27 17:37
# * Last modified : 2022-07-27 17:37
# * Filename      : myschd.py
# * Description   :
# **********************************************************
from datetime import datetime
import sys
import os
import asyncio
import time
import multiprocessing
import logging
from croniter import croniter
import json
import heapq

from call_util import dynamic_call_func, get_content_md5

pool = None

'''
CALL_PARAMS = [
    # [module_name, file_path, func, offset, interval]
    ['cleandimg', '/home/ryanxjli/data/myschd/cleanimg/cleandimg.py', 'cleandimg', 5, 24 * 60 * 60],
    ['upgit', '/home/ryanxjli/data/myschd/upgit/upgit.py', 'upgit', 10, 24 * 60 * 60],
]
'''

CALL_PARAMS = [
    # [module_name, file_path, func, crontab]
    ['cleandimg', '/home/ryanxjli/data/myschd/cleanimg/cleandimg.py', 'cleandimg', '0 */8 * * *', ],
    ['upgit', '/home/ryanxjli/data/myschd/upgit/upgit.py', 'upgit', '10 */8 * * *', ],
]

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                    level=logging.INFO)

CFG_PATH = os.path.join(os.path.dirname(__file__), 'cfg.json')
MD5_CFG = None
HEAP = []
EMPTY_CHECK_INTERVAL = 5*60 


class CallItem(object):
    def __init__(self, item):
        self.module_name = item[0]
        self.file_path = item[1]
        self.func_name = item[2]
        self.crontab = item[3]
        self.call_at = item[4]
        self.call_name = None
        self.file_md5 = None

    def set_key(self, call_name):
        self.call_name = call_name

    def cal_md5(self):
        with open(self.file_path, 'r') as f:
            data = f.read()
        self.file_md5 = get_content_md5(data.encode('utf8'))

    @property
    def key(self):
        return self.call_name

    def __str__(self):
        return f'''CallItem
        call_name: {self.call_name}
        module_name: {self.module_name}
        file_path: {self.file_path}
        func_name: {self.func_name}
        crontab: {self.crontab}
        call_at: {self.call_at}
        '''

    def __eq__(self, other):
        return self.call_at == other.call_at

    def __lt__(self, other):
        return self.call_at < other.call_at

    
def read_cfg():
    global MD5_CFG
    with open(CFG_PATH, 'r') as f:
        data = f.read()
    md5_cfg = get_content_md5(data.encode('utf8'))
    if md5_cfg != MD5_CFG:
        MD5_CFG = md5_cfg
        json_cfg = json.loads(data)
        return True, json_cfg
    return False, None


def call_wrap():
    logging.info("enter call_wrap")
    global HEAP
    need_update, json_cfg = read_cfg()

    if need_update:
        logging.info("enter call_wrap")
        # 建新堆，替换旧堆
        tmp_heap = []
        for k, v in json_cfg.items():
            ci = croniter(v[3], datetime.now())
            next_time = datetime.timestamp(ci.get_next(datetime))
            v.append(next_time)
            item = CallItem(v)
            item.set_key(k)
            item.cal_md5()
            logging.info("reinit heap, push:{}".format(item))
            tmp_heap.append(item)
        HEAP = tmp_heap
        heapq.heapify(HEAP)

    # 同一时间可能有多个调用
    now = time.time()
    while len(HEAP) > 0 and HEAP[0].call_at <= now:
        more_call = heapq.heappop(HEAP)
        # 调用
        logging.info("call {}".format(more_call))
        with open(more_call.file_path, 'r') as f:
            data = f.read()
        file_md5 = get_content_md5(data.encode('utf8'))
        params = [more_call.module_name, more_call.file_path, more_call.func_name, file_md5 == more_call.file_md5, ]
        pool.apply_async(dynamic_call_func, (params, ))
        # 下次调用入堆
        ci = croniter(more_call.crontab, datetime.now())
        next_time = datetime.timestamp(ci.get_next(datetime))
        more_call.call_at = next_time
        logging.info("later recall: {}".format(more_call))
        logging.info("repush to heap")
        heapq.heappush(HEAP, more_call)
    
    # 最小堆取值，设置定时
    if len(HEAP) == 0:
        # 没有更多任务， 5min检查一次
        later_time = EMPTY_CHECK_INTERVAL
        logging.info("no more task, check later {}s".format(later_time))
    else:
        item = HEAP[0]
        logging.info("ready to call_later, pop heap item:{}".format(item))
        later_time = item.call_at - time.time()
        later_time = later_time if later_time > 0 else 0

    loop = asyncio.get_event_loop()
    loop.call_later(later_time, call_wrap, )


def sched():
    need_update, json_cfg = read_cfg()
    if not need_update:
        return
    # 所有调用入最小堆
    for k, v in json_cfg.items():
        ci = croniter(v[3], datetime.now())
        next_time = datetime.timestamp(ci.get_next(datetime))
        v.append(next_time)
        item = CallItem(v)
        item.set_key(k)
        item.cal_md5()
        logging.info("init heap, push:{}".format(item))
        heapq.heappush(HEAP, item)

    # 取最早调用，设置定时
    if len(HEAP) == 0:
        later_time = EMPTY_CHECK_INTERVAL
    else:
        item = HEAP[0]
        logging.info("ready to call_later, item:{}".format(item))
        later_time = item.call_at - time.time()
        later_time = later_time if later_time > 0 else 0

    loop = asyncio.get_event_loop()
    logging.info(later_time)
    loop.call_later(later_time, call_wrap, )
    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=2)
    sched()
