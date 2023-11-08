# -*- coding: utf-8 -*-
# Date       : 2023/11/6
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Minimum demo
import openai
import os
import swarmagent.singleagent.singleagent as singleagent
import swarmagent.environments.group as group

openai.api_key = os.getenv("OPENAI_KEY")
"""
请使用英文，按照我的要求输出以一下内容
在2023年11月6日，一个中国初创公司的CEO,CTO,CFO在公司会议室讨论是否购入华为的显卡训练AI模型。
这三个人的商业特点与性格特点迥异，但他们都是为了公司的发展而努力。

请你按照以下格式分别输出三个角色的name与Identity，你可以自由发挥，但是要保证输出的内容符合上述要求
{
    "name": ,
    "identitu": 
}
"""

ceo_agent = singleagent.Agent(name="Zhang Wei",
                  identity="Zhang Wei, as the CEO, is a forward-thinking leader who believes in harnessing cutting-edge technology to stay ahead of the competition. She has a keen interest in adopting AI to streamline operations and enhance product offerings. Despite the high costs, she is inclined towards investing in Huawei's GPUs as a long-term strategy for AI development.")
cto_agent = singleagent.Agent(name="Li Jie",
                  identity="Li Jie, the CTO, is deeply tech-savvy with a practical approach. He is meticulous about technical specifications and performance metrics. Although he understands the benefits of Huawei's GPUs for AI, he is cautious about compatibility issues and support. He prefers a balanced approach, weighing the pros and cons of the hardware in the context of the company's specific AI training needs.")
cfo_agent = singleagent.Agent(name="Wang Hong",
                  identity="Wang Hong, serving as the CFO, is very cost-conscious and data-driven. She constantly analyzes the financial implications of any investment and is wary of expenditures that do not promise a clear return on investment (ROI). She acknowledges the potential of AI but is advocating for a thorough cost-benefit analysis before approving the purchase of Huawei's GPUs.")

conference_room = group.Group(ceo_agent, [ceo_agent, cto_agent, cfo_agent],
                        "whether to purchase Huawei's GPUs for AI training", mode="conference", max_round=10)
print(conference_room.power_agent)
result = conference_room.conference()

print(f"会议结果为{result}")
print(f"会议历史记录为{conference_room.message_history}")
