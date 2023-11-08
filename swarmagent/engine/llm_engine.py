# -*- coding: utf-8 -*-
# Date       : 2023/11/5
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: LLM engine

import openai
import time


class OpenAILLM:
    def __init__(self, model="gpt-3.5-turbo-1106", temperature=0.7, max_tokens=20, timeout=60):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def get_response(self, prompt: str, max_tokens=None, instructions: str = "No Special Instructions", retries=5):
        if max_tokens:
            self.max_tokens = max_tokens
        if instructions:
            prompt = prompt + instructions
        for i in range(retries):
            try:
                response = openai.ChatCompletion.create(model=self.model, messages=[{"role": "user", "content": prompt}],
                                                    max_tokens=self.max_tokens, temperature=self.temperature)
                return response.choices[0].message.content
            except openai.error.RateLimitError:
                print("Occur RateLimitError, sleep 10s")
                time.sleep(10)
            except openai.error.AuthenticationError:
                print("Please check your openai api key")
            except Exception as e:
                print(e)
