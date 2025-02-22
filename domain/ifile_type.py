"""
@file IFileType.py
@brief This module defines the IFileType class, which represents a file type interface.
        It provides methods to get source file extensions, destination language name, 
        comment characters, and generated file extension.

@author [Your Name]
@date [Today's Date]
"""

from abc import ABC, abstractmethod
from typing import List
import re

class IFileType():
    """
    @class IFileType
    @brief This class represents a file type interface.
    
    It provides methods to get source file extensions, destination language name, 
    comment characters, and generated file extension.
    
    @param destination_language_name The name of the destination language.
    @param force_destination_file_type The file type of the destination file.
    @param force_source_file_types A list of source file types. Defaults to None.
    @param force_comment_string The comment string. Defaults to None.
    """
    def __init__(self, destination_language_name: str, force_destination_file_type: str, force_source_file_types: List = None, force_comment_string: str = None):
        """
        @brief Initializes the IFileType object.
        
        @param destination_language_name The name of the destination language.
        @param force_destination_file_type The file type of the destination file.
        @param force_source_file_types A list of source file types. Defaults to None.
        @param force_comment_string The comment string. Defaults to None.
        """
        self.destination_language_name: str = destination_language_name
        self.force_source_file_types: List = force_source_file_types
        self.force_destination_file_type: str = force_destination_file_type
        self.force_comment_string: str = force_comment_string

    def _get_source_file_extensions(self) -> str:
        """
        @brief Gets the source file extensions.
        
        @return A string of source file extensions.
        @note This method is intended to be used internally by the class.
        """
        return self.force_source_file_types 
    
    def get_source_file_extensions(self) -> List:
        """
        @brief Gets the source file extensions as a list of regular expressions.
        
        @return A list of regular expressions representing the source file extensions.
        """
        return [re.compile(r'\.' + extension) for extension in self._get_source_file_extensions()]
    
    def get_destination_language_name(self) -> str:
        """
        @brief Gets the destination language name.
        
        @return The destination language name.
        """
        return self.destination_language_name
    
    def get_comment_characters(self) -> str:
        """
        @brief Gets the comment characters.
        
        @return The comment characters. If force_comment_string is None, returns an empty string.
        """
        return self.force_comment_string if self.force_comment_string is not None else ""

    def get_generated_file_extension(self) -> str:
        """
        @brief Gets the generated file extension.
        
        @return The generated file extension. If force_destination_file_type is None, returns None.
        """
        return f'.{self.force_destination_file_type}' if self.force_destination_file_type is not None else None
