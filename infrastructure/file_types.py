from domain.ifile_type import IFileType
from typing import List
import re

class FileTypePython(IFileType):
    # def __init__(self, force_destination_file_type, str, force_source_file_types: List = None, force_comment_string: str = None):
    #     super.__init__(force_destination_file_type, force_source_file_types, force_comment_string)
    def _get_source_file_extensions(self) -> List:
        return [ r'py$' ]

    def get_comment_characters(self) -> str:
        return "#"
    
class FileTypeCpp(IFileType):

    def _get_source_file_extensions(self) -> List:
        return [ r'[ch][xp\+]*$' ]

    def get_comment_characters(self) -> str:
        return "//"
    
class FileTypeJava(IFileType):
    def _get_source_file_extensions(self) -> List:
        return [ r'java$' ]

    def get_comment_characters(self) -> str:
        return "//"

class FileTypeShell(IFileType):

    def _get_source_file_extensions(self) -> List:
        return [ r'[ckz]{0,1}sh$' ]

    def get_comment_characters(self) -> str:
        return "#"

class FileTypeTypescript(IFileType):

    def _get_source_file_extensions(self) -> List:
        return [ r'[tj]s$' ]

    def get_comment_characters(self) -> str:
        return "//"

class FileTypePlantUML(IFileType):
    def _get_source_file_extensions(self) -> List:
        list_extensions: List = []
        list_extensions.extend(FileTypeTypescript().get_source_file_extensions())
        list_extensions.extend(FileTypeJava().get_source_file_extensions())
        list_extensions.extend(FileTypeCpp().get_source_file_extensions())
        list_extensions.extend(FileTypePython().get_source_file_extensions())
        list_extensions.extend(FileTypeTypescript().get_source_file_extensions())
        return list_extensions
    
    def get_comment_characters(self) -> str:
        return "'"
    
    def get_generated_file_extension(self) -> str:
        return ".puml"
    
class FileTypeAll(IFileType):
    def _get_source_file_extensions(self) -> List:
        if self.force_source_file_types is None or len(self.force_source_file_types) == 0:
            return [r'.*']
        return self.force_source_file_types

    def get_generated_file_extension(self) -> str:
        return f'.{self.force_destination_file_type}' if self.force_destination_file_type is not None else '.md'