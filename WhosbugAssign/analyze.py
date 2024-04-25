# -*- coding: utf-8 -*-
from WhosbugAssign.analyze_object import add_object_from_change_line_number
from WhosbugAssign.antlr_analyzer import analyze_java



def analyze_commit_diff(pid, commit_diffs, commit_id, commit):
    """分析一次commit的所有变更文件

    :param pid: 项目的唯一标识
    :param commit_diffs: 一次commit的所有变更文件（一个diff对应一个变更文件）
    :param commit_id: 该次commit的版本号
    :param commit: 包含该次commit的所有diff objects的dict（commit['commit_diffs']即为该次commit的所有diff objects）

    """
    # log_init()

    for commit_diff in commit_diffs:
        commit_diff["commit"] = commit_id  # 版本号
        commit_diff["diff_content"] = {}
        tempfile = commit_diff["diff_file_path"]  # 处理后源码路径
        file_path = commit_diff['diff_file']

        # antlr分析源码
        try:
            antlr_analyze_res = analyze_java(tempfile)
        except AttributeError:
            print("We can't analyze file {}".format(tempfile))
            continue
        except:
            continue
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(antlr_analyze_res)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # 该diff文件的所有更改行号
        change_line_numbers = commit_diff['change_line_numbers']
        objects = {}

        for change_line_number in change_line_numbers:  # 遍历变更行号
            add_object_from_change_line_number(pid, file_path, objects, change_line_number, antlr_analyze_res)
        print('objects:{}:'.format(objects))
        # 将该diff分析结果归属到每个产生diff的文件下
        commit_diff["diff_content"] = objects
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(commit_diff["diff_content"])
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # 将diff file归属到该次commit下
        commit["commit_diffs"].append(commit_diff)
