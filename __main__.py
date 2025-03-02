"""
@file main.py
@brief Main entry point of the application.
"""

import argparse
import os
import sys
import logging
from logging import Logger
from functools import partial
from typing import List
from service.application_service import ApplicationService
from domain.llm_utils import LLMUtils
from typing import Self

class CommandLineArgumentsHandler:
    """
    @brief Program name.
    """
    program_name = os.path.basename(sys.argv[0])  

    """
    @brief Argument parser for the application.
    """
    argument_parser: argparse.ArgumentParser = argparse.ArgumentParser(prog=program_name)  

    """
    @brief Partial function to split a string by comma.
    """
    split_string_by_comma = partial(str.split, sep=',')  

    """
    @brief Default model name.
    """
    default_model_name: str = "llama3-70b"  

    """
    @brief Default logging level.
    """
    default_logging_level = logging.INFO  

    """
    @brief Logger instance.
    """
    logger: Logger = logging.getLogger(f'loggername_{program_name}')  # Create a logger instance with a unique name

    """
    @brief LLM utilities instance.
    """
    llm_utils = LLMUtils(os.getenv("GPT2CODE_EXTERNAL_FILE_CODE_REQUESTS", default=""), logger)  

    """
    @brief List of all code LLM requests.
    """
    all_code_llm_requests: List = [idx for idx in range(len(llm_utils.get_all_code_llm_requests()))]  

    """
    @brief Selected code request.
    """
    selected_code_request_id = 0  

    """
    @brief Force full output flag.
    """
    force_full_output_flag: bool = False  

    """
    @brief Arguments handler.
    """
    args: argparse.Namespace = None

    # Define command line arguments
    def define_command_line_arguments(self) -> Self:
        """
        @brief Define command line arguments for the application.
        """
        self.argument_parser.add_argument('--from_directory', type=str, help='Specify the directory to open')  # Add argument to specify the directory to open
        self.argument_parser.add_argument('--to_directory', type=str, help='Specify the directory where to store generated files')  # Add argument to specify the directory where to store generated files
        self.argument_parser.add_argument('--model_name', type=str, help=f'Specify the name of the LLM model to use. Default is {self.default_model_name}')  # Add argument to specify the name of the LLM model to use
        self.argument_parser.add_argument('--skip_files', type=self.split_string_by_comma, help='Comma separated list of files to be skipped')  # Add argument to specify a comma separated list of files to be skipped
        self.argument_parser.add_argument('--language_name', type=str, help='Language name: Java, Python, C++, C, Typescript, Shell, PlantUML, All')  # Add argument to specify the language name
        self.argument_parser.add_argument('--code_request', type=int, help=f'Specify code request to process from the following list: [[ {self.llm_utils.get_all_code_requests_and_ids_str()} ]], default is {self.selected_code_request_id}')  # Add argument to specify the code request to process
        self.argument_parser.add_argument('--force_source_file_types', type=self.split_string_by_comma, help=f'Specify source file types as regexp separated by commas')  # Add argument to specify source file types as regexp separated by commas
        self.argument_parser.add_argument('--force_destination_file_type', type=str, help=f'Specify source file types as regexp separated by commas')  # Add argument to specify the destination file type as regexp
        self.argument_parser.add_argument('--force_comment_string', type=str, help=f'Specify the string to be used for comments')  # Add argument to specify the string to be used for comments
        self.argument_parser.add_argument('--force_destination_language_name', type=str, help=f'Specify the destination language name')  # Add argument to specify the destination language name
        self.argument_parser.add_argument('--debug', action="store_true", help='Set logging to debug')  # Add argument to set logging to debug
        self.argument_parser.add_argument('--show_temperature_recommendations', action="store_true", help='Display values for various use cases')  # Add argument to display values for various use cases
        self.argument_parser.add_argument('--simulate_calls_only', action="store_true", help=f'Do not perform the calls to LLM: used for debugging purpose.')  # Add argument to simulate calls only
        self.argument_parser.add_argument('--force_top_p', action="store_true", help=f'Increases diversity from various probable outputs in results.')  # Add argument to increase diversity from various probable outputs in results
        self.argument_parser.add_argument('--force_temperature', action="store_true", help=f'Higher temperature increases non sense and creativity while lower yields to focused and predictable results.')  # Add argument to increase non sense and creativity while lower yields to focused and predictable results
        self.argument_parser.add_argument('--force_full_output', action="store_true", help=f'By default remove all what is not source code, this option allows to take into account all output from the LLM.')  # Add argument to take into account all output from the LLM

        self.args = self.argument_parser.parse_args()  # Parse command line arguments
        self.check_temperature_recommendations()

        return self

    # Check if temperature recommendations should be displayed
    def check_temperature_recommendations(self) -> None:
        """
        @brief Check if temperature recommendations should be displayed.
        """
        if self.args.show_temperature_recommendations:
            LLMUtils.print_recommended_temperature_and_top_p(self.logger)  # Print recommended temperature and top p
            sys.exit(0)  # Exit the application

    # Update logging level if debug mode is enabled
    def update_logging_level(self) -> Self:
        """
        @brief Update logging level if debug mode is enabled.
        """
        if self.args is not None and self.args.debug:
            self.default_logging_level = logging.DEBUG  # Update logging level to debug
        
        logging.basicConfig(encoding='utf-8', level=self.default_logging_level, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')  # Set up basic logging configuration

        return self


    # Update selected code request if provided
    def update_selected_code_request(self) -> Self:
        """
        @brief Update selected code request if provided.
        """
        if self.args is not None and self.args.code_request:
            self.selected_code_request_id = self.args.code_request  # Update selected code request
        
        return self

    # Update model name if provided
    def update_model_name(self) -> Self:
        """
        @brief Update model name if provided.
        """
        if self.args.model_name:
            self.default_model_name = args.model_name  # Update model name
        return self

    # Update temperature if provided
    def update_temperature(self) -> Self:
        """
        @brief Update temperature if provided.
        """
        if self.args.force_temperature:
            self.llm_utils.set_temperature(self.args.force_temperature)  # Update temperature
        return self

    # Update top p if provided
    def update_top_p(self) -> Self:
        """
        @brief Update top p if provided.
        """
        if self.args.force_top_p:
            self.llm_utils.set_top_p(self.args.force_top_p)  # Update top p
        return self

    # Update force full output if provided
    def update_force_full_output(self) -> Self:
        """
        @brief Update force full output if provided.
        """
        if self.args.force_full_output:
            self.force_full_output_flag = self.args.force_full_output  # Update force full output
        return self

    # Check if the selected code request is valid
    def check_selected_code_request(self) -> Self:
        """
        @brief Check if the selected code request is valid.
        """
        if not self.llm_utils.code_requests_are_valid([self.selected_code_request_id]):
            self.logger.error(f'The selected code {self.selected_code_request_id} is not valid. Please use the help to see valid code requests: python {self.program_name} -h.')  # Log an error message
            sys.exit(1)  # Exit the application
        return self

    # Create an instance of ApplicationService
    def create_application_service(self) -> ApplicationService:
        """
        @brief Create an instance of ApplicationService.
        """
        args: argparse.Namespace = self.args
        return ApplicationService(args.from_directory, args.to_directory, args.skip_files, \
                                  args.language_name, args.simulate_calls_only, self.logger, \
                                  self.llm_utils, self.selected_code_request_id, \
                                  self.default_model_name, args.force_source_file_types, \
                                  args.force_destination_file_type, args.force_comment_string, \
                                  args.force_destination_language_name, self.force_full_output_flag)

# Main function
def main() -> None:
    """
    @brief Main entry point of the application.
    """
    CommandLineArgumentsHandler() \
        .define_command_line_arguments() \
                .update_logging_level() \
                    .update_selected_code_request() \
                        .update_model_name() \
                            .update_temperature() \
                                .update_top_p() \
                                    .update_force_full_output() \
                                        .check_selected_code_request() \
                                            .create_application_service()

if __name__ == "__main__":
    main()  # Call the main function
