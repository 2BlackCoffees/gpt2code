import argparse
import os
import sys
import logging
from functools import partial
from typing import List, Dict
from infrastructure.content_out import ContentOut
#from domain.ppt2gpt import PPT2GPT
from service.application_service import ApplicationService
from domain.llm_utils import LLMUtils

program_name = os.path.basename(sys.argv[0])
parser = argparse.ArgumentParser(prog=program_name)
csv_ = partial(str.split, sep=',')

model_name: str = "llama3-70b"



llm_utils = LLMUtils(os.getenv("GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS", default=""))
all_code_llm_requests: List = [ idx for idx in range(len(llm_utils.get_all_code_llm_requests())) ]
only_slides = None

parser.add_argument('--from_directory', type=str, help='Specify the directory to open')
parser.add_argument('--to_directory', type=str, help='Specify the directory where to store generated files')
parser.add_argument('--model_name', type=str, help=f'Specify the name of the LLM model to use. Default is {model_name}')
parser.add_argument('--skip_files', type=csv_, help='Comma separated list of files to be skipped')
parser.add_argument('--language_name', type=str, help='Language name: Java, Python, C++, C, Typescript, Shell')
parser.add_argument('--code_requests', type=csv_, help=f'Specify code requests to process: 1,3-5,7 from the following list: [[ {llm_utils.get_all_code_requests_and_ids_str()} ]], default is {all_code_llm_requests}')
parser.add_argument('--multiple_analysis', action="store_true", help='Apply all changes in one file or create multiple files')
parser.add_argument('--debug', action="store_true", help='Set logging to debug')
parser.add_argument('--simulate_calls_only', action="store_true", help=f'Do not perform the calls to LLM: used for debugging purpose.')
args = parser.parse_args()

logging_level = logging.INFO

if args.debug:
    logging_level = logging.DEBUG
if args.code_requests:
    selected_code_requests = LLMUtils.get_list_parameters(args.code_requests)
if args.model_name:
    model_name = args.model_name

ApplicationService(args.from_directory, args.to_directory, args.skip_files, args.language_name, args.simulate_calls_only, logging_level, \
                   llm_utils, selected_code_requests,  model_name, args.multiple_analysis)