import requests
from src.logger import Logger
from utils.environment import ENV


class Request:
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None, params: dict = None):
        return Request._send(url, data, headers, cookies, 'POST', params)

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None, params: dict = None):
        return Request._send(url, data, headers, cookies, 'GET', params)

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None, params: dict = None):
        return Request._send(url, data, headers, cookies, 'PUT', params)

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str, params: dict):
        url = f"{ENV.base_url()}{url}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        if params is None:
            params = {}

        additional_header = {'X-THIS_IS_TEST': 'True'}
        headers.update(additional_header)

        Logger.get_instance().add_request(url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, data=data, headers=headers, cookies=cookies, params=params)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f'Bad HTTP method "{method}" was received')

        Logger.get_instance().add_response(response)
        return response
