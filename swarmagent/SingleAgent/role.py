# -*- coding: utf-8 -*-
# Date       : 2023/11/1
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 单Agent的Role Class

"""
Role需要支持哪些功能
对内
1. 支持记忆结构
2. 支持Brain 所有方法（实现记忆结构，实现RAG，实现Decision（不同情况写不同的React Prompt），实现Plan规划）
对外
3. 支持一系列底层 TOOL

对外
1. 支持MultiAgent的Environment环境
2. 支持 perceive 方法获取环境信息
"""


class Agent():
    def __init__(self):
        pass

       