"""
@file IRequests.py
@brief This module contains the abstract base class IRequests and its concrete implementation CodeChecker.
@details It provides a framework for handling requests and retrieving error information.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from domain.llm_utils import LLMUtils
from pprint import pprint, pformat

class IRequests(ABC):
    """
    @class IRequests
    @brief Abstract base class for handling requests.
    @details This class provides a basic structure for handling requests and retrieving error information.
    """
    def __init__(self, llm_utils: LLMUtils, request: int,  error_information: str):
        """
        @brief Constructor for the IRequests class.
        @param llm_utils An instance of LLMUtils.
        @param request The request ID.
        @param error_information The error information associated with the request.
        """
        self.llm_utils = llm_utils
        self.request = request
        self.error_information = error_information

    @abstractmethod
    def get_request(self) -> Dict:
        """
        @brief Abstract method to retrieve the request.
        @return A dictionary containing the request information.
        @note This method must be implemented by any concrete subclass of IRequests.
        """

    def get_error_information(self) -> str:
        """
        @brief Method to retrieve the error information associated with the request.
        @return The error information as a string.
        """
        return self.error_information 

class CodeChecker(IRequests):
    """
    @class CodeChecker
    @brief Concrete implementation of the IRequests class for code checking.
    @details This class provides a specific implementation for handling code checking requests.
    """
    def get_request(self) -> Dict:
        """
        @brief Method to retrieve the code checking request.
        @return A dictionary containing the code checking request information.
        @details This method uses the LLMUtils instance to retrieve the code checking request information.
        """
        list_value: List = self.llm_utils.get_all_code_llm_requests([self.request])
        return list_value[0]
