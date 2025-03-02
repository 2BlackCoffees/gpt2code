"""
Module for abstracting access to Large Language Models (LLMs).

This module provides an abstract base class for accessing LLMs, allowing for different
implementations to be used. It also defines a custom exception for context window exceeded errors.
"""

from abc import abstractmethod, ABC
from typing import List, Dict
from logging import Logger
from domain.ichecker import IRequestHandler
from pprint import pprint

# Custom exception for context window exceeded errors
class ContextWindowExceededError(Exception):
    """
    Custom exception for context window exceeded errors.

    This exception is raised when the context window of an LLM is exceeded.
    """
    pass

# Abstract base class for accessing Large Language Models (LLMs)
class AbstractLLMAccess(ABC):
    """
    Abstract base class for accessing Large Language Models (LLMs).

    This class provides a common interface for accessing LLMs, including setting a checker,
    preparing and sending requests, and checking file content.

    Attributes:
        logger (Logger): The logger instance used for logging.
        checker (IRequests): The checker instance used for getting requests and error information.
        model_name (str): The name of the LLM model being used.
    """

    # Initialize the AbstractLLMAccess instance
    def __init__(self, logger: Logger, model_name: str):
        """
        Initializes the AbstractLLMAccess instance.

        Args:
            logger (Logger): The logger instance used for logging.
            model_name (str): The name of the LLM model being used.
        """
        # Set the logger instance
        self.logger = logger
        # Initialize the checker instance to None
        self.request_handler: IRequestHandler = None
        # Set the model name
        self.model_name = model_name  # "llama3-70b"  # or use gpt-4o-mini, gpt-4o as per access requested

    # Set the checker instance
    def set_request_checker(self, request_handler: IRequestHandler):
        """
        Sets the checker instance used for getting requests and error information.

        Args:
            checker (IRequests): The checker instance to be used.
        """
        self.request_handler = request_handler

    # Prepare and send a request to the LLM
    @abstractmethod
    def prepare_and_send_llm_request(self, request_inputs: List, language_name: str) -> List:
        """
        Prepares and sends a request to the LLM.

        This method is abstract and must be implemented by concrete subclasses.

        Args:
            request_inputs (List): The input data for the request.
            language_name (str): The name of the language being used.

        Returns:
            List: The response from the LLM.
        """
        pass

    @abstractmethod
    def send_plain_request(self, messages: List, request_name: str, temperature: float, top_p: float) -> str:
        """
        Sends a plain request to the LLM.

        This method is abstract and must be implemented by concrete subclasses.

        Args:
            messages (List): The messages to be sent.
            request_name (str): The name of the request.
            temperature (float): The temperature parameter for the LLM.
            top_p (float): The top-p parameter for the LLM.

        Returns:
            str: The response from the LLM.
        """
        # Renamed method to send_plain_llm_request for better clarity
        pass

    def check(self, file_content: str, language_name: str) -> List:
        """
        Checks the file content using the LLM.

        This method uses the checker instance to get the request and error information,
        prepares the request input data, and then calls the prepare_and_send_llm_request method
        to send the request to the LLM.

        Args:
            file_content (str): The content of the file to be checked.
            language_name (str): The name of the language being used.

        Returns:
            List: The response from the LLM.

        Raises:
            Exception: If the checker instance is not properly defined.
        """
        # Renamed method to check_file_content for better clarity
        if self.request_handler is None:
            # Raise an exception if the checker instance is not defined
            raise Exception("Internal error: Checker was not properly defined!") 
        # Get the request from the checker instance
        request: Dict = self.request_handler.retrieve_request_data() 
        # Get the error information from the checker instance
        error_information: str = self.request_handler.get_error_details() 

        # Prepare the request input data
        request_input: Dict = {
            'request_name': request['request_name'],
            'request_llm': request['request'],
            'error_information': error_information,
            'file_content': file_content,
            'temperature': request["temperature"], 
            'top_p': request["top_p"]
        }  

        # Call the prepare_and_send_llm_request method to send the request to the LLM
        return self.prepare_and_send_llm_request([request_input], language_name)
