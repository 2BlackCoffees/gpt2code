from typing import Dict, List
import json
from pprint import pprint, pformat
from pathlib import Path
class LLMUtils:
    # In order to get purely Python code, we would need to define specific grammars on the server side:
    https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md 
     
    def __init__(self, external_file_code_requests: str):
        external_code_requests: List = self.__read_json(external_file_code_requests)
        self.external_code_llm_requests = [
            {'request_name': 'Create Unittests', 
                'request': f"For each function please create unittests and ensure 100% code coverage.",
                'generated_file_extension': 'unittests'},
            {'request_name': 'Comments creation', 
                'request': f"For all source code, please ensure a proper documentation of each function following best practices.",
                'generated_file_extension': 'comments'},
            {'request_name': 'Language best practices',
                'request': f"Refactor each method following best practices.",
                'generated_file_extension': 'language-best-practices'},
            {'request_name': 'OOP Best practices',
                'request': f"Refactor all the code following OOP best practices. Please add comments as TODO for all parts where changes need to be done but you are lacking information from the rest of the code.",
                'generated_file_extension': 'oop-best-practices'},

        ]
        self.external_code_llm_requests.extend(external_code_requests)


    def __read_json(self, filename: str):
        path = Path(filename)
        if path.is_file():
            with open(filename) as f:
                return json.load(f)
        return []

    def __get_all_requests(self, request_list: List, from_list: List = None):
        if from_list is None:
            return request_list
        else:
            return [ request_list[idx] for idx in from_list ]
    
    def get_all_code_llm_requests(self, from_list: List = None):
        return self.__get_all_requests(self.external_code_llm_requests, from_list)
    
    def __get_all_code_requests_and_ids(self, request_list: List, from_list: List = None):
        all_requests: List = []
        for idx, llm_request in enumerate(request_list):
            if from_list is None or idx in from_list:
                all_requests.append({'idx': idx, 'llm_request': llm_request['request_name'], 'file_extension': llm_request['generated_file_extension']})
        return all_requests    
    
    def get_all_code_requests_and_ids(self, from_list: List = None):
        return self.__get_all_code_requests_and_ids(self.external_code_llm_requests, from_list)
    
   
    def get_all_code_requests_and_ids_str(self, from_list: List = None, separator: str = ", "):
        all_requests = self.get_all_code_requests_and_ids(from_list)
        return separator.join([f"{req['idx']}: {req['llm_request']}" for req in all_requests])
    
    def get_all_code_extensions(self, from_list: List = None) -> List:
        all_requests = self.get_all_code_requests_and_ids(from_list)
        return [f"{req['file_extension']}" for req in all_requests]
    
    @staticmethod
    def get_list_parameters(parameters):
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
        return f"""[Consider following source code, understand it thoroughly {language_name}]"""