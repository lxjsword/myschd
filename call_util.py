#!/usr/bin/env python
# coding:utf-8

# **********************************************************
# * Author        : ryanxjli
# * Email         : ryanxjli@tencent.com
# * Create time   : 2022-08-04 15:14
# * Last modified : 2022-08-04 15:14
# * Filename      : call_util.py
# * Description   :
# **********************************************************
import sys
import os
import logging
import time
from datetime import datetime, date, timedelta
from importlib.util import spec_from_file_location, module_from_spec
import importlib
import hashlib


logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                    level=logging.INFO)


def add_days_ts(day=1):
    today = date.today()
    delta = timedelta(days=day)
    tomorrow = today + delta
    ts = time.mktime(tomorrow.timetuple())
    return ts


def get_content_md5(content):
    md5_tmp = hashlib.md5()
    md5_tmp.update(content)
    return md5_tmp.hexdigest()


def dynamic_call_func(call_params):
    if call_params[0] in sys.modules:
        logging.info("{} in {}'s sys.modules".format(call_params[0], os.getpid()))
        if not call_params[3]:
            sys.modules[call_params[0]] = importlib.reload(call_params[0])
        module = sys.modules[call_params[0]]
    else:
        logging.info("{} not in {}'s sys.modules".format(call_params[0], os.getpid()))
        spec = spec_from_file_location(call_params[0], call_params[1])
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[call_params[0]] = module

    func = getattr(module, call_params[2])
    logging.info('call {} at {}'.format(func.__name__, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    func()


def call_func(call_params):
    if call_params[0] in sys.modules:
        logging.info("{} in {}'s sys.modules".format(call_params[0], os.getpid()))
        module = sys.modules[call_params[0]]
    else:
        logging.info("{} not in {}'s sys.modules".format(call_params[0], os.getpid()))
        spec = spec_from_file_location(call_params[0], call_params[1])
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[call_params[0]] = module

    func = getattr(module, call_params[2])
    logging.info('call {} at {}'.format(func.__name__, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    func()
