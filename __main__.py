"""
@file main.py
@brief Main entry point of the application.
@author [Your Name]
@date [Today's Date]
"""

import argparse
import os
import sys
import logging
from functools import partial
from typing import List, Dict
from infrastructure.content_out import ContentOut
from service.application_service import ApplicationService
from domain.llm_utils import LLMUtils

"""
@brief Program name.
"""
program_name = os.path.basename(sys.argv[0])

"""
@brief Argument parser for the application.
"""
parser = argparse.ArgumentParser(prog=program_name)

"""
@brief Partial function to split a string by comma.
"""
csv_ = partial(str.split, sep=',')

"""
@brief Default model name.
"""
model_name: str = "llama3-70b"

"""
@brief Default logging level.
"""
logging_level = logging.INFO

"""
@brief Program name.
"""
program_name = os.path.basename(sys.argv[0])

"""
@brief Logger instance.
"""
logger = logging.getLogger(f'loggername_{program_name}')

"""
@brief Basic configuration for the logger.
"""
logging.basicConfig(encoding='utf-8', level=logging_level, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

"""
@brief LLM utilities instance.
"""
llm_utils = LLMUtils(os.getenv("GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS", default=""), logger)

"""
@brief List of all code LLM requests.
"""
all_code_llm_requests: List = [ idx for idx in range(len(llm_utils.get_all_code_llm_requests())) ]

"""
@brief Only slides flag.
"""
only_slides = None

"""
@brief Selected code request.
"""
selected_code_request = 0

"""
@brief Force full output flag.
"""
force_full_output: bool = False

"""
@brief Add argument to specify the directory to open.
"""
parser.add_argument('--from_directory', type=str, help='Specify the directory to open')

"""
@brief Add argument to specify the directory where to store generated files.
"""
parser.add_argument('--to_directory', type=str, help='Specify the directory where to store generated files')

"""
@brief Add argument to specify the name of the LLM model to use.
"""
parser.add_argument('--model_name', type=str, help=f'Specify the name of the LLM model to use. Default is {model_name}')

"""
@brief Add argument to specify a comma separated list of files to be skipped.
"""
parser.add_argument('--skip_files', type=csv_, help='Comma separated list of files to be skipped')

"""
@brief Add argument to specify the language name.
"""
parser.add_argument('--language_name', type=str, help='Language name: Java, Python, C++, C, Typescript, Shell, PlantUML, All')

"""
@brief Add argument to specify the code request to process.
"""
parser.add_argument('--code_request', type=int, help=f'Specify code request to process from the following list: [[ {llm_utils.get_all_code_requests_and_ids_str()} ]], default is {selected_code_request}')

"""
@brief Add argument to specify source file types as regexp separated by commas.
"""
parser.add_argument('--force_source_file_types', type=csv_, help=f'Specify source file types as regexp separated by commas')

"""
@brief Add argument to specify the destination file type as regexp.
"""
parser.add_argument('--force_destination_file_type', type=str, help=f'Specify source file types as regexp separated by commas')

"""
@brief Add argument to specify the string to be used for comments.
"""
parser.add_argument('--force_comment_string', type=str, help=f'Specify the string to be used for comments')

"""
@brief Add argument to specify the destination language name.
"""
parser.add_argument('--force_destination_language_name', type=str, help=f'Specify the destination language name')

"""
@brief Add argument to set logging to debug.
"""
parser.add_argument('--debug', action="store_true", help='Set logging to debug')

"""
@brief Add argument to display values for various use cases.
"""
parser.add_argument('--show_temperature_recommendations', action="store_true", help='Display values for various use cases')

"""
@brief Add argument to simulate calls only.
"""
parser.add_argument('--simulate_calls_only', action="store_true", help=f'Do not perform the calls to LLM: used for debugging purpose.')

"""
@brief Add argument to increase diversity from various probable outputs in results.
"""
parser.add_argument('--force_top_p', action="store_true", help=f'Increases diversity from various probable outputs in results.')

"""
@brief Add argument to increase non sense and creativity while lower yields to focused and predictable results.
"""
parser.add_argument('--force_temperature', action="store_true", help=f'Higher temperature increses non sense and creativity while lower yields to focused and predictable results.')

"""
@brief Add argument to take into account all output from the LLM.
"""
parser.add_argument('--force_full_output', action="store_true", help=f'By defult remove all what is not source code, this option allows to take into account all output from the LLM.')

"""
@brief Parse the arguments.
"""
args = parser.parse_args()

"""
@brief Check if temperature recommendations should be displayed.
"""
if args.show_temperature_recommendations:
    """
    @brief Print recommended temperature and top p.
    """
    LLMUtils.print_recommended_temperature_and_top_p(logger)
    sys.exit(0)

"""
@brief Check if debug mode is enabled.
"""
if args.debug:
    logging_level = logging.DEBUG

"""
@brief Update selected code request if provided.
"""
if args.code_request:
    selected_code_request = args.code_request

"""
@brief Update model name if provided.
"""
if args.model_name:
    model_name = args.model_name

"""
@brief Update temperature if provided.
"""
if args.force_temperature:
    llm_utils.set_temperature(args.force_temperature)

"""
@brief Update top p if provided.
"""
if args.force_top_p:
    llm_utils.set_top_p(args.force_top_p)

"""
@brief Update force full output if provided.
"""
if args.force_full_output:
    force_full_output = args.force_full_output

"""
@brief Check if the selected code request is valid.
"""
if not llm_utils.code_requests_are_valid([selected_code_request]):
    logger.error(f'The selected code {selected_code_request} is not valid. Please use the help to see valid code requests: python {program_name} -h.')
    sys.exit(1)

"""
@brief Create an instance of ApplicationService.
"""
ApplicationService(args.from_directory, args.to_directory, args.skip_files, args.language_name, args.simulate_calls_only, logger, \
                   llm_utils, selected_code_request,  model_name, args.force_source_file_types, args.force_destination_file_type, \
                   args.force_comment_string, args.force_destination_language_name, force_full_output)
