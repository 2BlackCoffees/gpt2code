from abc import abstractmethod, ABC
from typing import List, Dict
import json
from logging import Logger
from domain.ichecker import IRequests
from pprint import pprint

class ContextWindowExceededError(Exception):
    pass

class AbstractLLMAccess(ABC):
    def __init__(self, logger: Logger, model_name: str): 
        self.logger = logger
        self.checker = None
        self.model_name = model_name # "llama3-70b"  # or use gpt-4o-mini, gpt-4o as per access requested

    def set_checker(self, checker: IRequests):
        self.checker = checker

    @abstractmethod
    def _prepare_and_send_request(self, request_inputs: List, language_name: str) -> List:
        """
        """
    @abstractmethod
    def _send_request_plain(self, messages: List, request_name: str, temperature: float, top_p: float) -> str: 
        """
        """

    def check(self, file_content: str, language_name: str) -> List:
        if self.checker is None:
            raise Exception("Internal error: Checker was not properly defined!") 
        request: Dict = self.checker.get_request() 
        error_information: str = self.checker.get_error_information() 

        request_input: Dict = {
            'request_name': request['request_name'],
            'request_llm': request['request'],
            'error_information': error_information,
            'file_content': file_content,
            'temperature': request[ "temperature"], 
            'top_p': request["top_p"]
        }  

        return self._prepare_and_send_request(request_input, language_name)