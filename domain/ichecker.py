from abc import ABC, abstractmethod
from typing import List, Dict
from domain.llm_utils import LLMUtils
from pprint import pprint, pformat
class IRequests(ABC):
    def __init__(self, llm_utils: LLMUtils, request: int,  error_information: str):
        self.llm_utils = llm_utils
        self.request = request
        self.error_information = error_information

    @abstractmethod
    def get_request(self) -> Dict:
        """
        """

    def get_error_information(self) -> str:
        return self.error_information 

class CodeChecker(IRequests):
    def get_request(self) -> Dict:
        list_value: List = self.llm_utils.get_all_code_llm_requests([self.request])
        return list_value[0]




