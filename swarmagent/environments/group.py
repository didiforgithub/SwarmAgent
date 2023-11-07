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
from swarmagent.engine.llm_engine import OpenAILLM
from swarmagent.singleagent.singleagent import Agent


class Group:
    def __init__(self, power_agent: Agent, agent_list: List[Agent], topic: str, mode="conference", max_round=10,
                 message_history=None):
        self.power_agent = power_agent
        self.agent_list = agent_list
        self.topic = topic
        self.mode = mode
        self.max_round = max_round
        if not message_history:
            self.message_history = []
        else:
            self.message_history = message_history
        self.llm = OpenAILLM()

    def group_chat(self):
        if self.mode == "conference":
            result = self.conference()
            return result
        else:
            return None

    def conference(self):
        address_agent = self.power_agent
        conferencing = True
        self.message_history.append(f"{self.mode}'s topic:{self.topic}.")
        conference_prompt = f"You need to play the role of a participant in a meeting. The topic of the meeting is {self.topic}. I will provide you with your Identity Description and the Message history of the meeting. Please speak from the perspective of your role, engaging fully with your Identity and the other participants in the discussion." + "\n" + "Note one: The language style should be close to everyday conversation." + "\n" + "Note two: Before you speak, first consider the Message history and the current issues of the topic, then carefully consider your viewpoint before you contribute to the discussion."

        for i in range(self.max_round):
            print(f"现在是第{i}轮")
            """
            1. 如果round为0则由Power-Agent发言引出话题
            2. 循环逻辑
                2.1 触发Agent Send行为（在conference模式下，Agent_list统一为None，也就是全部发送）；记录发言顺序
                ！！！ 我这里写的非常简单，因为根本没有使用Send，而是使用的messgae_history 统一记录，之后需要改进
                2.2 触发Select_speaker,选择回复者，进入下一轮循环
            3. round 为 max_round - 1 的时候，PowerAgent根据会议记录决定这次会议的结果
                3.0 PowerAgent首先思考自己的想法与会议结果是否一致，如果一致，则进行总结并输出会议结果；如果不一致，思考是否维持自己的建议还是接受会议结果，输出这个决策
            """
            if conferencing:
                chat = address_agent.generate_chat(conference_prompt, f"message history:{self.message}")
                self.message_history.append(f"{address_agent.name}:{chat}")
                print(f"{address_agent.name} says:{chat}")
                address_agent = self.select_speaker()
                conferencing = self.terminate_chat()
            else:
                return self.conclusion_chat()
        return self.conclusion_chat()

    @property
    def message(self):
        msg = ""
        for i in self.message_history:
            msg = msg + i + "\n"
        return msg

    def select_speaker(self):
        select_prompt = f"""
        You are in a role play game. The following roles are available:
        {self.agents_roles()}.

        Read the following conversation.
        Then select the next role from {[agent.name for agent in self.agent_list]} to play. Only return the role."""

        speaker = self.llm.get_response(select_prompt)
        print(f"select_speaker:{speaker}")
        return speaker

    def terminate_chat(self):
        terminate_prompt = f"""
        You have the authority to terminate the meeting. You may choose to end the meeting or to continue it.
        If you decide to continue the meeting, please return True. If you decide to end the meeting, please return False.
        Remember, you can only return True or False
        Your Identity and the transcript of the meeting's discussions are as follows:
        """
        result = self.power_agent.generate_chat(terminate_prompt, f"message history:{self.message}")
        print(f"terminate_chat:{result}")
        return True

    def conclusion_chat(self):
        conclusion_prompt = f"""
        You need to summarize the meeting based on the message_history from the meeting. 
        Then provide your perspective on the issues described in {self.topic}.
        Your Identity and the transcript of the meeting's discussions are as follows:
        """
        result = self.power_agent.generate_chat(conclusion_prompt, f"message history:{self.message}")
        print(f"conclusion_chat:{result}")
        return "conclusion"

    def agents_roles(self):
        return [f"{agent.name}:{agent.identity}" for agent in self.agent_list]
