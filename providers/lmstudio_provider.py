import os, backoff, requests, json
from .base import LLMProvider

class LMStudioProvider(LLMProvider):
    def __init__(self, model: str, base_url: str = "http://localhost:1234/v1"):
        self.model, self.base_url = model, base_url

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def complete(self, messages, **kw) -> str:
        r = requests.post(f"{self.base_url}/chat/completions",
                          json={"model": self.model, "messages": list(messages), **kw}, timeout=120)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
