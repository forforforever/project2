# -*- coding: utf-8 -*-
from WhosbugAssign.git_parser import parse_commits, parse_diff
from WhosbugAssign.get_diff import get_diff
from WhosbugAssign.analyze import analyze_commit_diff


def analysis(repo_path, branch_name, pid):
    """
    diff parse for a new version release

    :param pid: 项目的唯一标识
    :param repo_path: 项目的保存路径
    :param branch_name: 项目的分支名

    :return all_commits: final result dict of diff-parse
    """

    release_diff = get_diff(repo_path, branch_name, pid)#将所有diff字符串读进来
    """
    release_diff = {
        'commit_info': commit_info, 部分提交信息的字段含时间 哈希 邮箱 名字 日期
        'diff': diff, 所有信息的字段
        'branch_name': branch_name,
        'head_commit_id': new_release_commit_hash,
    }
    """
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #print(release_diff['diff'])
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    commits = list(parse_commits(release_diff['diff'], release_diff['commit_info'].split('\n')))
    """
    
    parsed_commit = {
            'commit_left_index': raw_commit.span()[0],  #每个<re.Match object; span=(0, 48), match='commit
            # f336c40951b7df021ed6ab6cff65109ad53567ea\n>的commit：的起始位置
            'commit': info_list[0],#例如 40d42574e065e8078b242d201e0fc1455c430c71
            'commit_time': to_iso8601(time_list),
            'committer': {
                'name': info_list[2],
                'email': info_list[1]
            }
        }
    """
    all_commits = []

    for index in range(len(commits)):#1421
        commit = commits[index]
        commit_id = commit["commit"]  # 版本号 如f336c40951b7df021ed6ab6cff65109ad53567ea
        if index == len(commits)-1:
            diff_park = release_diff['diff'][commit['commit_left_index']:]#读出单次commit的commit以下的内容
        else:
            next_commit_left_index = commits[index + 1]['commit_left_index']
            # 从commit详细info中抽取出的重要diff部分
            diff_park = release_diff['diff'][commit['commit_left_index']:next_commit_left_index]
        # 从diff_park得到一次commit的diff集合

        commit_diffs = list(parse_diff(diff_park))#parts
        print('commit_diffs:{}'.format(commit_diffs))

        commit["commit_diffs"] = []
        analyze_commit_diff(pid, commit_diffs, commit_id, commit)
        print("!!!!!!!!!!")
        print(commit)
        print("!!!!!!!!!!!!!!!!!")
        all_commits.append(commit)



    return all_commits
