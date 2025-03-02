"""
@file IContentOut.py
@brief Abstract base class for content output operations.

This module defines the IContentOut abstract base class, which provides a common interface for writing content to output files.
"""

from abc import ABC, abstractmethod

class IContentOut(ABC):
    """
    @class IContentOut
    @brief Abstract base class for content output operations.

    This class defines the interface for writing content to output files. 
    """

    @abstractmethod
    def configure_output_file(self, output_file_name: str) -> None:
        """
        @brief Configures the output file by setting its base name.

        @param output_file_name The base name for the output file.
        @return None
        @note This method must be implemented by any concrete subclass of IContentOut.
        """
        pass

    @abstractmethod
    def write_content_to_file(self, content_to_write: str) -> None:
        """
        @brief Writes the provided content to the configured output file.

        @param content_to_write The content to be written to the output file.
        @return None
        @note This method must be implemented by any concrete subclass of IContentOut.
        """
        pass
