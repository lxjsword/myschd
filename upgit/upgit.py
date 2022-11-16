#!/usr/bin/env python
# coding:utf-8

# **********************************************************
# * Author        : ryanxjli
# * Email         : ryanxjli@tencent.com
# * Create time   : 2022-07-27 16:53
# * Last modified : 2022-07-27 16:53
# * Filename      : upgit.py
# * Description   :
# **********************************************************
import sys
import logging
import git
import traceback

repo_url = [
    '/home/ryanxjli/QQMail/mmsearch',
    '/home/ryanxjli/data/mmsearch_git/mmsearchoss',
    '/home/ryanxjli/data/mmsearch_git/mmsearchossnew',
]

logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
                    level=logging.INFO)


def upgit():
    global repo_url
    try:
        for url in repo_url:
            logging.info('check {}'.format(url))
            repo = git.Repo(url)
            logging.info('active_branch name: {}'.format(repo.active_branch.name))
            if not repo.is_dirty():
                logging.info('not dirty, ready to pull')
                remote = repo.remote()
                # res = remote.pull(refspec='{}:{}'.format(repo.active_branch.name, repo.active_branch.name))
                res = remote.pull(refspec='{}'.format(repo.active_branch.name, ))
                info = res[0]
                logging.info('pull note: {}'.format(info.note))
    except:
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    upgit()
