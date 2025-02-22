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
logging_level = logging.INFO

program_name = os.path.basename(sys.argv[0])
logger = logging.getLogger(f'loggername_{program_name}')
logging.basicConfig(encoding='utf-8', level=logging_level, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

llm_utils = LLMUtils(os.getenv("GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS", default=""), logger)
all_code_llm_requests: List = [ idx for idx in range(len(llm_utils.get_all_code_llm_requests())) ]
only_slides = None
selected_code_request = 0
parser.add_argument('--from_directory', type=str, help='Specify the directory to open')
parser.add_argument('--to_directory', type=str, help='Specify the directory where to store generated files')
parser.add_argument('--model_name', type=str, help=f'Specify the name of the LLM model to use. Default is {model_name}')
parser.add_argument('--skip_files', type=csv_, help='Comma separated list of files to be skipped')
parser.add_argument('--language_name', type=str, help='Language name: Java, Python, C++, C, Typescript, Shell, PlantUML, All')
parser.add_argument('--code_request', type=int, help=f'Specify code request to process from the following list: [[ {llm_utils.get_all_code_requests_and_ids_str()} ]], default is {selected_code_request}')
parser.add_argument('--force_source_file_types', type=csv_, help=f'Specify source file types as regexp separated by commas')
parser.add_argument('--force_destination_file_type', type=str, help=f'Specify source file types as regexp separated by commas')
parser.add_argument('--force_comment_string', type=str, help=f'Specify the string to be used for comments')
parser.add_argument('--force_destination_language_name', type=str, help=f'Specify the destination language name')
parser.add_argument('--debug', action="store_true", help='Set logging to debug')
parser.add_argument('--show_temperature_recommendations', action="store_true", help='Display values for various use cases')
parser.add_argument('--simulate_calls_only', action="store_true", help=f'Do not perform the calls to LLM: used for debugging purpose.')
parser.add_argument('--force_top_p', action="store_true", help=f'Increases diversity from various probable outputs in results.')
parser.add_argument('--force_temperature', action="store_true", help=f'Higher temperature increses non sense and creativity while lower yields to focused and predictable results.')
args = parser.parse_args()

if args.show_temperature_recommendations:
    LLMUtils.print_recommended_temperature_and_top_p(logger)
    sys.exit(0)

if args.debug:
    logging_level = logging.DEBUG
if args.code_request:
    selected_code_request = args.code_request
if args.model_name:
    model_name = args.model_name
if args.force_temperature:
    llm_utils.set_temperature(args.force_temperature)
if args.force_top_p:
    llm_utils.set_top_p(args.force_top_p)

if not llm_utils.code_requests_are_valid([selected_code_request]):
    logger.error(f'The selected code {selected_code_request} is not valid. Please use the help to see valid code requests: python {program_name} -h.')
    sys.exit(1)

ApplicationService(args.from_directory, args.to_directory, args.skip_files, args.language_name, args.simulate_calls_only, logger, \
                   llm_utils, selected_code_request,  model_name, args.force_source_file_types, args.force_destination_file_type, \
                   args.force_comment_string, args.force_destination_language_name)