"""
@file LLMUtils.py
@brief This module provides a class LLMUtils to handle external code requests and LLM parameters.
"""

from typing import List, Dict
import json
from pprint import pprint, pformat
from pathlib import Path
from logging import Logger

class LLMUtils:
    """
    @class LLMUtils
    @brief This class handles external code requests and LLM parameters.
    """

    def __init__(self, external_file_code_requests_path: str, logger: Logger):
        """
        @brief Initializes the LLMUtils object.
        @param external_file_code_requests_path The path to the external file containing code requests.
        @param logger The logger object.
        """
        self.logger: Logger = logger
        self.force_temperature: float = None
        self.force_top_p: float = None
        
        external_code_requests: List = self.read_json_file(external_file_code_requests_path)
       
        self.external_code_llm_requests = [
            {   'request_name': 'Create Unittests', 
                'request': f"For each function please create unittests and ensure 100% code coverage related to the code you have. Do not create any unittests for any dependency",
                "temperature": 0.2, 
                "top_p": 0.1,
                "forced_destination_file_type": None,
                "generate_full_output": False

            },
            {   'request_name': 'Comments creation', 
                'request': f"For all source code, please ensure a proper documentation of each function. Keep the initial code exacly as is, only document the whole code in detail following Doxygen best practices.",
                "temperature": 0.3, 
                "top_p": 0.2,
                "generate_full_output": False
            },
            {   'request_name': 'Review comments',
                'request': 'Review the Doxygen documentation against the code semantics and respond as follows:' +
                           '* If the documentation is accurate and well-written, I should reply with "OK".' +
                           '* If there are minor issues or errors that do not significantly impact the understanding of the code, I should reply with "Acceptable".' +''
                           '* If I find serious errors in the documentation, I will provide detailed feedback including suggestions for correction, along with specific references to the method, class, variable, and line numbers involved.',
                "temperature": 0.1, 
                "top_p": 0.2,
                "forced_destination_file_type": "md",
                "generate_full_output": True,
                "force_comment_caracter": ""
            },
            {   'request_name': 'Language best practices',
                'request': f"Refactor each method following language best practices. Ensure that mathods have a proper name. Any change shall be associated with a comment explaining what was done within the code itself. Ensure method and variables have all a meaningfull name.",
                "temperature": 0.2, 
                "top_p": 0.1,
                "generate_full_output": False
            },
            {   'request_name': 'OOP Best practices',
                'request': f"Refactor all the code following OOP best practices. Please add comments as TODO for all parts where changes need to be done but you are lacking information from dependencies.",
                "temperature": 0.2, 
                "top_p": 0.1,
                "generate_full_output": False
            },
            {   'request_name': 'UML Class diagrams reverse engineering',
                'request': f"We need to have the whole file reversed engineer as UML class diagram following plantuml syntax.",
                "temperature": 0.2, 
                "top_p": 0.1,
                "generate_full_output": False
            },

        ]

        self.external_code_llm_requests.extend(external_code_requests)

    def set_default_temperature(self, new_temperature: float) -> None:
        """
        @brief Sets the temperature for all LLM requests.
        @param new_temperature The new temperature value.
        """

        # Loop through each request and update the default temperature
        for request in self.external_code_llm_requests:
            request['temperature'] = new_temperature

    def set_default_top_p(self, new_top_p: float) -> None:
        """
        @brief Sets the top_p value for all LLM requests.
        @param new_top_p The new top_p value.
        """

        # Loop through each request and update the default top_p value
        for request in self.external_code_llm_requests:
            request['top_p'] = new_top_p

    def read_json_file(self, filename: str):
        """
        @brief Reads a JSON file and returns its contents.
        @param filename The path to the JSON file.
        @return The contents of the JSON file.
        """

        file_path = Path(filename)
        if filename is not None and len(filename) > 0:
            if file_path.is_file():
                with open(filename) as file:
                    return_value: List = json.load(file)
                    self.logger.info(f"File {filename} was read.")
                    return return_value
                
            self.logger.warning(f"File {filename} could not be opened.")
        return []

    def get_all_requests(self, request_list: List, filter_request_indices: List = None):
        """
        @brief Returns all requests or a subset of requests based on the filter_request_indices parameter.
        @param request_list The list of requests.
        @param filter_request_indices The list of indices to filter the requests.
        @return The list of requests.
        """
        # Check if filter_request_indices is not None and not empty
        if filter_request_indices is not None and len(filter_request_indices) > 0:
            filtered_requests: List = [ request_list[idx] for idx in filter_request_indices if idx < len(request_list) ]
            if len(filtered_requests) > 0:
                return filtered_requests
        return request_list

    
    def get_all_code_llm_requests(self, filter_request_indices: List = None):
        """
        @brief Returns all code LLM requests or a subset of requests based on the filter_request_indices parameter.
        @param filter_request_indices The list of indices to filter the requests.
        @return The list of code LLM requests.
        """
        return self.get_all_requests(self.external_code_llm_requests, filter_request_indices)
    
    def get_all_code_requests_and_ids(self, filter_request_indices: List = None):
        """
        @brief Returns all code requests and their indices or a subset of requests based on the filter_request_indices parameter.
        @param filter_request_indices The list of indices to filter the requests.
        @return The list of code requests and their indices.
        """

        all_requests: List = []
        for idx, llm_request in enumerate(self.external_code_llm_requests):

            # Check if filter_request_indices is not enabled or if the current index is in filter_request_indices
            if filter_request_indices is None or idx in filter_request_indices:
                all_requests.append({'idx': idx, 'llm_request': llm_request['request_name']})
        return all_requests    
    
    def _get_parameter_value_from_request(self, parameter_name: str, selected_code_request: int):
        """
        @brief Provide the forced file type extension  according to the LLM request and selected language.
        @param selected_code_request The id of the request.
        @return The forced file type for the destination: it will be None unless specifically required from the request.
        """
        for idx, llm_request in enumerate(self.external_code_llm_requests):

            if idx == selected_code_request:
                if parameter_name in llm_request:
                    return llm_request[parameter_name]
                break
        return None    

    def get_generated_file_extension(self, selected_code_request: int):
        """
        @brief Provide the forced file type extension  according to the LLM request and selected language.
        @param selected_code_request The id of the request.
        @return The forced file type for the destination: it will be None unless specifically required from the request.
        """
        return self._get_parameter_value_from_request('generated_file_extension', selected_code_request)
    
    def get_generate_full_output(self, selected_code_request: int) -> bool:
        """
        @brief Informs whether full output is requested.
        @param selected_code_request The id of the request.
        @return This comment should be caught: The forced file type for the destination: it will be None unless specifically required from the request.
        """
        generate_full_output: bool = self._get_parameter_value_from_request('generate_full_output', selected_code_request)
        if generate_full_output is not None:
            if isinstance(generate_full_output, str):
                generate_full_output = generate_full_output.lower() == 'true'
            return generate_full_output
        return False
    
    def get_force_comment_caracter(self, selected_code_request: int) -> str:
        """
        @brief Informs whether full output is requested.
        @param selected_code_request The id of the request.
        @return This comment should be caught: The forced file type for the destination: it will be None unless specifically required from the request.
        """
        force_comment_caracter: bool = self._get_parameter_value_from_request('force_comment_caracter', selected_code_request)
        if force_comment_caracter is not None:
            return force_comment_caracter
        return None
    
    def get_language_name(self, selected_code_request: int) -> str:
        """
        @brief Provide language name specified in JSON.
        @param selected_code_request The id of the request.
        @return Language name defined in json.
        """
        return self._get_parameter_value_from_request('language_name', selected_code_request)
    
    def get_forced_source_file_types(self, selected_code_request: int) -> List:
        """
        @brief Provide language name specified in JSON.
        @param selected_code_request The id of the request.
        @return Language name defined in json.
        """
        forced_source_file_types: str = self._get_parameter_value_from_request('forced_source_file_types', selected_code_request)
        if forced_source_file_types is not None:
            return forced_source_file_types.split(',')
        return None
    
    def get_dict_requestid_request_name(self, selecteted_request: int):
        """
        @brief Returns all code requests and their indices or a subset of requests based on the filter_request_indices parameter.
        @param filter_request_indices The list of indices to filter the requests.
        @return The list of code requests and their indices.
        """

        dict_it_req_name: Dict = {}
        for idx, llm_request in enumerate(self.external_code_llm_requests):

            # Check if filter_request_indices is not enabled or if the current index is in filter_request_indices
            if idx == selecteted_request:
                dict_it_req_name[idx] = llm_request['request_name']
                break
        return dict_it_req_name    
    
    # Renamed method to make it more descriptive
    def code_requests_are_valid(self, filter_request_indices: List):
        """
        @brief Checks if the code requests are valid.
        @param filter_request_indices The list of indices to check.
        @return True if the code requests are valid, False otherwise.
        """

        # Loop through each index and check if it's within the bounds of the requests list
        for code_request in filter_request_indices:
            if code_request < 0 or code_request >= len(self.external_code_llm_requests):
                return False
        return True
    
   
    # Renamed method to make it more descriptive
    def get_all_code_requests_and_ids_str(self, filter_request_indices: List = None, separator: str = ", "):
        """
        @brief Returns all code requests and their indices as a string.
        @param filter_request_indices The list of indices to filter the requests.
        @param separator The separator to use between requests.
        @return The string of code requests and their indices.
        """

        all_requests = self.get_all_code_requests_and_ids(filter_request_indices)
        return separator.join([f"{req['idx']}: {req['llm_request']}" for req in all_requests])
    
    def get_all_code_extensions(self, filter_request_indices: List = None) -> List:
        """
        @brief Returns all code extensions or a subset of extensions based on the filter_request_indices parameter.
        @param filter_request_indices The list of indices to filter the extensions.
        @return The list of code extensions.
        """

        all_requests = self.get_all_code_requests_and_ids(filter_request_indices)

        # Get the file extension for each request
        return [f"{req['file_extension']}" for req in all_requests]
    
    @staticmethod
    # Renamed method to make it more descriptive
    def parse_parameter_list(parameters):
        """
        @brief Returns a list of parameters.
        @param parameters The parameters to convert to a list.
        @return The list of parameters.
        """

        parameter_list: List = []
        for parameter in parameters:
            if '-' in parameter:

                parameter_range = parameter.split('-')
                for parameter_nb in range(int(parameter_range[0]), int(parameter_range[1]) + 1):
                    parameter_list.append(int(parameter_nb))
            else:
                parameter_list.append(int(parameter))
        return parameter_list
    
    @staticmethod
    def get_llm_instructions_for_language(language_name: str) -> str:
        """
        @brief Returns the LLM instructions for a given language.
        @param language_name The name of the language.
        @return The LLM instructions.
        """
        return f"""[Consider following source code, understand it thoroughly {language_name}]"""
    
    @staticmethod
    def print_recommended_temperature_and_top_p_values(logger: any):
        """
        @brief Prints the recommended temperature and top_p values for different use cases.
        @param logger The logger object.
        """
        # Define the data
        data = {
            "Code Generation": {
                "temperature": 0.2, "top_p": 0.1, 
                "description": "Generates code that adheres to established patterns and conventions. Output is more deterministic and focused. Useful for generating syntactically correct code."
            },
            "Creative Writing": {
                "temperature": 0.7, "top_p": 0.8, 
                "description": "Generates creative and diverse text for storytelling. Output is more exploratory and less constrained by patterns."
            },
            "Chatbot Responses": {
                "temperature": 0.5, "top_p": 0.5, 
                "description": "Generates conversational responses that balance coherence and diversity. Output is more natural and engaging."
            },
            "Code Comment Generation": {
                "temperature": 0.3, "top_p": 0.2, 
                "description": "Generates code comments that are more likely to be concise and relevant. Output is more deterministic and adheres to conventions."
            },
            "Data Analysis Scripting": {
                "temperature": 0.2, "top_p": 0.1, 
                "description": "Generates data analysis scripts that are more likely to be correct and efficient. Output is more deterministic and focused."
            },
            "Exploratory Code Writing": {
                "temperature": 0.6, "top_p": 0.7, 
                "description": "Generates code that explores alternative solutions and creative approaches. Output is less constrained by established patterns."
            }
        }

        # Print the headers
        logger.info(f"{'Use Case':^30} | {'Temperature':^10} | {'Top P':^5} | {'Description':^100}")
        logger.info("-" * 150)

        # Print the data
        for use_case, params in data.items():
            logger.info(f"{use_case:^30} | {params['temperature']:^10.1f} | {params['top_p']:^5.1f} | {params['description']:^100}")
