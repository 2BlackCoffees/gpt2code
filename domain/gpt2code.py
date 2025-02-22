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
from typing import List, Dict
from logging import Logger
from pathlib import Path

from domain.ichecker import IRequests, CodeChecker
from domain.allm_access import AbstractLLMAccess
from domain.llm_utils import LLMUtils
from domain.ifile_type import IFileType
from domain.icontent_out import IContentOut

class GPT2Unittests:
    """
    @class GPT2Unittests
    @brief This class is responsible for processing source files and generating output based on LLM requests.

    @param from_directory The directory to read source files from.
    @param to_directory The directory to write output files to.
    @param files_to_skip A list of files to skip during processing.
    @param logger A logger instance for logging messages.
    @param content_out An instance of IContentOut for writing output.
    @param llm_utils An instance of LLMUtils for LLM-related utilities.
    @param selected_code_request The selected code request to use.
    @param llm_access An instance of AbstractLLMAccess for accessing LLM functionality.
    @param source_language_name The name of the source language.
    @param file_type An instance of IFileType for file type-related functionality.
    @param force_full_output A flag to force full output.
    """

    def __init__(self, from_directory: str, to_directory: str, files_to_skip: List,\
                 logger: Logger, content_out: IContentOut, llm_utils: LLMUtils, \
                 selected_code_request: int, llm_access: AbstractLLMAccess, source_language_name: str, file_type: IFileType, force_full_output: bool):
        """
        @brief Initializes the GPT2Unittests instance.

        @param from_directory The directory to read source files from.
        @param to_directory The directory to write output files to.
        @param files_to_skip A list of files to skip during processing.
        @param logger A logger instance for logging messages.
        @param content_out An instance of IContentOut for writing output.
        @param llm_utils An instance of LLMUtils for LLM-related utilities.
        @param selected_code_request The selected code request to use.
        @param llm_access An instance of AbstractLLMAccess for accessing LLM functionality.
        @param source_language_name The name of the source language.
        @param file_type An instance of IFileType for file type-related functionality.
        @param force_full_output A flag to force full output.
        """
        self.content_out = content_out
        self.logger = logger
        self.llm_utils = llm_utils
        self.from_directory: str = from_directory
        self.to_directory: str = to_directory
        self.files_to_skip = files_to_skip
        self.selected_code_request = selected_code_request
        self.llm_access = llm_access
        self.file_type = file_type
        self.source_language_name: str = source_language_name
        try:
            self.__gpt2code(force_full_output)
        except Exception as err:                    
            self.logger.warning(f"Caught exception {err=}\n {type(err)=}\n {traceback.print_exc()}\n Leaving application.")

    def __reformat_response(self, response: str, force_full_output: bool) -> str:
        """
        @brief Reformat the response from the LLM.

        @param response The response from the LLM.
        @param force_full_output A flag to force full output.

        @return The reformatted response.
        """
        in_code: bool = False
        new_response: List = []
        in_code_str: str = f'```{self.file_type.get_destination_language_name()}'
        for line in response.split('\n'):
            if line == '```':
                in_code = False
            if not in_code:
                if force_full_output: 
                    new_response.append(self.file_type.get_comment_characters() + ' ' + line)
            else:
                new_response.append(line)

            if line == in_code_str:
                in_code = True

        return '\n'.join(new_response)

    def __send_llm_requests_and_expand_output(self, content_to_check: List, force_full_output: bool) -> None:
        """
        @brief Send LLM requests and expand the output.

        @param content_to_check The content to check.
        @param force_full_output A flag to force full output.
        """
        result = self.llm_access.check(content_to_check, self.source_language_name)

        for response in result:
            #self.content_out.write(f"{self.file_type.get_comment_characters()} {response['request_name']}")
            self.content_out.write(self.__reformat_response(response['response'], force_full_output))

    def __gpt2code(self, force_full_output: bool):
        """
        @brief Process the source files and generate output based on LLM requests.

        @param force_full_output A flag to force full output.
        """
        directories_to_skip = [".git"]
        for root, _, files in os.walk(self.from_directory):
            level: int = root.replace(self.from_directory, '').count(os.sep)
            current_dir = root.replace(self.from_directory + os.sep, '')
            if sum([ 1 if current_dir == dir_to_skip or current_dir.startswith(dir_to_skip + os.sep) else 0 for dir_to_skip in directories_to_skip]) > 0:
                self.logger.debug(f'Skipping directory {current_dir}')
                continue
            indent: str = ' ' * 4 * (level)
            information: str = f'Analyzing directory {indent}{os.path.basename(root)}/'
            generated_file_extension: str = self.file_type.get_generated_file_extension()
            self.logger.info(f"Analyzing directory {indent}{os.path.basename(root)}")
            subindent = ' ' * 4 * (level + 1)
            for file_name in files:
                full_file_name: str = f'{current_dir}{os.sep}{file_name}'
                if self.files_to_skip is not None and len(self.files_to_skip) > 0 and full_file_name in self.files_to_skip:
                    self.logger.info(f'Skipping file {full_file_name} as per request')
                    
                _, file_extension = os.path.splitext(full_file_name)
                file_extensions: List = self.file_type.get_source_file_extensions()
                if sum([ 1 if re.match(reg_exp_extension, file_extension) else 0 for reg_exp_extension in file_extensions]) > 0:
                    from_file: str = f'{root}{os.sep}{file_name}'
                    to_file: str = f'{self.to_directory}{os.sep}{full_file_name}'
                    if generated_file_extension is not None:
                        to_file += generated_file_extension
                    os.makedirs(os.path.dirname(to_file), exist_ok=True)
                    
                    self.logger.info(f"Processing {full_file_name} into {to_file}.")
                    self.content_out.set_base_file_name(to_file)
                    #sub_information: str = f'Analyzing file {subindent}{full_file_name}'
                    #self.content_out.write(f'{self.file_type.get_comment_characters()} {information}')
                    #self.content_out.write(f'{self.file_type.get_comment_characters()} {sub_information}')

                    file_content: List = []
                    # with open(from_file, 'rb') as f:
                    #     for line in f:
                    #         file_content.append(line.decode(errors='ignore'))
                    with open(from_file, 'r', encoding="utf-8") as file:
                        file_content = file.read()

                    checker: IRequests = CodeChecker(self.llm_utils, self.selected_code_request, f' ({file_name})')
                    self.llm_access.set_checker(checker)
                    self.__send_llm_requests_and_expand_output(file_content, force_full_output)

                else:
                    self.logger.debug(f"Skipping file {full_file_name} with extension {file_extension}.")
