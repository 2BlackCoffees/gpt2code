"""
@file ContentOut.py
@brief This module contains the ContentOut class, which is responsible for writing content to a file.
@author [Your Name]
@date [Today's Date]
"""

from domain.icontent_out import IContentOut
from typing import List, Dict

class ContentOut(IContentOut):
    """
    @class ContentOut
    @brief This class implements the IContentOut interface and provides methods for setting the base file name and writing content to the file.
    """

    def __init__(self):
        """
        @brief Constructor for the ContentOut class.
        @details Initializes the ContentOut object.
        """
        pass

    def set_base_file_name(self, out_file_name: str) -> None:
        """
        @brief Sets the base file name for the output file.
        @details Creates a new file with the specified name if it does not exist, and truncates the file if it already exists.
        @param out_file_name The name of the output file.
        @return None
        """
        self.out_file_name = out_file_name
        with open(self.out_file_name, "w", encoding="utf-8") as file:
            """
            @brief Opens the file in write mode and sets the encoding to UTF-8.
            @details If the file does not exist, it will be created. If the file already exists, its contents will be truncated.
            """
            file.write('')  # Write an empty string to the file to ensure it is created

    def write(self, content: str) -> None:
        """
        @brief Writes content to the output file.
        @details Appends the specified content to the end of the file, followed by a newline character.
        @param content The content to be written to the file.
        @return None
        """
        with open(self.out_file_name, "a", encoding="utf-8") as file:
            """
            @brief Opens the file in append mode and sets the encoding to UTF-8.
            @details If the file does not exist, it will be created. If the file already exists, the content will be appended to the end of the file.
            """
            file.write(content + '\n')  # Write the content to the file, followed by a newline character
