import requests
from requests.exceptions import HTTPError
from .types import ChatRequest, ChatResponse, GenerateResponse, Options

class TextGeneration:
    def __init__(self, instance_id: str, api_key: str):
        self.base_url = f"https://instances.alteryse.cloud/{instance_id}"
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key
        }

    def generate(self, prompt: str, images: Optional[List[str]] = None, options: Optional[Options] = None) -> GenerateResponse:
        payload = {
            'options': options.__dict__ if options else None,
            'images': images,
            'mode': 'generate',
            'stream': False,
            'prompt': prompt
        }
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return GenerateResponse(**response.json())
        except HTTPError as http_err:
            if response.status_code == 503:
                raise Exception(response.json().get('code', 'Service Unavailable'))
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

    def chat(self, messages: List[ChatRequest], options: Optional[Options] = None) -> ChatResponse:
        payload = {
            'options': options.__dict__ if options else None,
            'stream': False,
            'mode': 'chat',
            'messages': messages
        }
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return ChatResponse(**response.json())
        except HTTPError as http_err:
            if response.status_code == 503:
                raise Exception(response.json().get('code', 'Service Unavailable'))
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"An error occurred: {err}")

    @staticmethod
    def parse_chunk(chunk):
        try:
            return chunk  # Assuming chunk is already processed correctly
        except Exception:
            return None
