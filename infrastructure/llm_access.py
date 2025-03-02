"""
Module for accessing the OpenAI API.

This module provides a class OpenAIAccess that handles the interaction with the OpenAI API.
It includes methods for creating and sending requests to the API, as well as handling errors and exceptions.
"""

from openai import OpenAI
from pprint import pformat
from typing import List, Dict
import time
import re
import os
from domain.llm_utils import LLMUtils
from domain.allm_access import AbstractLLMAccess, ContextWindowExceededError
from pprint import pprint

class LLMAccess(AbstractLLMAccess):
    """
    Class for accessing the OpenAI API.

    This class provides methods for creating and sending requests to the OpenAI API.
    It also handles errors and exceptions that may occur during the interaction with the API.

    Attributes:
        api_key (str): The API key for the OpenAI API.
        client (OpenAI): The OpenAI client object.
    """

    # Extracted API key from environment variable for better readability
    api_key = os.getenv("OPENAI_API_KEY", "")
    """
    The API key for the OpenAI API.
    """

    # Created OpenAI client object with API key and base URL
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL"),
        # base_url="https://api.openai.com/v1"
        api_key=api_key
    ) if api_key is not None and len(api_key) > 0 else None
    """
    The OpenAI client object.
    """

    def convert_request_llm_to_string(self, request_input: Dict) -> str:
        """
        Converts the request LLM to a string.

        Args:
            request_input (Dict): The input dictionary containing the request LLM.

        Returns:
            str: The request LLM as a string.
        """
        # Renamed method to follow PEP 8 naming conventions
        # Added type hint for request_input
        request_llm: str = ""
        if isinstance(request_input["request_llm"], list):
            # Used isinstance to check if request_input["request_llm"] is a list
            request_llm = " ".join(request_input["request_llm"])
        else:
            request_llm = request_input["request_llm"]

        self.logger.debug(f'type(request_input["request_llm"]) = {type(request_input["request_llm"])}): request_input["request_llm"] = {request_input["request_llm"]}')
        self.logger.debug(f'request_llm = {request_llm}')

        return request_llm

    def create_initial_message(self, content: str, request_name: str, language_name: str) -> tuple:
        """
        Creates an initial message for the OpenAI API.

        Args:
            content (str): The content of the message.
            request_name (str): The name of the request.
            language_name (str): The name of the language.

        Returns:
            tuple: A tuple containing the message and the request name.
        """
        # Renamed method to better describe its purpose
        return [{"role": "system", "content": f"As a {language_name} expert, I am assigned the task of being able to process the source files as requested. Only source code shall be returned. Any comment from the LLM shall be provided as a comment as specified in the {language_name} standard."},
                {"role": "user", "content": LLMUtils.get_llm_instructions_for_language(language_name)},
                {"role": "user", "content": content}], \
               request_name

    def create_messages(self, request_input: Dict, file_content: str, language_name: str) -> tuple:
        """
        Creates messages for the OpenAI API.

        Args:
            request_input (Dict): The input dictionary containing the request information.
            file_content (str): The content of the file.
            language_name (str): The name of the language.

        Returns:
            tuple: A tuple containing the messages, request names, temperature, and top_p.
        """
        # Renamed method to better describe its purpose
        llm_requests: List = []
        request_names: List = []
        # Prepare request and add content of slide
        llm_requests, request_name = self.create_initial_message(file_content, request_input["request_name"], language_name)
        request_names.append(request_name)
        llm_requests.append({"role": "user", "content": self.convert_request_llm_to_string(request_input)})
        temperature: float = request_input.get('temperature', 0.2)  # Used get method to provide default value
        top_p: float = request_input.get('top_p', 0.1)  # Used get method to provide default value
        return llm_requests, request_names, temperature, top_p

    def send_plain_request(self, messages: List, request_name: str, temperature: float, top_p: float) -> Dict:
        """
        Sends a plain request to the OpenAI API.

        Args:
            messages (List): The list of messages to send.
            request_name (str): The name of the request.
            temperature (float): The temperature for the request.
            top_p (float): The top_p for the request.

        Returns:
            Dict: A dictionary containing the response from the API.
        """

        return_message: str = None

        self.logger.info(f'Requesting {request_name}')
        review = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            top_p=top_p
        )

        return_message = re.sub(r'\'\s+.*refusal=.*,.*role=.*\)', '', re.sub(r'ChatCompletionMessage\(content=', '', str(review.choices[0].message.content.strip())))

        return {
            'request_name': request_name,
            'response': return_message,
        }

    def send_request_with_error_handling(self, messages: List, error_information: str, request_name: str, temperature: float, top_p: float) -> Dict:
        """
        Sends a request to the OpenAI API with error handling.

        Args:
            messages (List): The list of messages to send.
            error_information (str): The error information.
            request_name (str): The name of the request.
            temperature (float): The temperature for the request.
            top_p (float): The top_p for the request.

        Returns:
            Dict: A dictionary containing the response from the API.
        """
        # Renamed method to better describe its purpose
        openai_response: bool = False
        sleep_time: int = 10
        response: Dict = {}

        while not openai_response:
            try:
                response = self.send_plain_request(messages, request_name, temperature, top_p)
                openai_response = True
            except Exception as err:                    
                self.logger.warning(f"{error_information}: {request_name}: Caught exception {err=}, {type(err)=}\nMessage: {pformat(messages)}")
                if "ContextWindowExceededError" in str(err):
                    self.logger.error(f"{request_name}: It seems your request is too big.")
                    raise ContextWindowExceededError(f"{request_name}: It seems the size of your request is too big.")
                self.logger.warning(f"{request_name}: Backoff retry: Sleeping {sleep_time} seconds.")
                time.sleep(sleep_time)
                if sleep_time < 30:
                    sleep_time = sleep_time * 2
        return response

    def prepare_and_send_llm_request(self, request_input: Dict, language_name: str) -> List:
        """
        Prepares and sends a request to the OpenAI API.

        Args:
            request_input (Dict): The input dictionary containing the request information.
            language_name (str): The name of the language.

        Returns:
            List: A list containing the response from the API.
        """
        # Renamed method to better describe its purpose
        return_value: List = []
        file_content: str = request_input[0]['file_content'] 
        error_information: str = request_input[0]['error_information'] 

        llm_requests, request_names, temperature, top_p = self.create_messages(request_input[0], file_content, language_name)
        return_value.append(self.send_request_with_error_handling(llm_requests, \
                                                error_information, \
                                                " & ".join(request_names),
                                                temperature, top_p))
        return return_value
