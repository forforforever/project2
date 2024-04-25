# -*- coding: utf-8 -*-
from json import loads, dumps
from io import TextIOWrapper
from sys import stdout
from requests import post
from WhosbugAssign.authutils import AuthUtil
# 【online】
HOST = 'https://sngapm.qq.com/whosbug'
A = AuthUtil()
stdout = TextIOWrapper(stdout.buffer, encoding='utf-8')


def get_latest_release(pid):
    """
    :return: latest release commit id
    """
    token = A.gen_token()
    url = HOST + '/releases/last/'
    headers = {
        "token": token,
    }

    data = {
        'pid': pid
    }
    get_latest_release_res = post(url, data=data, headers=headers)
    if get_latest_release_res.status_code == 200:
        return loads(get_latest_release_res.content.decode('UTF-8', 'ignore'))['commit_hash']
    else:
        print(get_latest_release_res.content)
        return None


def post_commit(res):
    """post result to database

    :param res: final diff-parse result

    """
    token = A.gen_token()
    url = HOST + '/commits/diffs/'
    res_json = dumps(res, sort_keys=True, indent=4, separators=(',', ': '))
    headers = {
        "token": token,
        'Content-Type': 'application/json'
    }
    post_res = post(url, data=res_json, headers=headers)
    if post_res.status_code == 201:
        print("insert database successful")
    else:
        print(post_res.text)


def post_params(pid, release, monkey_task_name):
    """post params to NewMonkey

    :param pid: 项目的唯一标识
    :param release: 项目产品发布的版本（已加密）
    :param monkey_task_name: NewMonkey任务名

    """
    url = 'https://monkey.qq.com/bugs/whosbug_params'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'pid': pid,
        'release': release,
        'task_name': monkey_task_name
    }
    post_res = post(url, data=dumps(data, sort_keys=True, indent=4, separators=(',', ': ')), headers=headers)
    if post_res.status_code == 200:
        print('post params successful')
    else:
        print(post_res.text)
