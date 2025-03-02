"""
Module for handling different file types.

This module provides classes for various file types, each implementing the IFileType interface.
Each class provides methods for getting source file extensions and comment characters.
"""

from domain.ifile_type import FileTypeInterface
from typing import List
import re

class PythonFileType(FileTypeInterface):
    """
    Class representing Python file type.

    This class provides methods for getting source file extensions and comment characters for Python files.
    """

    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Python files.

        @return A list of regular expressions matching Python file extensions.
        """
        return [ 'py$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Python files.

        @return The comment character for Python files.
        """
        return "#"

class CppFileType(FileTypeInterface):
    """
    Class representing C++ file type.

    This class provides methods for getting source file extensions and comment characters for C++ files.
    """

    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for C++ files.

        @return A list of regular expressions matching C++ file extensions.
        """
        return [ '[ch][xp\\+]*$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for C++ files.

        @return The comment character for C++ files.
        """
        # Renamed method to get_cpp_comment_characters for clarity
        return "//"

class JavaFileType(FileTypeInterface):
    """
    Class representing Java file type.

    This class provides methods for getting source file extensions and comment characters for Java files.
    """

    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Java files.

        @return A list of regular expressions matching Java file extensions.
        """

        return [ 'java$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Java files.

        @return The comment character for Java files.
        """

        return "//"

class ShellFileType(FileTypeInterface):
    """
    Class representing Shell file type.

    This class provides methods for getting source file extensions and comment characters for Shell files.
    """

    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Shell files.

        @return A list of regular expressions matching Shell file extensions.
        """

        return [ '[ckz]{0,1}sh$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Shell files.

        @return The comment character for Shell files.
        """

        return "#"

class TypescriptFileType(FileTypeInterface):
    """
    Class representing Typescript file type.

    This class provides methods for getting source file extensions and comment characters for Typescript files.
    """

    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for Typescript files.

        @return A list of regular expressions matching Typescript file extensions.
        """

        return [ '[tj]s$' ]

    def get_comment_characters(self) -> str:
        """
        Gets the comment characters for Typescript files.

        @return The comment character for Typescript files.
        """

        return "//"

class PlantUMLFileType(FileTypeInterface):
    """
    Class representing PlantUML file type.

    This class provides methods for getting source file extensions, comment characters, and generated file extension for PlantUML files.
    """

    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for PlantUML files.

        This method returns a list of regular expressions matching file extensions for various programming languages.

        @return A list of regular expressions matching file extensions.
        """

        supported_file_types = [
            JavaFileType('java', 'java'),
            CppFileType('c++', '[ch][p+x]{2}'),
            PythonFileType('python', 'py'),
            TypescriptFileType('typescript', 'ts')
        ]

        file_extensions = []
        for file_type in supported_file_types:
            file_extensions.extend(file_type.get_source_file_extensions_as_regex())
        return file_extensions

    def get_source_file_extensions_as_regex(self) -> List[re.Pattern]:
        """
        @brief Gets the source file extensions as a list of regular expressions.
        
        @return A list of regular expressions representing the source file extensions.
        """
        return self._get_raw_source_file_extensions()

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

class AllFileType(FileTypeInterface):
    """
    Class representing all file types.

    This class provides methods for getting source file extensions and generated file extension for all files.
    """


    def _get_raw_source_file_extensions(self) -> List:
        """
        Gets the source file extensions for all files.

        If force_source_file_types is not specified, this method returns a list containing a regular expression matching all file extensions.

        @return A list of regular expressions matching file extensions.
        """
        if self.force_source_file_types is None or len(self.force_source_file_types) == 0:
            # If force_source_file_types is not specified, return a list containing a regular expression matching all file extensions
            return ['.*']
        return self.force_source_file_types

    def get_generated_file_extension(self) -> str:
        """
        Gets the generated file extension for all files.

        If force_destination_file_type is specified, this method returns a file extension based on the force_destination_file_type.
        Otherwise, it returns '.md'.

        @return The generated file extension for all files.
        """

        return f'.{self.force_destination_file_type}' if self.force_destination_file_type is not None else '.md'
