#!/usr/bin/env python
# coding:utf-8

# **********************************************************
# * Author        : ryanxjli
# * Email         : ryanxjli@tencent.com
# * Create time   : 2022-12-05 10:34
# * Last modified : 2022-12-05 10:34
# * Filename      : health_tip.py
# * Description   :
# **********************************************************
import datetime
import random
import requests
import sys
import subprocess


MORNING_TIPS = [
    '工作1小时啦，起来接杯茶，喝口水吧！',
    '记得起来走走，活动下筋骨哟！',
    '站起来望望窗外，眼睛休息下吧！',
    '站起来活动下，马上就吃午饭啦！',
]

AFTERNOON_TIPS = [
    '起来上个洗手间，走动走动吧！',
    '下午的工作繁重，也要注意间隔休息哦!',
    '站起来望望窗外，眼睛休息下吧！',
    '站起来活动下，然后继续加油！',
]

EVENING_TIPS = [
    '晚上有没有吃多， 起来活动下吧！',
    '下午的工作繁重，也要注意间隔休息哦!',
    '起来喝杯牛奶， 晚上好休息！',
    '提高工作效率， 晚上早点下班哟！',
]


def send_tips():

    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d, %H:%M:%S')
    now_hour = now.hour
    choice_tip = None
    if now_hour <= 12:
        # 上午
        choice_tip = random.choice(MORNING_TIPS)
    elif now_hour <= 18:
        # 下午
        choice_tip = random.choice(AFTERNOON_TIPS)
    else:
        # 晚上
        choice_tip = random.choice(EVENING_TIPS)

    tip_msg = f'现在是{now_str}, {choice_tip}'

    if sys.platform == 'darwin':
        # osascript -e 'display notification "内容" with title "标题"
        cmd = 'display notification "{}" with title "健康提醒⏰" '.format(tip_msg)
        subprocess.call(['osascript', '-e', cmd])
    else:
        print(tip_msg)


if __name__ == '__main__':
    send_tips()
