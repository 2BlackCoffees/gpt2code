"""
@file IRequests.py
@brief This module contains the abstract base class IRequestHandler and its concrete implementation CodeCheckerRequestHandler.
@details It provides a framework for handling requests and retrieving error information.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from domain.llm_utils import LLMUtils
from pprint import pprint, pformat

class IRequestHandler(ABC):
    """
    @class IRequestHandler
    @brief Abstract base class for handling requests.
    @details This class provides a basic structure for handling requests and retrieving error information.
    """
    def __init__(self, llm_utilities: LLMUtils, request_id: int, error_details: str):
        """
        @brief Constructor for the IRequestHandler class.
        @param llm_utilities An instance of LLMUtils.
        @param request_id The request ID.
        @param error_details The error details associated with the request.
        """

        self.llm_utilities = llm_utilities
        self.request_id = request_id
        self.error_details = error_details

    @abstractmethod
    def retrieve_request_data(self) -> Dict:
        """
        @brief Abstract method to retrieve the request data.
        @return A dictionary containing the request information.
        @note This method must be implemented by any concrete subclass of IRequestHandler.
        """

    def get_error_details(self) -> str:
        """
        @brief Method to retrieve the error details associated with the request.
        @return The error details as a string.
        """
        return self.error_details 

class CodeCheckerRequestHandler(IRequestHandler):
    """
    @class CodeCheckerRequestHandler
    @brief Concrete implementation of the IRequestHandler class for code checking requests.
    @details This class provides a specific implementation for handling code checking requests.
    """
    def retrieve_request_data(self) -> Dict:
        """
        @brief Method to retrieve the code checking request data.
        @return A dictionary containing the code checking request information.
        @details This method uses the LLMUtilities instance to retrieve the code checking request information.
        """

        request_data_list: List = self.llm_utilities.get_all_code_llm_requests([self.request_id])

        if request_data_list and len(request_data_list) > 0:
            return request_data_list[0]
        else:
            raise ValueError("No request data found")
