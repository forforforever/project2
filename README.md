# Whosbug CI 插件

## 本地调试步骤



### 准备被侧仓库

在某一路径下准备好被测项目（一定要是`git`拉下来的，`whosbug`基于`git commit`粒度来解析）



### 环境准备

#### 安装`python3`

这个不多说，`whosbug`是基于`python3`开发的

#### 安装项目依赖

安装`requirements.txt`内的相关依赖

```
pip install -r requirements.txt  # 最好先 pip -V 确认一下pip是指向python3的，如果不是的话使用pip3安装
```



### 设置环境变量

- BK_CI_GIT_REPO_CODE_PATH: 被测仓库的绝对路径 / 相对路径
- BK_CI_GIT_REPO_BRANCH: 被测分支名
- WHOSBUG_SECRET: 对称加密密钥（可以自己定）



### 开始调试

插件主入口为`WhosbugAssign/command_line.py`，无运行参数，直接运行（或运行`setup.py`打包并`pip install`后命令行运行）



### 输出解析结果（已加密）

输出结果在`WhosbugAssign/res.json`内，重要信息均为流加密后的密文