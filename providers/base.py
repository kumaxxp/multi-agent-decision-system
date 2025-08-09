from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    def complete(self, messages: Iterable[Dict[str, str]], **kw) -> str: ...
