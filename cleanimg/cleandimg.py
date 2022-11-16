#!/usr/bin/env python
# coding:utf-8

# **********************************************************
# * Author        : ryanxjli
# * Email         : ryanxjli@tencent.com
# * Create time   : 2022-07-27 09:28
# * Last modified : 2022-07-27 09:28
# * Filename      : cleandimg.py
# * Description   :
# **********************************************************
import sys
import subprocess
import re
import logging

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                    level=logging.INFO)


def cleandimg():
    out = subprocess.run('docker images', shell=True, capture_output=True)
    images = out.stdout.decode().split('\n')[1:]
    logging.info(images)

    clean_imgids = []
    for line in images:
        out_arr = line.split()
        if len(out_arr) < 5:
            continue
        imageid, num, unit = out_arr[2], int(out_arr[3]), out_arr[4]
        if re.search('mmsearchossdendenmushi', line):
            if unit == 'days' and num >= 7:
                logging.info(line)
                clean_imgids.append(imageid)
            elif unit == 'weeks':
                logging.info(line)
                clean_imgids.append(imageid)

        # if re.search('mmsearchossdendenmushi', line) and re.search('weeks ago', line):
            # logging.info(line)
            # imageid = line.split()[2]
            # clean_imgids.append(imageid)
    logging.info(clean_imgids)

    if len(clean_imgids) > 0:
        out = subprocess.run('docker rmi {}'.format(' '.join(clean_imgids)), shell=True, capture_output=True)
        logging.info(out.stdout)


if __name__ == '__main__':
    cleandimg()
