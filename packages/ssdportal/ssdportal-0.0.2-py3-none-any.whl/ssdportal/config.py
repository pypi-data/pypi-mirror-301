import requests
from dotenv import load_dotenv
import os

load_dotenv()

class SetUp():
    def __init__(self) -> None:
        self.version = 'v1'
        self.baseUrl = 'https://ssdportal.com/api/'+self.version
        self.api_key = os.getenv('ssdportal_key')
        if self.api_key is None:
            raise Exception("API KEY not provided in the environment variables")
        self.header = {
            'Content-Type': 'application/json',
            'apiKey': self.api_key
        }