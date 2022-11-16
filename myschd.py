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
import asyncio
import time
import multiprocessing
import logging
from croniter import croniter

from call_util import call_func, add_days_ts

pool = multiprocessing.Pool(processes=2)

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


def call_wrap(call_params, ):
    pool.apply_async(call_func, (call_params, ))
    ci = croniter(call_params[3], datetime.now())
    next_time = datetime.timestamp(ci.get_next(datetime))
    loop = asyncio.get_event_loop()
    loop.call_later(next_time - time.time(), call_wrap, call_params, )


def sched():
    loop = asyncio.get_event_loop()
    # tomorrow = add_days_ts()
    logging.info(CALL_PARAMS)
    # logging.info('tomorrow: {}'.format(tomorrow))
    for item in CALL_PARAMS:
        ci = croniter(item[3], datetime.now())
        next_time = datetime.timestamp(ci.get_next(datetime))
        logging.info('{} call later: {}'.format(item[2], next_time - time.time()))
        loop.call_later(next_time - time.time(), call_wrap, item)

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    sched()
