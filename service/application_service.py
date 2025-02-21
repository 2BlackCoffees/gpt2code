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
    def __init__(self, from_directory: str, to_directory: str, skip_files: List, language_name: str, simulate_calls_only: bool, \
                 logger: any, llm_utils: LLMUtils, \
                 selected_code_request: int, model_name: str, \
                 force_source_file_types: List, force_destination_file_type: str, force_comment_string: str, force_destination_language_name: str):


        path = Path(from_directory)
        if not path.is_dir():
            logger.error(f'The directory {from_directory} does not seem to be valid (You are in {os.getcwd()}).')
            exit(1)

        information_user: List = []
        if skip_files is not None and len(skip_files) > 0:
            information_user.append(f"Files to be skipped are: {skip_files}")

        content_out: IContentOut = ContentOut()
        for information in information_user:
            logger.info(information)
        
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


        llm_access: AbstractLLMAccess = LLMAccess(logger, model_name) if not simulate_calls_only \
            else LLMAccessSimulateCalls(logger, model_name)

        GPT2Unittests(from_directory, to_directory, skip_files, logger, content_out, llm_utils, selected_code_request, \
                llm_access, language_name, file_type)
   