from openai import OpenAI
from pprint import pformat
from typing import List, Dict
import time
import re
import os
from domain.llm_utils import LLMUtils
from domain.allm_access import AbstractLLMAccess, ContextWindowExceededError

class LLMAccess(AbstractLLMAccess):

    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL"),
        # base_url="https://api.openai.com/v1"
        # api_key=os.getenv("OPENAI_API_KEY") is default
    )

    def _get_request_llm_to_string(self, request_input: Dict):
        request_llm: str = ""
        if type(request_input["request_llm"]) is list:
            request_llm = " ".join(request_input["request_llm"])
        else:
            request_llm = request_input["request_llm"]

        self.logger.debug(f'type(request_input["request_llm"]) = {type(request_input["request_llm"])}): request_input["request_llm"] = {request_input["request_llm"]}')
        self.logger.debug(f'request_llm = {request_llm}')

        return request_llm
    
    def _create_message(self, content: str, request_name: str, language_name: str):

        return [{"role": "system", "content": f"As a {language_name} expert, I am assigned the task of being able to process the source files as requested. Only source code shall be returned. Any comment from the LLM shall be provided as a comment as specified in the {language_name} standard."},
                {"role": "user", "content": LLMUtils.get_llm_instructions(language_name)},
                {"role": "user", "content": content}], \
               request_name

    def _create_messages(self, request_inputs: List, file_content: str, language_name: str):
        llm_requests: List = []
        request_names: List = []
        if len(request_inputs) > 0:
            # Prepare request and add content of slide
            llm_requests, request_name = self._create_message(file_content, request_inputs[0]["request_name"], language_name)
            request_names.append(request_name)
            for request_input in request_inputs:
                llm_requests.append({"role": "user", "content": self._get_request_llm_to_string(request_input)})
                request_names.append(request_input["request_name"])

        return llm_requests, request_names

    def _send_request_plain(self, messages: List, generated_file_extension: str, request_name: str) -> str: 
        #pprint(self.slide_content)
        #pprint(request)
        return_message: str = None

        self.logger.info(f'Requesting {request_name}')
        review = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        return_message = re.sub(r'\'\s+.*refusal=.*,.*role=.*\)', '', re.sub(r'ChatCompletionMessage\(content=', '', str(review.choices[0].message.content.strip())))

        return {
            'request_name': request_name,
            'response': return_message ,
            'generated_file_extension': generated_file_extension
        }

    def _send_request(self, messages: List, generated_file_extension: str, error_information: str, request_name: str) -> str:
        openai_response: bool = False
        sleep_time: int = 10
        response: Dict = {}

        while not openai_response:
            try:
                response = self._send_request_plain(messages, generated_file_extension, request_name)
                openai_response = True
            except Exception as err:                    
                self.logger.warning(f"{error_information}: {request_name}: Caught exception {err=}, {type(err)=}\nMessage: {pformat(messages)}")
                if "ContextWindowExceededError" in str(err):
                    self.logger.error(f"{request_name}: It seems your request is too big.")
                    raise ContextWindowExceededError(f"{request_name}: It seems your request is too big.")
                self.logger.warning(f"{request_name}: Backoff retry: Sleeping {sleep_time} seconds.")
                time.sleep(sleep_time)
                if sleep_time < 30:
                    sleep_time = sleep_time * 2
        return response
    
    
    def _prepare_and_send_requests(self, request_inputs: List, language_name: str) -> List:
        return_value: List = []
        file_content: str = request_inputs[0]['file_content'] if len(request_inputs) > 0 else None
        error_information: str = request_inputs[0]['error_information'] if len(request_inputs) > 0 else None

        llm_requests, request_names = self._create_messages(request_inputs, file_content, language_name)
        return_value.append(self._send_request(llm_requests, request_inputs[0]['generated_file_extension'], \
                                                error_information, \
                                                " & ".join(request_names)))
        return return_value
    



