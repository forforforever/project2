# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import json
from WhosbugAssign.code_diff import analysis
from WhosbugAssign.to_database import result


def demo():
    """
    @summary: WhosbugAssign
    """
    print("enter WhosbugAssign")
    # 输入F
    input_params = get_input()
    # 获取名为inputDemo的输入字段值
    project_id = input_params.get("__PROJRCT_ID", None)
    release_version = input_params.get("__RELEASE_VERSION") or '1.0.0(default)'
    repo_path = input_params.get('__PROJECT_URL') or os.getenv("BK_CI_GIT_REPO_CODE_PATH")

    branch_name = os.getenv("BK_CI_GIT_REPO_BRANCH", 'master')

    print(
        "project_id: {}\n"
        "release: {}\n"
        "repo_path: {}\n"
        "branch_name: {}".format(project_id, release_version,
                                 repo_path, branch_name))

    res_commits = analysis(repo_path, branch_name, project_id)
    print('res_commits{}'.format(res_commits))
    print(res_commits)
    print(len(res_commits))
    if res_commits:
        result(res_commits, project_id, release_version)
    else:
        print('release is up to date')

    print("whosbug analysis done")

    exit(0)


def get_input():
    with open('../input.json', 'r') as f:
        return json.load(f)


def main():
    demo()


if __name__ == "__main__":
    main()
