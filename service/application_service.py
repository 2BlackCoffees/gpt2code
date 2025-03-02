"""
@file ApplicationService.py
@brief This module provides the ApplicationService class, which is responsible for 
       processing source files and generating output based on the provided parameters.
"""

import os
from pathlib import Path
from logging import Logger
from typing import List

from domain.llm_utils import LLMUtils
from domain.icontent_out import IContentOut
from domain.allm_access import AbstractLLMAccess
from domain.gpt2code import GPT2Code
from domain.ifile_type import FileTypeInterface

from infrastructure.llm_access import LLMAccess
from infrastructure.llm_access_simulate import LLMAccessSimulator
from infrastructure.content_out import ContentOut
from infrastructure.file_types import CppFileType, JavaFileType, PythonFileType, \
                                      ShellFileType, TypescriptFileType, PlantUMLFileType, \
                                      AllFileType


class ApplicationService:
    """
    @class ApplicationService
    @brief This class provides the main functionality for processing source files and 
           generating output based on the provided parameters.

    @param source_directory The directory containing the source files to be processed.
    @param destination_directory The directory where the output files will be generated.
    @param files_to_skip A list of files to be skipped during processing.
    @param language_name The name of the programming language being used.
    @param simulate_llm_calls_only A flag indicating whether to simulate LLM calls or not.
    @param logger The logger object used for logging purposes.
    @param llm_utils The LLMUtils object used for LLM-related functionality.
    @param selected_code_request The selected code request.
    @param model_name The name of the LLM model being used.
    @param forced_source_file_types A list of source file types to be forced.
    @param forced_destination_file_type The destination file type to be forced.
    @param forced_comment_string The comment string to be forced.
    @param forced_destination_language_name The destination language name to be forced.
    @param generate_full_output A flag indicating whether to generate full output or not.
    """

    def __init__(self, source_directory: str, destination_directory: str, files_to_skip: List, language_name: str, \
                 simulate_llm_calls_only: bool, logger: Logger, llm_utils: LLMUtils, \
                 selected_code_request: int, model_name: str, \
                 forced_source_file_types: List, forced_destination_file_type: str, forced_comment_string: str, 
                 forced_destination_language_name: str, generate_full_output: bool):
        """
        @brief Initializes the ApplicationService object with the provided parameters.

        @param source_directory The directory containing the source files to be processed.
        @param destination_directory The directory where the output files will be generated.
        @param files_to_skip A list of files to be skipped during processing.
        @param language_name The name of the programming language being used.
        @param simulate_llm_calls_only A flag indicating whether to simulate LLM calls or not.
        @param logger The logger object used for logging purposes.
        @param llm_utils The LLMUtils object used for LLM-related functionality.
        @param selected_code_request The selected code request.
        @param model_name The name of the LLM model being used.
        @param forced_source_file_types A list of source file types to be forced.
        @param forced_destination_file_type The destination file type to be forced.
        @param forced_comment_string The comment string to be forced.
        @param forced_destination_language_name The destination language name to be forced.
        @param generate_full_output A flag indicating whether to generate full output or not.
        """
        
        # Check if the provided directory is valid
        source_directory_path = Path(source_directory)
        if not source_directory_path.is_dir():
            # Added a comment to explain the purpose of the error message
            logger.error(f'The directory {source_directory} does not seem to be valid (You are in {os.getcwd()}).')
            # Exit the program with a non-zero status code to indicate an error
            exit(1)

        # Initialize the information user list
        information_messages: List = []
        if files_to_skip is not None and len(files_to_skip) > 0:
            # Changed 'Files to be skipped are' to 'The following files will be skipped' for clarity
            information_messages.append(f"The following files will be skipped: {files_to_skip}")

        output_handler: IContentOut = ContentOut()
        # Log each information message
        for information in information_messages:
            logger.info(information)
        
        # Initialize the file type object
        file_type_handler: FileTypeInterface = None

        # Set the forced destination language name if it is not provided
        if forced_destination_language_name is None:
            forced_destination_language_name = language_name

        # Determine the file type handler based on the language name and forced parameters
        if forced_source_file_types is None and forced_comment_string is None:

            # Use a match statement to determine the file type handler based on the language name
            match language_name.lower():
                case 'c':
                    # Use FileTypeCpp for C language
                    file_type_handler = CppFileType(forced_destination_language_name, forced_destination_file_type)
                case 'c++':
                    # Use FileTypeCpp for C++ language
                    file_type_handler = CppFileType(forced_destination_language_name, forced_destination_file_type)
                case 'java':
                    # Use FileTypeJava for Java language
                    file_type_handler = JavaFileType(forced_destination_language_name, forced_destination_file_type)
                case 'python':
                    # Use FileTypePython for Python language
                    file_type_handler = PythonFileType(forced_destination_language_name, forced_destination_file_type)
                case 'shell':
                    # Use FileTypeShell for Shell language
                    file_type_handler = ShellFileType(forced_destination_language_name, forced_destination_file_type)
                case 'typescript':
                    # Use FileTypeTypescript for Typescript language
                    file_type_handler = TypescriptFileType(forced_destination_language_name, forced_destination_file_type)
                case 'plantuml':
                    # Use FileTypePlantUML for PlantUML language
                    file_type_handler = PlantUMLFileType(forced_destination_language_name, forced_destination_file_type)
        else:
            # Use FileTypeAll for other languages
            file_type_handler = AllFileType(forced_destination_language_name, forced_destination_file_type, forced_source_file_types, forced_comment_string)


        # Renamed 'llm_access' to 'llm_access_handler' for clarity
        llm_access_handler: AbstractLLMAccess = LLMAccess(logger, model_name) if not simulate_llm_calls_only \
            else LLMAccessSimulator(logger, model_name)

        self.initialize_gpt2code(source_directory, destination_directory, files_to_skip, logger, output_handler, llm_utils, selected_code_request, \
                llm_access_handler, language_name, file_type_handler, generate_full_output)

    def initialize_gpt2code(self, source_directory: str, destination_directory: str, files_to_skip: List, logger: Logger, output_handler: IContentOut, llm_utils: LLMUtils, selected_code_request: int, \
                llm_access_handler: AbstractLLMAccess, language_name: str, file_type_handler: FileTypeInterface, generate_full_output: bool):
        """
        @brief Initializes the GPT2Code object with the provided parameters.

        @param source_directory The directory containing the source files to be processed.
        @param destination_directory The directory where the output files will be generated.
        @param files_to_skip A list of files to be skipped during processing.
        @param logger The logger object used for logging purposes.
        @param output_handler The output handler object used for handling output.
        @param llm_utils The LLMUtils object used for LLM-related functionality.
        @param selected_code_request The selected code request.
        @param llm_access_handler The LLM access handler object used for accessing LLM models.
        @param language_name The name of the programming language being used.
        @param file_type_handler The file type handler object used for handling file types.
        @param generate_full_output A flag indicating whether to generate full output or not.
        """
        GPT2Code(source_directory, destination_directory, files_to_skip, logger, output_handler, llm_utils, selected_code_request, \
                llm_access_handler, language_name, file_type_handler, generate_full_output)
