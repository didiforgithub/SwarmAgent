import openai
import os
from swarmagent.engine.llm_engine import OpenAILLM

openai.api_key = os.getenv("OPENAI_KEY")
prompt = """You're god in the earth, please give random one's name and identity.
Please return with json format just like below:
{
    "name":,
    "identity":
}
"""
# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-1106",
#     messages=[{"role": "user", "content": prompt}],
#     max_tokens=300,
#     response_format = {"type":"json_object"}
# )
#
# print(response.choices[0].message.content)
llm = OpenAILLM()
result = llm.get_response(prompt, json_mode=True)
print(result)
print(type(result))