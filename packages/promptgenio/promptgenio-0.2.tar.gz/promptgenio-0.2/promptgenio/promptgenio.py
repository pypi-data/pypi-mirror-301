import json
import requests
import logging
from groq import Groq

class PromptGenio:
    def __init__(self, groq_api_key, promptgenio_api_key, tags=None):
        self.client = Groq(api_key=groq_api_key)
        self.logger = logging.getLogger(__name__)
        self.webhook_url = "https://promptgenio.com/api/prompt-logs"
        self.promptgenio_api_key = promptgenio_api_key
        self.tags = tags or {}

    def chat_completion(self, messages, **kwargs):
        try:
            response = self.client.chat.completions.create(messages=messages, **kwargs)
            self._log_success(messages, response)
            return response
        except Exception as e:
            self._log_error(messages, str(e))
            raise

    def _log_success(self, messages, response):
        log_data = {
            "status": "success",
            "messages": messages,
            "response": response.model_dump(),
            "tags": self.tags
        }
        self._send_log(log_data)

    def _log_error(self, messages, error):
        log_data = {
            "status": "error",
            "messages": messages,
            "error": error,
            "tags": self.tags
        }
        self._send_log(log_data)

    def _send_log(self, data):
        try:
            headers = {
                "Authorization": f"Bearer {self.promptgenio_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(self.webhook_url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send log: {str(e)}")

    def add_tag(self, key, value):
        self.tags[key] = value

    def remove_tag(self, key):
        self.tags.pop(key, None)

    def clear_tags(self):
        self.tags.clear()