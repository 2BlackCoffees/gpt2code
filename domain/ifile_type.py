from abc import ABC, abstractmethod
from typing import List

class IFileType(ABC):
    @abstractmethod
    def _get_file_extension(self) -> str:
        """
        """
    def get_file_extension(self) -> str:
        return '.' + self._get_file_extension()

    @abstractmethod
    def get_comment_characters(self) -> str:
        """
        """