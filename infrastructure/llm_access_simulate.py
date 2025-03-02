"""
Module for simulating LLM access calls.

This module provides a class LLMAccessSimulator that inherits from LLMAccess.
It simulates the sending of requests by returning a predefined response instead of actually sending the request.
"""

from pprint import pformat
from typing import List

from infrastructure.llm_access import LLMAccess

class LLMAccessSimulator(LLMAccess):
    """
    Class for simulating LLM access calls.

    This class provides a method to simulate the sending of requests.
    It returns a dictionary containing the request name and a response message.
    """

    def send_plain_request(self, messages: List, request_name: str, temperature: float, top_p: float) -> dict:
        """
        Simulates sending a request.

        This method takes a list of messages and a request type as input.
        It returns a dictionary containing the request type and a response message.
        The response message indicates that no calls were performed and includes the original request.

        Args:
            input_messages (List): A list of messages to be sent.
            request_type (str): The type of the request.

        Returns:
            dict: A dictionary containing the request type and a response message.
        """

        # The response message is a formatted string that includes the original request
        response_message = f"# No calls performed\nOriginal request:\n{pformat(messages)}"

        return {
            'request_name': request_name,  # Changed key name to request_type
            'response': response_message  # This is the response message that will be returned
        }
