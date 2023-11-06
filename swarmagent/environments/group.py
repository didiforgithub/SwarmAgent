# -*- coding: utf-8 -*-
# Date       : 2023/11/6
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 多Agent的Environment


"""
多agent的环境
1. 实现消息的发送与接受
2. 在会议模式下选择Speaker，由大模型决定谁下一个来发言

引入AutoGen选择Speaker的机制，由大模型决定下一个谁来发言


"""
from typing import List
from swarmagent.singleagent.singleagent import Agent


class Group:
    def __init__(self, power_agent: Agent, agent_list: List, topic: str, mode="conference", max_round=10,
                 message_history=[]):
        self.power_agent = power_agent
        self.agent_list = agent_list
        self.topic = topic
        self.mode = mode
        self.max_round = max_round
        self.message_history = message_history

    def group_chat(self):
        if self.mode == "conference":
            result = self.conference()
            return result
        else:
            return None

    def conference(self):
        address_agent = self.power_agent
        conferencing = True
        for i in range(self.max_round):
            """
            1. 如果round为0则由Power-Agent发言引出话题
            2. 循环逻辑
                2.1 触发Agent Send行为（在conference模式下，Agent_list统一为None，也就是全部发送）；记录发言顺序
                2.2 触发Select_speaker,选择回复者，进入下一轮循环
            3. round 为 max_round - 1 的时候，PowerAgent根据会议记录决定这次会议的结果
                3.0 PowerAgent首先思考自己的想法与会议结果是否一致，如果一致，则进行总结并输出会议结果；如果不一致，思考是否维持自己的建议还是接受会议结果，输出这个决策
            """
            if conferencing:
                chat = address_agent.generate_chat(self.topic)
                self.message_history.append(f"{address_agent.name}:{chat}")
                address_agent = self.select_speaker()
                conferencing = self.terminate_chat()
            else:
                return self.conclusion_chat()
        return self.conclusion_chat()


    def select_speaker(self):
        """
        使用大模型Select发言者（需要输入的内容有过去的聊天记录，历史发言顺序，角色职责与个性）
        :return:
        """
        return self.agent_list[1]

    def terminate_chat(self):
        return True

    def conclusion_chat(self):
        return "conclusion"
