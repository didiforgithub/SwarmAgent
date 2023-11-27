# -*- coding: utf-8 -*-
# Date       : 2023/11/27
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 方案2 Env实现

from generate_world import generate


class Environment:

    def __init__(self):
        pass

    def run(self):
        """
        根据输入的时间轮数，遍历环境中的Group，判断是否展开Group的讨论行为
        随后基于下一轮的时间，将Agent安排到Plan产生的Group之中
        """
        pass

    def generate(self):
        """
        基于输入的Idea，生成一个适配的Group群体与Agent群体
        需要调用外部函数
        """
        generate()
        pass

    def publish(self):
        """
        发布公开信息，考虑一下什么类型的Group能够接收到
        """
        pass

    def save(self):
        """
        保存当前环境中各个Group的状态
        """
        pass

    def load(self):
        """
        加载环境与当前环境中Group状态
        """
        pass
