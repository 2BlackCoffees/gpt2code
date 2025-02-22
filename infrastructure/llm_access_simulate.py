"""
Module for simulating LLM access calls.

This module provides a class LLMAccessSimulateCalls that inherits from LLMAccess.
It simulates the sending of requests by returning a predefined response instead of actually sending the request.
"""

from pprint import pformat
from typing import List

from infrastructure.llm_access import LLMAccess

class LLMAccessSimulateCalls(LLMAccess):
    """
    Class for simulating LLM access calls.

    This class provides a method to simulate the sending of requests.
    It returns a dictionary containing the request name and a response message.
    """

    def _send_request_plain(self, messages: List, request_name: str) -> dict:
        """
        Simulates sending a request.

        This method takes a list of messages and a request name as input.
        It returns a dictionary containing the request name and a response message.
        The response message indicates that no calls were performed and includes the original request.

        Args:
            messages (List): A list of messages to be sent.
            request_name (str): The name of the request.

        Returns:
            dict: A dictionary containing the request name and a response message.
        """
        return {
            'request_name': request_name,
            'response': f"# No calls performed\nOriginal request:\n{pformat(messages)}" 
        }
