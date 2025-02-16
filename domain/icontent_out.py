from abc import ABC, abstractmethod
from typing import List

class IContentOut:
    @abstractmethod
    def set_base_file_name(self, out_file_name: str) -> None:
        """
        """

    @abstractmethod
    def write(self, content: str) -> None:
        """
        """
