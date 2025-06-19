from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

class BaseScraper(ABC):    
    @abstractmethod
    def extract(self, url: str) -> Tuple[str, str, List[str]]:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass