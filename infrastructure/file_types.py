from domain.ifile_type import IFileType
from typing import List
class FileTypePython(IFileType):

    def _get_file_extension(self) -> str:
        return r'py$'

    def get_comment_characters(self) -> str:
        return "#"
    
class FileTypeCpp(IFileType):

    def _get_file_extension(self) -> str:
        return r'[ch][xp\+]*$'

    def get_comment_characters(self) -> str:
        return "//"
    
class FileTypeJava(IFileType):
    def _get_file_extension(self) -> str:
        return r'java$'

    def get_comment_characters(self) -> str:
        return "//"

class FileTypeShell(IFileType):

    def _get_file_extension(self) -> str:
        return r'[ckz]{0,1}sh$'

    def get_comment_characters(self) -> str:
        return "#"

class FileTypeTypescript(IFileType):

    def _get_file_extension(self) -> str:
        return r'[tj]s$'

    def get_comment_characters(self) -> str:
        return "//"