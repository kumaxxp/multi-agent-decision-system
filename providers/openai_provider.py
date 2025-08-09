import os, backoff
from openai import OpenAI
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str, base_url: str | None = None):
        self.client = OpenAI(base_url=base_url) if base_url else OpenAI()
        self.model = model

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def complete(self, messages, **kw) -> str:
        resp = self.client.chat.completions.create(model=self.model, messages=list(messages), **kw)
        return resp.choices[0].message.content.strip()
