import os
from src.logger import Logger

"""
EXAMPLE OF PASSING ENVIRONMENT DYNAMICALLY
"""


class Environment:
    LOCAL = 'local'
    STAGING = 'staging'

    URLS = {
        LOCAL: 'http://localhost:8080',
        STAGING: 'https://reqres.in/'
    }

    def __init__(self):
        self.name = self._get_environment_variable()

    @staticmethod
    def _get_environment_variable() -> str:
        try:
            print("OS environ", os.environ['ENVIRONMENT'])
            return os.environ['ENVIRONMENT']
        except KeyError:
            #Logger.logger.info('No variable passed, using default ENVIRONMENT: staging.')
            return 'staging'

    def base_url(self) -> str:
        return self.URLS[self.name]


ENV = Environment()
