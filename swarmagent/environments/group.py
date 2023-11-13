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
from swarmagent.engine.llm_engine import OpenAILLM, prompt_load
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
        conference_prompt = f"""
        In a role-playing game, you're participating in a meeting centered around the topic of {self.topic}. 
        You are limited to playing the specific character mentioned previously. Your responses and decisions must be based solely on this character's perspective, considering their unique role and background.
        Here are some guidelines:
            1. Starting the Meeting: If the dialogue history is empty, it means you need to initiate the meeting. Begin with an opening statement that sets the stage for the discussion, focusing on the theme of {self.topic}. Your opening could introduce the topic, highlight its importance, and perhaps pose a question or thought to encourage participation from others.
            2. Concise Contributions: Avoid long speeches. Instead, make your points succinctly, allowing room for others to contribute. Your remarks should be insightful but not exhaustive, leaving aspects open for further exploration by other participants.
            3. Engaging with Others: Engaging with Others: When others seek opinions, focus on responding to their views and needs rather than repetitively expressing your own desire for their input. Your aim should be to advance the conversation by acknowledging and building upon what others have said, fostering a collaborative dialogue that moves the discussion forward.
            4. Normal Speaking Tone in Results: When participating in discussions, use a normal speaking tone that reflects how your character would verbally express themselves in the meeting. Avoid the tone of internal thoughts or monologues. Ensure that your character's responses and contributions sound like natural dialogue in the context of the role-playing game
        """
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
                chat = address_agent.generate_chat(query=f"message history: {self.message}",
                                                   instruction=f"instruction: {conference_prompt}", max_tokens=300)
                self.message_history.append(f"{address_agent.name}:{chat}")
                address_agent = self.select_speaker()
                conferencing = self.terminate_chat()
            else:
                return self.conclusion_chat()
        return self.conclusion_chat()

    @property
    def message(self):
        msg = ""
        for i in self.message_history:
            msg = msg + i + "\n" + "\n"
        return msg

    def get_agent(self, name: str):
        for agent in self.agent_list:
            if agent.name == name:
                return agent
        return None

    def agents_roles(self):
        return [f"{agent.name}:{agent.profile}" for agent in self.agent_list]

    def select_speaker(self):
        # TODO self.mode choose different select_prompt
        # TODO 修改Prompt
        select_prompt = f""" 
        You are a conference coordinator skilled at deducing people's thoughts.
        There are {len(self.agent_list)} participants in this meeting, each with unique personality traits and perspectives outlined in {self.agents_roles()}.
        Your task is to predict who is most likely to speak next in the context of the current meeting discussion {self.message}.
        Return your prediction as a JSON-formatted string, structured as follows.
        {{
        'next_speaker': 
        }}"""
        speaker = self.llm.get_response(prompt=select_prompt, json_mode=True)
        speaker_agent = self.get_agent(speaker['next_speaker'])
        if speaker_agent:
            return speaker_agent
        else:
            return self.power_agent

    def terminate_chat(self):
        """
        TODO self.mode choose diffrent terminate_prompt
        """
        terminate_prompt = prompt_load("swarmagent/prompt/group_conference_terminate.txt")
        json_result = self.power_agent.generate_json(query=f"message history:{self.message}",
                                                     instruction=terminate_prompt)
        print(f"terminate_chat:{json_result['action']}")
        result = True if json_result["action"] == "continue" else False
        return result

    def conclusion_chat(self):
        """
        TODO self.mode choose diffrent conclusion_prompt
        TODO 这里要不要跟上一个合并啊？但是感觉会破坏逻辑，主要在于是轮次结束决定的结束还是PowerAgent决定的结束
        """
        conclusion_prompt = f"""
        In a role-playing game, you are participating in a meeting focused on the topic of {self.topic}.
        You need to play the character mentioned above and make decisions based on the historical conversation of the meeting and your character's thoughts.
        The decision can be to carry out something, or it can be an approval or opposition to the Topic.
        When making your decision, you should consider from a deeper perspective why you want to make this decision, and summarize a reason to persuade other speakers. 
        When making your decision, please return the result in JSON format to ensure compatibility with Python's json.loads() function. The format should be as follows:
        {{
        "decision": "Your decision",
        "reason": "Your reason"
        }}
        """
        result = self.power_agent.generate_json(query=f"message history: {self.message}", instruction=conclusion_prompt)
        print(f"conclusion_chat:{result}")
        return f'decision:{result["decision"]},reason:{result["reason"]}'
