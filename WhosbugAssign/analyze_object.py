# -*- coding: utf-8 -*-
from re import compile, error
from WhosbugAssign.get_hash import hash_code64


def search_insert(nums, target):
    """
    查找插入位置
    :param nums: 目标数组
    :param target: 比较值

    :return: 插入位置在目标数组中的下标
    """
    if not nums:
        return -1
    if target < nums[0] or target > nums[-1]:
        return -1
    for index in range(len(nums)):
        if target < nums[index]:
            return index - 1
        elif target == nums[index]:
            return index


def find_all_change_line_numbers(lines, re_change_mark=r"^[\+\-]"):
    """Find all the changed lines in diff file

    :param lines: 需要匹配的list类型资料
    :param re_change_mark: 匹配的正则表达式

    :return change_line_numbers: 匹配出的行数数组
    """
    try:
        mark_compile = compile(re_change_mark)
    except error:
        return []
    change_line_numbers = []
    line_number = 0
    # 一行一行正则匹配
    for line in lines:
        # 调整行号
        line_number = line_number + 1
        if mark_compile.search(line):
            change_line_numbers.append({
                'line_number': line_number,
                'change_type': line[0],#+或-
            })
    print(change_line_numbers)
    return change_line_numbers


def find_change_method(change_line_number, antlr_analyze_res):
    """
    Find all the change with ctags type

    :param change_line_number: 更改行
    :param antlr_analyze_res: antlr分析结果

    :return: antlr分析结果中的更改method
    """
    start_line_numbers = [item['startLine'] for item in antlr_analyze_res['methods']]
    print(start_line_numbers)
    res_index = search_insert(start_line_numbers, change_line_number['line_number'])
    print('changelinenumber:{}'.format(change_line_number))
    print('res_index:{}'.format(res_index))

    if res_index > -1:
        return antlr_analyze_res['methods'][res_index]

    return None


def add_object_from_change_line_number(pid: str, file_path: str, objects: dict, change_line_number: dict, antlr_analyze_res):
    """
    找出所有diff method并递归查找外层

    :param pid: 项目的唯一标识
    :param file_path: 当前diff文件在原仓库中的相对路径
    :param objects: 存储找出的所有objects
    :param change_line_number: 更改行
    :param antlr_analyze_res: antlr分析结果

    """
    change_method = find_change_method(change_line_number, antlr_analyze_res)
    print(change_method)
    #返回是antlr_analyze_res里的第几个method（index）
    # 若已存在则return
    if change_method is None or change_method['startLine'] in objects.keys():
        return
    child_hash_code = hash_code64(pid, change_method['methodName'], file_path)
    parent = change_method['masterObject']

    objects[change_method['startLine']] = {
        'name': change_method['methodName'],
        'hash': child_hash_code,
        'parent_name': parent['objectName'] if parent else '',
        'parent_hash': hash_code64(pid, parent['objectName'], file_path) if parent else ''
    }
