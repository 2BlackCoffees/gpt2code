from abc import ABC, abstractmethod
from typing import List
import re

class IFileType():
    def __init__(self, destination_language_name: str, force_destination_file_type: str, force_source_file_types: List = None, force_comment_string: str = None):
        self.destination_language_name: str = destination_language_name
        self.force_source_file_types: List = force_source_file_types
        self.force_destination_file_type: str = force_destination_file_type
        self.force_comment_string: str = force_comment_string

    def _get_source_file_extensions(self) -> str:
        return self.force_source_file_types 
    
    def get_source_file_extensions(self) -> List:
        return [re.compile(r'\.' + extension) for extension in self._get_source_file_extensions()]
    
    def get_destination_language_name(self) -> str:
        return self.destination_language_name
    
    def get_comment_characters(self) -> str:
        return self.force_comment_string if self.force_comment_string is not None else ""

    def get_generated_file_extension(self) -> str:
        return f'.{self.force_destination_file_type}' if self.force_destination_file_type is not None else None
