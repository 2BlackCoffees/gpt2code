from abc import abstractmethod, ABC
from typing import List
import json
from logging import Logger
from domain.ichecker import IRequests

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
    def _prepare_and_send_requests(self, request_inputs: List, language_name: str) -> List:
        """
        """
    @abstractmethod
    def _send_request_plain(self, messages: List, request_name: str) -> str: 
        """
        """

    def check(self, file_content: str, language_name: str) -> List:
        if self.checker is None:
            raise Exception("Internal error: Checker was not properly defined!") 
        slide_review_llm_requests: List = self.checker.get_all_requests() 
        error_information: str = self.checker.get_error_information() 

        request_inputs: List = [{
            'request_name': request['request_name'],
            'request_llm': request['request'],
            'generated_file_extension': request['generated_file_extension'],
            'error_information': error_information,
            'file_content': file_content
        }  for request in slide_review_llm_requests ]

        return self._prepare_and_send_requests(request_inputs, language_name)