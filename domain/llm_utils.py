"""
@file LLMUtils.py
@brief This module provides a class LLMUtils to handle external code requests and LLM parameters.
@author [Your Name]
@date [Today's Date]
"""

from typing import Dict, List
import json
from pprint import pprint, pformat
from pathlib import Path

class LLMUtils:
    """
    @class LLMUtils
    @brief This class handles external code requests and LLM parameters.
    """

    def __init__(self, external_file_code_requests: str, logger: any):
        """
        @brief Initializes the LLMUtils object.
        @param external_file_code_requests The path to the external file containing code requests.
        @param logger The logger object.
        """
        self.logger = logger
        self.force_temperature: float = None
        self.force_top_p: float = None
        external_code_requests: List = self.__read_json(external_file_code_requests)
        self.external_code_llm_requests = [
            {'request_name': 'Create Unittests', 
                'request': f"For each function please create unittests and ensure 100% code coverage related to the code you have. Do not create any unittests for any dependency",
                "temperature": 0.2, "top_p": 0.1},
            {'request_name': 'Comments creation', 
                'request': f"For all source code, please ensure a proper documentation of each function. Keep the initial code exacly as is, only document the whole code in detail following Doxygen best practices.",
                "temperature": 0.3, "top_p": 0.2},
            {'request_name': 'Language best practices',
                'request': f"Refactor each method following language best practices. Ensure that mathods have a proper name. Any change shall be associated with a comment explaining what was done within the code itself. Ensure method and variables have all a meaningfull name.",
                "temperature": 0.2, "top_p": 0.1},
            {'request_name': 'OOP Best practices',
                'request': f"Refactor all the code following OOP best practices. Please add comments as TODO for all parts where changes need to be done but you are lacking information from dependencies.",
                "temperature": 0.2, "top_p": 0.1},
            {'request_name': 'UML Class diagrams reverse engineering',
                'request': f"We need to have the whole file reversed engineer as UML class diagram following plantuml syntax.",
                "temperature": 0.2, "top_p": 0.1},

        ]
        self.external_code_llm_requests.extend(external_code_requests)

    def set_temperature(self, new_temperature: float) -> None:
        """
        @brief Sets the temperature for all LLM requests.
        @param new_temperature The new temperature value.
        """
        for request in self.external_code_llm_requests:
            request['temperature'] = new_temperature

    def set_top_p(self, new_top_p: float) -> None:
        """
        @brief Sets the top_p value for all LLM requests.
        @param new_top_p The new top_p value.
        """
        for request in self.external_code_llm_requests:
            request['top_p'] = new_top_p

    def __read_json(self, filename: str):
        """
        @brief Reads a JSON file and returns its contents.
        @param filename The path to the JSON file.
        @return The contents of the JSON file.
        """
        path = Path(filename)
        if filename is not None and len(filename) > 0:
            if path.is_file():
                with open(filename) as f:
                    return_value: List = json.load(f)
                    self.logger.info(f"File {filename} was read.")
                    return return_value
                
            self.logger.warning(f"File {filename} could not be opened.")
        return []

    def __get_all_requests(self, request_list: List, from_list: List = None):
        """
        @brief Returns all requests or a subset of requests based on the from_list parameter.
        @param request_list The list of requests.
        @param from_list The list of indices to filter the requests.
        @return The list of requests.
        """
        if from_list is not None and len(from_list) > 0:
            return_list: List = [ request_list[idx] for idx in from_list if idx < len(request_list) ]
            if len(return_list) > 0:
                return return_list
        return request_list

    
    def get_all_code_llm_requests(self, from_list: List = None):
        """
        @brief Returns all code LLM requests or a subset of requests based on the from_list parameter.
        @param from_list The list of indices to filter the requests.
        @return The list of code LLM requests.
        """
        return self.__get_all_requests(self.external_code_llm_requests, from_list)
    
    def __get_all_code_requests_and_ids(self, request_list: List, from_list: List = None):
        """
        @brief Returns all code requests and their indices or a subset of requests based on the from_list parameter.
        @param request_list The list of requests.
        @param from_list The list of indices to filter the requests.
        @return The list of code requests and their indices.
        """
        all_requests: List = []
        for idx, llm_request in enumerate(request_list):
            if from_list is None or idx in from_list:
                all_requests.append({'idx': idx, 'llm_request': llm_request['request_name']})
        return all_requests    
    
    def get_all_code_requests_and_ids(self, from_list: List = None):
        """
        @brief Returns all code requests and their indices or a subset of requests based on the from_list parameter.
        @param from_list The list of indices to filter the requests.
        @return The list of code requests and their indices.
        """
        return self.__get_all_code_requests_and_ids(self.external_code_llm_requests, from_list)
    
    def code_requests_are_valid(self, from_list: List):
        """
        @brief Checks if the code requests are valid.
        @param from_list The list of indices to check.
        @return True if the code requests are valid, False otherwise.
        """
        for code_request in from_list:
            if code_request < 0 or code_request >= len(self.external_code_llm_requests):
                return False
        return True
    
   
    def get_all_code_requests_and_ids_str(self, from_list: List = None, separator: str = ", "):
        """
        @brief Returns all code requests and their indices as a string.
        @param from_list The list of indices to filter the requests.
        @param separator The separator to use between requests.
        @return The string of code requests and their indices.
        """
        all_requests = self.get_all_code_requests_and_ids(from_list)
        return separator.join([f"{req['idx']}: {req['llm_request']}" for req in all_requests])
    
    def get_all_code_extensions(self, from_list: List = None) -> List:
        """
        @brief Returns all code extensions or a subset of extensions based on the from_list parameter.
        @param from_list The list of indices to filter the extensions.
        @return The list of code extensions.
        """
        all_requests = self.get_all_code_requests_and_ids(from_list)
        return [f"{req['file_extension']}" for req in all_requests]
    
    @staticmethod
    def get_list_parameters(parameters):
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
    def get_llm_instructions(language_name: str) -> str:
        """
        @brief Returns the LLM instructions for a given language.
        @param language_name The name of the language.
        @return The LLM instructions.
        """
        return f"""[Consider following source code, understand it thoroughly {language_name}]"""
    
    @staticmethod
    def print_recommended_temperature_and_top_p(logger: any):
        """
        @brief Prints the recommended temperature and top_p values for different use cases.
        @param logger The logger object.
        """
        # Define the data
        data = {
            "Code Generation": {"temperature": 0.2, "top_p": 0.1, "description": "Generates code that adheres to established patterns and conventions. Output is more deterministic and focused. Useful for generating syntactically correct code."},
            "Creative Writing": {"temperature": 0.7, "top_p": 0.8, "description": "Generates creative and diverse text for storytelling. Output is more exploratory and less constrained by patterns."},
            "Chatbot Responses": {"temperature": 0.5, "top_p": 0.5, "description": "Generates conversational responses that balance coherence and diversity. Output is more natural and engaging."},
            "Code Comment Generation": {"temperature": 0.3, "top_p": 0.2, "description": "Generates code comments that are more likely to be concise and relevant. Output is more deterministic and adheres to conventions."},
            "Data Analysis Scripting": {"temperature": 0.2, "top_p": 0.1, "description": "Generates data analysis scripts that are more likely to be correct and efficient. Output is more deterministic and focused."},
            "Exploratory Code Writing": {"temperature": 0.6, "top_p": 0.7, "description": "Generates code that explores alternative solutions and creative approaches. Output is less constrained by established patterns."}
        }

        # Print the headers
        logger.info(f"{'Use Case':^30} | {'Temperature':^10} | {'Top P':^5} | {'Description':^100}")
        logger.info("-" * 150)

        # Print the data
        for use_case, params in data.items():
            logger.info(f"{use_case:^30} | {params['temperature']:^10.1f} | {params['top_p']:^5.1f} | {params['description']:^100}")
