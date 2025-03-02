"""
@file GPT2Unittests.py
@brief This module contains the GPT2Unittests class, which is responsible for processing source files and generating output based on LLM requests.

@author [Your Name]
@date [Today's Date]
"""

import os
import re
import traceback
from pprint import pformat
from typing import List
from logging import Logger

from domain.ichecker import IRequestHandler, CodeCheckerRequestHandler
from domain.allm_access import AbstractLLMAccess
from domain.llm_utils import LLMUtils
from domain.ifile_type import FileTypeInterface
from domain.icontent_out import IContentOut

class GPT2Code                                                                                                               :
    """
    @class GPT2Unittests
    @brief This class is responsible for processing source files and generating output based on LLM requests.

    @param source_directory The directory to read source files from.
    @param target_directory The directory to write output files to.
    @param files_to_exclude A list of files to skip during processing.
    @param logger A logger instance for logging messages.
    @param content_writer An instance of IContentOut for writing output.
    @param llm_utilities An instance of LLMUtils for LLM-related utilities.
    @param selected_code_request The selected code request to use.
    @param llm_access An instance of AbstractLLMAccess for accessing LLM functionality.
    @param source_language_name The name of the source language.
    @param file_type An instance of IFileType for file type-related functionality.
    @param force_full_output A flag to force full output.
    """

    def __init__(self, source_directory: str, target_directory: str, files_to_exclude: List[str],\
                 logger: Logger, content_writer: IContentOut, llm_utils: LLMUtils, \
                 selected_code_request: int, llm_access: AbstractLLMAccess, source_language_name: str, \
                 file_type: FileTypeInterface, force_full_output: bool):
        """
        @brief Initializes the GPT2Unittests instance.

        @param source_directory The directory to read source files from.
        @param target_directory The directory to write output files to.
        @param files_to_exclude A list of files to skip during processing.
        @param logger A logger instance for logging messages.
        @param content_writer An instance of IContentOut for writing output.
        @param llm_utilities An instance of LLMUtils for LLM-related utilities.
        @param selected_code_request The selected code request to use.
        @param llm_access An instance of AbstractLLMAccess for accessing LLM functionality.
        @param source_language_name The name of the source language.
        @param file_type An instance of IFileType for file type-related functionality.
        @param force_full_output A flag to force full output.
        """
        # Renamed variables to have more meaningful names
        self.content_writer = content_writer
        self.logger: Logger = logger
        self.llm_utils: LLMUtils = llm_utils
        self.source_directory: str = source_directory
        self.target_directory: str = re.sub(f'[\\{os.sep}]*$', '', target_directory)
        self.files_to_exclude: List[str] = files_to_exclude
        self.selected_code_request:int = selected_code_request
        self.llm_access: AbstractLLMAccess = llm_access
        self.file_type: FileTypeInterface = file_type
        self.source_language_name: str = source_language_name
        self.force_full_output: bool = force_full_output
        try:
            # Renamed method to have a more meaningful name
            self.process_source_files()
        except Exception as err:                    
            self.logger.warning(f"Caught exception {err=}\n {type(err)=}\n \
                                {traceback.print_exc()}\n Leaving application.")

    def reformat_llm_response(self, response: str) -> str:
        """
        @brief Reformat the response from the LLM: This using a basic state machine considering mark down is returned from the LLM.

        @param response The response from the LLM.

        @return The reformatted response.
        """
        in_code_block: bool = False
        reformatted_response: List = []
        code_block_start: str = f'```{self.file_type.get_destination_language_name()}'
        for line in response.split('\n'):
            if line == '```':
                in_code_block = False
            if not in_code_block:
                if self.force_full_output: 
                    # This line adds a comment character to the start of each line when 
                    # * force_full_output is True
                    # * the MD file does not describe a code block
                    reformatted_response.append(self.file_type.get_comment_characters() + ' ' + line)
            else:
                reformatted_response.append(line)

            if line == code_block_start:
                in_code_block = True

        return '\n'.join(reformatted_response)

    def send_llm_requests_and_expand_output(self, content_to_check: List) -> None:
        """
        @brief Send LLM requests and expand the output.

        @param content_to_check The content to check.
        """
        result = self.llm_access.check(content_to_check, self.source_language_name)

        for response in result:
            self.content_writer.write_content_to_file(
                self.reformat_llm_response(response['response']))

    def _process_file(self, root: str, current_directory: str, file_name: str):
        """
        @brief Process one source file and generate output based on LLM requests.
        @param root source_directory.

        """
        generated_file_extension: str = self.file_type.get_generated_file_extension()

        full_file_name: str = os.path.join(current_directory, file_name)
        if self.files_to_exclude is not None and len(self.files_to_exclude) > 0 and \
            full_file_name in self.files_to_exclude:
            self.logger.info(f'Skipping file {full_file_name} as per request')
            
        _, file_extension = os.path.splitext(full_file_name)
        file_extensions: List = self.file_type.get_source_file_extensions_as_regex()
        if sum([ 1 if re.match(reg_exp_extension, file_extension) else 0 for reg_exp_extension in file_extensions]) > 0:
            from_file: str = os.path.join(root, file_name)
            to_file: str = os.path.join(self.target_directory, full_file_name)
            if generated_file_extension is not None:
                to_file += generated_file_extension
            os.makedirs(os.path.dirname(to_file), exist_ok=True)
            
            self.logger.info(f"Processing {from_file} into {to_file}.")
            self.content_writer.configure_output_file(to_file)
            file_content: List = []
            # CUse 'utf-8' encoding
            with open(from_file, 'r', encoding="utf-8") as file:
                file_content = file.read()

            code_checker: IRequestHandler = CodeCheckerRequestHandler(self.llm_utils, self.selected_code_request, f' ({file_name})')
            self.llm_access.set_request_checker(code_checker)
            self.send_llm_requests_and_expand_output(file_content)

        else:
            self.logger.debug(f"Skipping file {full_file_name} with extension {file_extension}.")
        
    def process_source_files(self):
        """
        @brief Process the source files and generate output based on LLM requests.
        """
        # Renamed method to have a more meaningful name
        directories_to_exclude = [".git"]
        for root, dirs_in_root, files_in_root in os.walk(self.source_directory):
            self.logger.debug(f"root: {root}, dirs_in_root: {dirs_in_root}, files_in_root: {files_in_root}")
            current_directory = re.sub(f'^{self.source_directory}[\\{os.sep}]*', '', root) 
            if sum([ \
                1 if current_directory == directory_to_exclude or current_directory.startswith(directory_to_exclude + os.sep) \
                    else 0 \
                        for directory_to_exclude in directories_to_exclude]) > 0:
                self.logger.debug(f'Skipping directory {current_directory}')
                continue
            self.logger.info(f"Analyzing directory {root}")
            for file_name in files_in_root:
                self._process_file(root, current_directory, file_name)
