# -*- coding: utf-8 -*-
from fnmatch import fnmatch

'''
support_languages = ['*.cpp', '*.py', '*.c', '*.java', '*.c++', '*.cc', '*.cp', '*.cpp', '*.cxx',
                     '*.h', '*.h++', '*.hh', '*.hp', '*.hpp', '*.hxx', '*.inl', '*.H', '*.CPP', '*.C',
                     '*.cs', '*.go', '*.js', '*.jsx', '*.mjs', '*.mm', '*.m', '*.h', '*.py', '*.pyx',
                     '*.pxd', '*.pxi', '*.scons', '*.wsgi', '*.kt', '*.kts', '*.swift']
'''
support_languages = ['*.java', ]


def language_filter(file_name):
    """过滤后缀得到支持的语言

    :param file_name: 目标文件名

    :return support_language: 过滤结果
    """
    for support_language in support_languages:
        if fnmatch(file_name, support_language):
            return support_language
    return False
