"""
Module for handling different file types.

This module provides classes for various file types, each implementing the IFileType interface.
Each class provides methods for getting source file extensions and comment characters.
"""

from domain.ifile_type import IFileType
from typing import List
import re

class FileTypePython(IFileType):
    """
    Class representing Python file type.

    This class provides methods for getting source file extensions and comment characters for Python files.
    """

    # def __init__(self, force_destination_file_type, str, force_source_file_types: List = None, force_comment_string: str = None):
    #     """
    #     Initializes a FileTypePython object.

    #     @param force_destination_file_type The destination file type.
    #     @param str 
    #     @param force_source_file_types A list of source file types. Defaults to None.
    #     @param force_comment_string The comment string. Defaults to None.
    #     """
    #     super.__init__(force_destination_file_type, force_source_file_types, force_comment_string)

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Python files.

        @return A list of regular expressions matching Python file extensions.
        """
        return [ r'py$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Python files.

        @return The comment character for Python files.
        """
        return "#"

class FileTypeCpp(IFileType):
    """
    Class representing C++ file type.

    This class provides methods for getting source file extensions and comment characters for C++ files.
    """

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for C++ files.

        @return A list of regular expressions matching C++ file extensions.
        """
        return [ r'[ch][xp\+]*$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for C++ files.

        @return The comment character for C++ files.
        """
        return "//"

class FileTypeJava(IFileType):
    """
    Class representing Java file type.

    This class provides methods for getting source file extensions and comment characters for Java files.
    """

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Java files.

        @return A list of regular expressions matching Java file extensions.
        """
        return [ r'java$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Java files.

        @return The comment character for Java files.
        """
        return "//"

class FileTypeShell(IFileType):
    """
    Class representing Shell file type.

    This class provides methods for getting source file extensions and comment characters for Shell files.
    """

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Shell files.

        @return A list of regular expressions matching Shell file extensions.
        """
        return [ r'[ckz]{0,1}sh$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Shell files.

        @return The comment character for Shell files.
        """
        return "#"

class FileTypeTypescript(IFileType):
    """
    Class representing Typescript file type.

    This class provides methods for getting source file extensions and comment characters for Typescript files.
    """

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Typescript files.

        @return A list of regular expressions matching Typescript file extensions.
        """
        return [ r'[tj]s$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Typescript files.

        @return The comment character for Typescript files.
        """
        return "//"

class FileTypePlantUML(IFileType):
    """
    Class representing PlantUML file type.

    This class provides methods for getting source file extensions, comment characters, and generated file extension for PlantUML files.
    """

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for PlantUML files.

        This method returns a list of regular expressions matching file extensions for various programming languages.

        @return A list of regular expressions matching file extensions.
        """
        list_extensions: List = []
        list_extensions.extend(FileTypeTypescript().get_source_file_extensions())
        list_extensions.extend(FileTypeJava().get_source_file_extensions())
        list_extensions.extend(FileTypeCpp().get_source_file_extensions())
        list_extensions.extend(FileTypePython().get_source_file_extensions())
        list_extensions.extend(FileTypeTypescript().get_source_file_extensions())
        return list_extensions
    
    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for PlantUML files.

        @return The comment character for PlantUML files.
        """
        return "'"
    
    def get_generated_file_extension(self) -> str:
        """
        Gets the generated file extension for PlantUML files.

        @return The generated file extension for PlantUML files.
        """
        return ".puml"

class FileTypeAll(IFileType):
    """
    Class representing all file types.

    This class provides methods for getting source file extensions and generated file extension for all files.
    """

    def _get_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for all files.

        If force_source_file_types is not specified, this method returns a list containing a regular expression matching all file extensions.

        @return A list of regular expressions matching file extensions.
        """
        if self.force_source_file_types is None or len(self.force_source_file_types) == 0:
            return [r'.*']
        return self.force_source_file_types

    def get_generated_file_extension(self) -> str:
        """
        Gets the generated file extension for all files.

        If force_destination_file_type is specified, this method returns a file extension based on the force_destination_file_type.
        Otherwise, it returns '.md'.

        @return The generated file extension for all files.
        """
        return f'.{self.force_destination_file_type}' if self.force_destination_file_type is not None else '.md'
