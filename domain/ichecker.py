from abc import ABC, abstractmethod
from typing import List
from domain.llm_utils import LLMUtils
class IRequests(ABC):
    def __init__(self, llm_utils: LLMUtils, from_list: List,  error_information: str):
        self.llm_utils = llm_utils
        self.from_list = from_list
        self.error_information = error_information

    @abstractmethod
    def get_all_requests(self) -> List:
        """
        """

    def get_error_information(self) -> str:
        return self.error_information 

class CodeChecker(IRequests):
    def get_all_requests(self) -> List:
        return self.llm_utils.get_all_code_llm_requests(self.from_list)



