"""
@file ContentOut.py
@brief This module contains the ContentOut class, which is responsible for writing content to a file.
"""

from domain.icontent_out import IContentOut
from typing import List, Dict

class ContentOut(IContentOut):
    """
    @class ContentOut
    @brief This class implements the IContentOut interface and provides methods f
    or setting the base file name and writing content to the file.
    """

    def __init__(self):
        """
        @brief Constructor for the ContentOut class.
        @details Initializes the ContentOut object.
        """
        # Initialize the output file name as None to avoid potential attribute errors
        self._output_file_name = None

    def configure_output_file(self, file_name: str) -> None:
        """
        @brief Initializes the output file with the specified name.
        @details Creates a new file with the specified name if it does not exist, and truncates the file if it already exists.
        @param file_name The name of the output file.
        @return None
        """
        # Added a check to ensure the file name is not None or empty
        if not file_name:
            raise ValueError("File name cannot be empty")
        
        self._output_file_name = file_name
        # Use a try-except block to handle potential file I/O errors
        try:
            with open(self._output_file_name, "w", encoding="utf-8") as file:
                # No need to write an empty string to the file, as opening in 'w' mode will truncate the file
                pass
        except IOError as e:
            print(f"Error initializing output file: {e}")

    def write_content_to_file(self, content: str) -> None:
        """
        @brief Appends content to the output file.
        @details Appends the specified content to the end of the file, followed by a newline character.
        @param content The content to be written to the file.
        @return None
        """
        if self._output_file_name is None:
            raise ValueError("Output file name is not set")
        
        
        # Use a try-except block to handle potential file I/O errors
        with open(self._output_file_name, "a", encoding="utf-8") as file:
            file.write(content + '\n')  # Write the content to the file, followed by a newline character

