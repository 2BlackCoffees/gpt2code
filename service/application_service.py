"""
@file ApplicationService.py
@brief This module provides the ApplicationService class, which is responsible for 
       processing source files and generating output based on the provided parameters.

@author [Your Name]
@date [Current Date]
"""

import re
import os
import sys
from pathlib import Path
import logging
from typing import List

from domain.llm_utils import LLMUtils
from domain.icontent_out import IContentOut
from domain.allm_access import AbstractLLMAccess
from domain.gpt2code import GPT2Unittests
from domain.ifile_type import IFileType

from infrastructure.llm_access import LLMAccess
from infrastructure.llm_access_simulate import LLMAccessSimulateCalls
from infrastructure.content_out import ContentOut
from infrastructure.file_types import FileTypeCpp, FileTypeJava, FileTypePython, \
                                      FileTypeShell, FileTypeTypescript, FileTypePlantUML, \
                                      FileTypeAll


class ApplicationService:
    """
    @class ApplicationService
    @brief This class provides the main functionality for processing source files and 
           generating output based on the provided parameters.

    @param from_directory The directory containing the source files to be processed.
    @param to_directory The directory where the output files will be generated.
    @param skip_files A list of files to be skipped during processing.
    @param language_name The name of the programming language being used.
    @param simulate_calls_only A flag indicating whether to simulate LLM calls or not.
    @param logger The logger object used for logging purposes.
    @param llm_utils The LLMUtils object used for LLM-related functionality.
    @param selected_code_request The selected code request.
    @param model_name The name of the LLM model being used.
    @param force_source_file_types A list of source file types to be forced.
    @param force_destination_file_type The destination file type to be forced.
    @param force_comment_string The comment string to be forced.
    @param force_destination_language_name The destination language name to be forced.
    @param force_full_output A flag indicating whether to generate full output or not.
    """

    def __init__(self, from_directory: str, to_directory: str, skip_files: List, language_name: str, simulate_calls_only: bool, \
                 logger: any, llm_utils: LLMUtils, \
                 selected_code_request: int, model_name: str, \
                 force_source_file_types: List, force_destination_file_type: str, force_comment_string: str, 
                 force_destination_language_name: str, force_full_output: bool):
        """
        @brief Initializes the ApplicationService object with the provided parameters.

        @param from_directory The directory containing the source files to be processed.
        @param to_directory The directory where the output files will be generated.
        @param skip_files A list of files to be skipped during processing.
        @param language_name The name of the programming language being used.
        @param simulate_calls_only A flag indicating whether to simulate LLM calls or not.
        @param logger The logger object used for logging purposes.
        @param llm_utils The LLMUtils object used for LLM-related functionality.
        @param selected_code_request The selected code request.
        @param model_name The name of the LLM model being used.
        @param force_source_file_types A list of source file types to be forced.
        @param force_destination_file_type The destination file type to be forced.
        @param force_comment_string The comment string to be forced.
        @param force_destination_language_name The destination language name to be forced.
        @param force_full_output A flag indicating whether to generate full output or not.
        """
        
        # Check if the provided directory is valid
        path = Path(from_directory)
        if not path.is_dir():
            logger.error(f'The directory {from_directory} does not seem to be valid (You are in {os.getcwd()}).')
            exit(1)

        # Initialize the information user list
        information_user: List = []
        if skip_files is not None and len(skip_files) > 0:
            information_user.append(f"Files to be skipped are: {skip_files}")

        # Initialize the content out object
        content_out: IContentOut = ContentOut()
        for information in information_user:
            logger.info(information)
        
        # Initialize the file type object
        file_type: IFileType = None
        if force_destination_language_name is None:
            force_destination_language_name = language_name
        if force_source_file_types is None and force_comment_string is None:
            match language_name.lower():
                case 'c':
                    file_type = FileTypeCpp(force_destination_language_name, force_destination_file_type)
                case 'c++':
                    file_type = FileTypeCpp(force_destination_language_name, force_destination_file_type)
                case 'java':
                    file_type = FileTypeJava(force_destination_language_name, force_destination_file_type)
                case 'python':
                    file_type = FileTypePython(force_destination_language_name, force_destination_file_type)
                case 'shell':
                    file_type = FileTypeShell(force_destination_language_name, force_destination_file_type)
                case 'typescript':
                    file_type = FileTypeTypescript(force_destination_language_name, force_destination_file_type)
                case 'plantuml':
                    file_type = FileTypePlantUML(force_destination_language_name, force_destination_file_type)
        else:
            file_type = FileTypeAll(force_destination_language_name, force_destination_file_type, force_source_file_types, force_comment_string)


        # Initialize the LLM access object
        llm_access: AbstractLLMAccess = LLMAccess(logger, model_name) if not simulate_calls_only \
            else LLMAccessSimulateCalls(logger, model_name)

        # Initialize the GPT2Unittests object
        GPT2Unittests(from_directory, to_directory, skip_files, logger, content_out, llm_utils, selected_code_request, \
                llm_access, language_name, file_type, force_full_output)
