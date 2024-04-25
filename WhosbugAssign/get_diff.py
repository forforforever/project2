# -*- coding: utf-8 -*-
from os import getcwd, chdir, popen, getenv
from WhosbugAssign.django_requests import get_latest_release
from WhosbugAssign.crypto import encrypt, decrypt
import time

SECRET = getenv('WHOSBUG_SECRET', '')

#将从上次运行到这次运行的所有commit_diff读出来
def get_diff(repo_path, branch_name, pid):
    """得到两个版本之间的diff内容

    :return: 两个版本之间所有信息，包括每次的commit，diff信息，之后将此数据传入分析
    release_diff = {
        'commit_info': commit_info,
        'diff': diff,
        'branch_name': argv[2],
        'head_commit_id': new_release_commit_hash,
    }
    """
    # 进入初始化后的本地仓库路径
    origin_path = getcwd()
    chdir(repo_path)
    print('change work path: ', getcwd())

    log_head = popen('git rev-parse HEAD')#最新一次提交的commit hash
    new_release_commit_hash = log_head.buffer.read().decode('UTF-8', 'ignore').rstrip("\n")
    log_head.close()
    origin_hash = get_latest_release(encrypt(pid, SECRET, pid))
    last_release_commit_hash = decrypt(pid, SECRET, origin_hash) if origin_hash else None
    last_release_commit_hash=None
    #'e118abdeca362fad65ed9b1c909548bc4a0f7427'
    new_release_commit_hash = '1a9937c7cb981a46a9251a0e21669c73ac1aa3c0'#101d08ae2492110e06b9c33586488e9e0c20e0ed'
    last_release_commit_hash =  'b2f6827c365da978991c8c1639ed74953d3f8b96'#76fbe7c9e9504b1225576a8f373d8e19700e2282'
    print('last release\'s commit hash: ', last_release_commit_hash)
    print('new release\'s commit hash: ', new_release_commit_hash)

    if last_release_commit_hash:
        log_1 = popen('git log --full-diff -p -U1000 --pretty=raw {}..{}'
                    .format(last_release_commit_hash, new_release_commit_hash))
        print(type(log_1))
        log_2 = popen('git log --pretty=format:%H,%ce,%cn,%cd {}..{}'
                      .format(last_release_commit_hash, new_release_commit_hash))
    else:
        log_1 = popen('git log --full-diff -p -U1000 --pretty=raw')
        log_2 = popen('git log --pretty=format:%H,%ce,%cn,%cd')

    diff = log_1.buffer.read().decode('UTF-8', 'ignore')

    log_1.close()
    commit_info = log_2.buffer.read().decode('UTF-8', 'ignore')
    log_2.close()
    #print(diff)
    #print(commit_info)
    release_diff = {
        'commit_info': commit_info,
        'diff': diff,
        'branch_name': branch_name,
        'head_commit_id': new_release_commit_hash,
    }

    # 将工作路径复原
    chdir(origin_path)
    print('change work path: ', getcwd())



    return release_diff
