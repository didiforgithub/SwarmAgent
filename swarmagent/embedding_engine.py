# -*- coding: utf-8 -*-
# Date       : 2023/11/5
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: embedding engine

import openai
import json
import os


class OpenAIEmbedding:
    def __init__(self, name: str, model="text-embedding-ada-002", save_path="storage/embedding_json"):
        self.name = name
        self.model = model
        self.save_path = save_path
        self.embedding_path = os.path.join(self.save_path, f"{self.name}.json")
        os.makedirs(self.embedding_path, exist_ok=True)

    def get_embeddings(self, query):
        with open(self.embedding_path, "r") as f:
            data = json.load(f)
        if query in data:
            return data[query]
        else:
            return self.get_embeddings_openai(query)

    def embedding_save(self, query, embeddings):
        with open(self.embedding_path, "r") as f:
            data = json.load(f)
        data[query] = embeddings
        with open(self.embedding_path, "w") as f:
            json.dump(data, f)

    def get_embeddings_openai(self, query):
        response = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        self.embedding_save(query, embeddings)
        return embeddings
