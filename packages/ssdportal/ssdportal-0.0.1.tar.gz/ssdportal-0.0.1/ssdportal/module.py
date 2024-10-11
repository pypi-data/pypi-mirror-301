from .config import *

class Profile(SetUp):
    def __init__(self) -> None:
        super().__init__()

    def test(self):
        r = requests.get(self.baseUrl, headers=self.header)
        response = r.json()
        if response['status'] == 'success':
            return True
        else:
            return False

    def balance(self) -> int:
        r = requests.get(self.baseUrl+'/user', headers=self.header)
        response = r.json()
        balance = response['data']['balance']
        return balance