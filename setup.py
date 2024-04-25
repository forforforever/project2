# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def parse_requirements():
    """
    @summary: 获取依赖
    """
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, "requirements.txt")):
        with open(os.path.join(BASE_DIR, "requirements.txt"), 'r') as f_requirements:
            for line in f_requirements.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs


def get_version():
    """
    @summary: 获取版本号. 发布插件时，系统自动传入版本号，无需开发者手动修改
    """
    version_file = os.path.join(BASE_DIR, "version.txt")
    if os.path.exists(version_file):
        with open(version_file, 'r') as f_version:
            version = f_version.read()
    else:
        version = "0.0.1"
    return version.strip()


if __name__ == "__main__":
    setup(
        version=get_version(),
        name="WhosbugAssign",
        description="",
        python_requires='>=3',  # 指定依赖的python版本

        cmdclass={},
        packages=find_packages(),
        include_package_data=True,
        package_data={'': ['*.txt', '*.TXT']},
        data_files=[],
        install_requires=parse_requirements(),

        entry_points={'console_scripts': [
            'WhosbugAssign = WhosbugAssign.command_line:main'
        ]},

        # metadata
        author="kevineluo",
        author_email="kevineluo@tencent.com",
        license="Copyright(c)2010-2018 test All Rights Reserved."
    )
