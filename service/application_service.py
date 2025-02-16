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
from infrastructure.file_types import FileTypeCpp, FileTypeJava, FileTypePython, FileTypeShell, FileTypeTypescript


class ApplicationService:
    def __init__(self, from_directory: str, to_directory: str, skip_files: List, language_name: str, simulate_calls_only: bool, \
                 logging_level: logging, llm_utils: LLMUtils, \
                 selected_code_requests: List, model_name: str, multiple_analysis: bool):

        program_name = os.path.basename(sys.argv[0])
        logger = logging.getLogger(f'loggername_{program_name}')

        logging.basicConfig(encoding='utf-8', level=logging_level)

        path = Path(from_directory)
        if not path.is_dir():
            logger.error(f'The directory {from_directory} does not seem to be valid (You are in {os.getcwd()}).')
            exit(1)

        information_user: List = []
        if skip_files is not None and len(skip_files) > 0:
            information_user.append(f"Slides to be skipped are: {skip_files}")

        if len(selected_code_requests) > 0:
            information_user.append(f"LLM artistic Requests to be applied on each slide are: {llm_utils.get_all_code_requests_and_ids_str(selected_code_requests)}")

        content_out: IContentOut = ContentOut()
        for information in information_user:
            logger.info(information)
        
        file_type: IFileType = None
        match language_name.lower():
            case 'c':
                file_type = FileTypeCpp()
            case 'c++':
                file_type = FileTypeCpp()
            case 'java':
                file_type = FileTypeJava()
            case 'python':
                file_type = FileTypePython()
            case 'shell':
                file_type = FileTypeShell()
            case 'typescript':
                file_type = FileTypeTypescript()

        llm_access: AbstractLLMAccess = LLMAccess(logger, model_name) if not simulate_calls_only \
            else LLMAccessSimulateCalls(logger, model_name)

        GPT2Unittests(from_directory, to_directory, skip_files, logger, content_out, llm_utils, selected_code_requests, \
                llm_access, language_name, file_type)
   