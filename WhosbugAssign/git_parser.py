# -*- coding: utf-8 -*-
"""
Parse git logs.

These parsing functions expect output of the following command:

    git log --pretty=raw --numstat

"""
import codecs
from os import makedirs, path
from re import compile, MULTILINE, VERBOSE
from WhosbugAssign.analyze_object import find_all_change_line_numbers
from WhosbugAssign.language_filter import language_filter

__author__ = 'Kevinello'
__email__ = 'Kevinello42@gmail.com'
__version__ = '0.5.2'

month_correspond = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

"""
PAT_COMMIT = r'''
commit\ (?P<commit>[a-f0-9]{40})\n
'''

PAT_DIFF = r'''
(
diff\ \-\-git\ a/(?P<diff_file>.+)\ b/.+\n
)
'''

PAT_DIFF_PART = r'''
(@@\ .*?\ @@\n)'''
"""
PAT_COMMIT = r'commit\ (?P<commit>[a-f0-9]{40})'

PAT_DIFF = r'(diff --git\ a/(?P<diff_file>.+)\ b/.+)'
#@@ -0,0 +1,59 @@
PAT_DIFF_PART = r'(@@\ .*?\ @@)'
# 将上面三个正则表达样式编译为正则表达对象

# 匹配每一次commit
RE_COMMIT = compile(PAT_COMMIT, MULTILINE)
# 匹配每一次commit的每一个diff
RE_DIFF = compile(PAT_DIFF, MULTILINE)
# 匹配每一个diff的更改行头部（eg:@@ -1,8 +1,9 @@）
RE_DIFF_PART = compile(PAT_DIFF_PART, MULTILINE)


def parse_commits(data, commits_info):
    """parse data to serial commits

    Accept a string and parse it into many commits.
    Parse and yield each commit-dictionary.
    This function is a generator.

    :param data: data that get from get diff cmd
    :param commits_info: the header of commit

    :return parsed_commit:include all commits
    """
    raw_commits = list(RE_COMMIT.finditer(data))  # 输入数据，拆分成一个个re_commit格式的commit内容
    #对整个diff进行匹配找到[<re.Match object; span=(0, 48), match='commit f336c40951b7df021ed6ab6cff65109ad53567ea\n>,中的match里的内容
    print(raw_commits)
    print('raw_commits_list:{}'.format(raw_commits))
    # 针对每一条commit
    for (raw_commit, commit_info) in zip(raw_commits, commits_info):
        info_list = commit_info.split(',')
        time_list = info_list[-1][4:].split(' ')
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
        yield parsed_commit


def parse_diff(data):
    """parse commit data

    output the diff code file and yield including all diff message

    :param data: a commit raw data

    :return parts: yield type data which include diff code
    """
    raw_diffs = list(RE_DIFF.finditer(data))
    print('raw_diffs:{}'.format(raw_diffs))
    print(len(raw_diffs))

    for index in range(len(raw_diffs)):
        raw_commit = raw_diffs[index]
        print(raw_commit.groups())
        full_commit = raw_commit.groups()[0]
        print('full_commit{}'.format(full_commit))
        parts = RE_DIFF.match(full_commit).groupdict()
        print('parts{}'.format(parts))
        left_diff_index = raw_commit.span()[0]
        print(left_diff_index)
        if index == len(raw_diffs)-1:
            diff_parts_content = data[left_diff_index:]
            print(diff_parts_content)
        else:
            right_diff_index = raw_diffs[index+1].span()[0]
            diff_parts_content = data[left_diff_index:right_diff_index]
        diff_head_match = list(RE_DIFF_PART.finditer(diff_parts_content))
        print(diff_head_match)
        if diff_head_match:
            # diff头部信息（eg:@@ -1,8 +1,9 @@）
            diff_head = diff_head_match[0]
        else:
            continue
        # diff头部信息右下标(用于字符串截取)
        right_diff_head_index = diff_head.span()[1]
        print(diff_head.span()[1])
        print(diff_head.span()[0])
        tempfile_content = diff_parts_content[right_diff_head_index:]
        lines = tempfile_content.split('\n')
        print(lines)
        change_line_numbers = find_all_change_line_numbers(lines)
        lines = map(lambda x: x[1:], lines)#去掉+-号
        source_code = '\n'.join(lines)
        print(source_code)
        file_name = path.basename(parts["diff_file"])

        if language_filter(file_name):

            print(file_name)
            print("!!!!!!!!!!!!!!!!!!")
            commit_dictionary_name = data[7:17]#f336c40951b7df021ed6ab6cff65109ad53567ea
            print(commit_dictionary_name)
            diff_file_path = 'SourceCode/{}/{}'.format(data[7:17], file_name)
            print(diff_file_path)
            if not path.exists('SourceCode/{}'.format(commit_dictionary_name)):
                makedirs('SourceCode/{}'.format(commit_dictionary_name))
            with codecs.open(diff_file_path, "w", encoding='UTF-8') as ffd:
                ffd.write(source_code)
            parts["diff_file_path"] = diff_file_path
            parts['change_line_numbers'] = change_line_numbers
            print('1111111111111111111111111111111111111111111111111111111')
            print(parts)

            yield parts
        else:
            continue


def to_iso8601(origin):
    """
    :param origin: time with format from git log
    origin :[Jul 16 15:51:03 2016 +0530]

    :return time_iso8601: time with ISO8601 format
    """
    return '{}-{}-{}T{}{}:{}'.format(origin[3], month_correspond[origin[0]], origin[1].zfill(2),
                                     origin[2], origin[4][:3], origin[4][3:])
# "commit_time": "2019-01-27T02:26:01+04:00",



