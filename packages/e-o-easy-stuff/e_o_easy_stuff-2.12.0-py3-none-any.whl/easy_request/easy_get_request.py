import requests
from enum import Enum
import json
from requests import Response


class EasyMethodType(Enum):
    GET = 'GET'
    POST = 'POST'


class EasyGetRequest:
    def __init__(self, base_url: str, method: EasyMethodType = EasyMethodType.GET, headers: dict = None,
                 bearer_token: str = None, full_url: str = None, root_key: str = None):
        self.headers: dict = {
        }
        self.root_key: str = root_key
        self.body: dict | str = None
        self.base_url: str = base_url
        self.full_url: str = full_url
        if headers:
            self.headers.update(headers)
        self.method: EasyMethodType = method

        if bearer_token:
            self.headers['Authorization'] = f'Bearer {bearer_token}'

    def set_method(self, method: EasyMethodType) -> 'EasyGetRequest':
        self.method = method
        return self

    def add_headers(self, headers: dict) -> 'EasyGetRequest':
        self.headers.update(headers)
        return self

    def add_header(self, key: str, value: any) -> 'EasyGetRequest':
        self.headers[key] = value
        return self

    def set_bearer_token(self, token: str) -> 'EasyGetRequest':
        self.headers['Authorization'] = f'Bearer {token}'
        return self

    def set_body(self, body: dict | str) -> 'EasyGetRequest':
        self.body = body
        return self

    def set_base_url(self, base_url: str) -> 'EasyGetRequest':
        self.base_url = base_url
        return self

    def set_url(self, url: str) -> 'EasyGetRequest':
        self.full_url = f"{self.base_url}{url}"
        return self

    def overwrite_full_url(self, full_url: str) -> 'EasyGetRequest':
        self.full_url = full_url
        return self

    def get_request_data(self) -> any:
        response = self.get_request_response()
        response_data = response.json()[self.root_key] if self.root_key else response.json()

        return response_data

    def get_request_response(self) -> Response:
        response: Response = None
        if self.method == EasyMethodType.GET:
            response = self.get_request_with_get_response()
        elif self.method == EasyMethodType.POST:
            response = self.get_request_with_post_response()

        response.raise_for_status()
        if response.status_code == 429:
            raise Exception("Too many requests")

        return response

    def get_request_with_get_response(self) -> Response:
        response = requests.get(self.full_url, headers=self.headers)

        return response

    def get_request_with_post_response(self) -> Response:
        if isinstance(self.body, str):
            json_body = json.dumps(json.loads(self.body))
        else:
            json_body = json.dumps(self.body)

        request_headers = self.headers
        request_headers['Content-Type'] = 'application/json'

        response = requests.post(self.full_url, headers=request_headers, data=json_body)

        return response
