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
    def __init__(self, from_directory: str, to_directiry: str, files_to_skip: List,\
                 logger: Logger, content_out: IContentOut, llm_utils: LLMUtils, \
                 additional_requests: List, llm_access: AbstractLLMAccess, language_name: str, file_type: IFileType):
        self.content_out = content_out
        self.logger = logger
        self.llm_utils = llm_utils
        self.from_directory: str = from_directory
        self.to_directory: str = to_directiry
        self.files_to_skip = files_to_skip
        self.additional_requests = additional_requests
        self.llm_access = llm_access
        self.file_type = file_type
        self.language_name: str = language_name
        try:
            self.__gpt2code()
        except Exception as err:                    
            self.logger.warning(f"Caught exception {err=}\n {type(err)=}\n {traceback.print_exc()}\n Leaving application.")

    
    def __send_llm_requests_and_expand_output(self, content_to_check: List) -> None:

            result = self.llm_access.check(content_to_check, self.language_name)

            for response in result:
                self.content_out.write(f"{self.file_type.get_comment_characters()} {response['request_name']}")

                self.content_out.write(response['response'])

    def __gpt2code(self):
        directories_to_skip = [".git"]
        for root, directories, files in os.walk(self.from_directory):
            level: int = root.replace(self.from_directory, '').count(os.sep)
            current_dir = root.replace(self.from_directory + os.sep, '')
            if sum([ 1 if current_dir == dir_to_skip or current_dir.startswith(dir_to_skip + os.sep) else 0 for dir_to_skip in directories_to_skip]) > 0:
                self.logger.debug(f'Skipping directory {current_dir}')
                continue
            indent: str = ' ' * 4 * (level)
            information: str = f'{self.file_type.get_comment_characters()} Analyzing {indent}{os.path.basename(root)}/'
            self.logger.info(information)
            subindent = ' ' * 4 * (level + 1)
            for file_name in files:
                full_file_name: str = f'{current_dir}{os.sep}{file_name}'
                if self.files_to_skip is not None and len(self.files_to_skip) > 0 and full_file_name in self.files_to_skip:
                    self.logger.info(f'Skipping file {full_file_name} as per request')
                _, file_extension = os.path.splitext(full_file_name)
                if re.match(self.file_type.get_file_extension(), file_extension):
                    from_file: str = f'{root}{os.sep}{file_name}'
                    to_file: str = f'{self.to_directory}{os.sep}{full_file_name}'
                    os.makedirs(os.path.dirname(to_file), exist_ok=True)
                    self.logger.info(f"Processing {full_file_name} into {to_file}.")
                    self.content_out.set_base_file_name(to_file)
                    sub_information: str = f'{self.file_type.get_comment_characters()}  Analyzing {subindent}{full_file_name}'
                    self.logger.info(sub_information)
                    self.content_out.write(information)
                    self.content_out.write(sub_information)
                    with open(from_file, 'r', encoding="utf-8") as file:
                        file_content = file.read()

                    checker: IRequests = CodeChecker(self.llm_utils, self.additional_requests, f' ({file_name})')
                    self.llm_access.set_checker(checker)
                    self.__send_llm_requests_and_expand_output(file_content)

                else:
                    self.logger.debug(f"Skipping file {full_file_name} with extension {file_extension}.")



        