# -*- coding: utf-8 -*-
from json import dump
from os import getenv
from WhosbugAssign.crypto import encrypt
from WhosbugAssign.django_requests import post_commit, post_params

SECRET = getenv('WHOSBUG_SECRET', '')



def result(res_lists, pid, release_version):
    """将结果整理为输入数据库的json格式

    :param res_lists: 初始格式的结果
    :param pid: 项目的唯一标识
    :param release_version: 项目产品发布的版本

    :return res: 重构后的whosbug分析结果dict
    """
    print('pid: ', pid)
    print('release: ', release_version)
    latest_commit_hash = res_lists[0]['commit']
    print(latest_commit_hash)
    print(SECRET)
    project = {
        'pid': encrypt(pid, SECRET, pid)
    }
    release = {
        'release': release_version,#encrypt(pid, SECRET, release_version),
        'commit_hash': latest_commit_hash,#encrypt(pid, SECRET, latest_commit_hash)#最新一次的commit进行加密
    }
    print(release['commit_hash'])
    # objects列表里每一个元素都是一个变更函数的信息
    objects = []
    for commit in res_lists:#两次
        owner = '{}-{}'.format(commit['committer']['name'], commit['committer']['email'])
        print(len(commit['commit_diffs']))
        print(len(commit['commit_diffs'][0]['diff_content']))
        for diff_file in commit['commit_diffs']:#一次

            file_path = diff_file['diff_file'].split('/')[-1]
            #diff_file['diff_content'].keys() diff函数的start_line
            #函数的名字和hash以及parent_name的函数和hash

            for (line_number, values) in zip(diff_file['diff_content'].keys(), diff_file['diff_content'].values()):#两次
                objects.append({
                    'owner': owner,#encrypt(pid, SECRET, owner)
                    'file_path': file_path,#encrypt(pid, SECRET, file_path),
                    #encrypt(pid, SECRET, values['parent_name'])
                    'parent_name': values['parent_name'] if values['parent_name'] else values[
                        'parent_name'],
                    #encrypt(pid, SECRET, values['parent_hash'])
                    'parent_hash': values['parent_hash'] if values['parent_hash'] else values[
                        'parent_hash'],
                    'name': values['name'],#encrypt(pid, SECRET, values['name']),
                    'hash': values['hash'],#encrypt(pid, SECRET, values['hash']),
                    'old_name': "",
                    'commit_time': commit['commit_time'],
                })
    res = {
        'objects': objects,
        'release': release,
        'project': project
    }

    # 结果传入数据库
    post_commit(res)
    print('已传入数据库')
    with open("res.json", "w", encoding="UTF-8") as file:
        dump(res, file, sort_keys=True, indent=4, separators=(',', ': '))

    return res
