"""
@file IContentOut.py
@brief Abstract base class for content output operations.

This module defines the IContentOut abstract base class, which provides a common interface for writing content to output files.
"""

from abc import ABC, abstractmethod
from typing import List

class IContentOut(ABC):
    """
    @class IContentOut
    @brief Abstract base class for content output operations.

    This class defines the interface for writing content to output files. It provides two abstract methods: set_base_file_name and write.
    """

    @abstractmethod
    def set_base_file_name(self, out_file_name: str) -> None:
        """
        @brief Sets the base file name for the output file.

        @param out_file_name The base file name for the output file.
        @return None
        @note This method must be implemented by any concrete subclass of IContentOut.
        """
        """
        """

    @abstractmethod
    def write(self, content: str) -> None:
        """
        @brief Writes content to the output file.

        @param content The content to be written to the output file.
        @return None
        @note This method must be implemented by any concrete subclass of IContentOut.
        """
        """
        """
