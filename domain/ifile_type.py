"""
@file IFileType.py
@brief This module defines the IFileType class, which represents a file type interface.
        It provides methods to get source file extensions, destination language name, 
        comment characters, and generated file extension.

"""

from abc import ABC, abstractmethod
from typing import List
import re

class FileTypeInterface:
    """
    @class FileTypeInterface
    @brief This class represents a file type interface.
    
    It provides methods to get source file extensions, destination language name, 
    comment characters, and generated file extension.
    
    @param destination_language_name The name of the destination language.
    @param destination_file_extension The file extension of the destination file.
    @param source_file_extensions A list of source file extensions. Defaults to None.
    @param comment_string The comment string. Defaults to None.
    """
    def __init__(self, destination_language_name: str, destination_file_extension: str, comment_string: str = None, source_file_extensions: List[str] = None):
        """
        @brief Initializes the FileTypeInterface object.
        
        @param destination_language_name The name of the destination language.
        @param destination_file_extension The file extension of the destination file.
        @param source_file_extensions A list of source file extensions. Defaults to None.
        @param comment_string The comment string. Defaults to None.
        """
        # Renamed variable names to be more descriptive and follow PEP 8 conventions
        self._destination_language_name: str = destination_language_name
        self._source_file_extensions: List[str] = source_file_extensions
        self._destination_file_extension: str = destination_file_extension
        self._comment_string: str = comment_string

    def _get_raw_source_file_extensions(self) -> List[str]:
        """
        @brief Gets the raw source file extensions.
        
        @return A list of raw source file extensions.
        @note This method is intended to be used internally by the class.
        """
        return self._source_file_extensions
    
    def get_source_file_extensions_as_regex(self) -> List[re.Pattern]:
        """
        @brief Gets the source file extensions as a list of regular expressions.
        
        @return A list of regular expressions representing the source file extensions.
        """

        return [re.compile('\\.' + extension) for extension in self._get_raw_source_file_extensions()]
    
    def get_destination_language_name(self) -> str:
        """
        @brief Gets the destination language name.
        
        @return The destination language name.
        """
        return self._destination_language_name
    
    def _default_comment_characters(self) -> str:
        return ""
    
    def get_comment_characters(self) -> str:
        """
        @brief Gets the comment characters.
        
        @return The comment characters. If comment_string is None, returns an empty string, meaning no comment character.
        """
        return self._comment_string if self._comment_string is not None else self._default_comment_characters()

    def get_generated_file_extension(self) -> str:
        """
        @brief Gets the generated file extension.
        
        @return The generated file extension. If destination_file_extension is None, returns None.
        """
        return f'.{self._destination_file_extension}' if self._destination_file_extension is not None else None
