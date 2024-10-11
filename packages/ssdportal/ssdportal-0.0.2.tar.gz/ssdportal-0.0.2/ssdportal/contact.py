from .config import *

class Contact(SetUp):
    def __init__(self) -> None:
        super().__init__()

    def all(self):
        r = requests.get(self.baseUrl+'/contact', headers=self.header)
        return r.json()
    
    def add(self, name: str, phoneNumber: str, listId: str = None):
        body = {
            "name": name,
            "phoneNumber": phoneNumber
        }
        if listId:
            r = requests.post(self.baseUrl+'/contact/list/'+listId, json=body, headers=self.header)
        else:
            r = requests.post(self.baseUrl+'/contact', json=body, headers=self.header)
        return r.json()

    def update(self, contactId: str, name: str, phoneNumber: str):
        body = {
            "name": name,
            "phoneNumber": phoneNumber
        }
        r = requests.put(self.baseUrl+'/contact/'+contactId, json=body, headers=self.header)
        return r.json()

    def get(self, contactId):
        r = requests.get(self.baseUrl+'/contact/'+contactId, headers=self.header)
        return r.json()

    def addList(self, name: str):
        body = {
            "name": name
        }
        r = requests.post(self.baseUrl+'/contact/list', json=body, headers=self.header)
        return r.json()

    def viewList(self, listId: str):
        r = requests.get(self.baseUrl+'/contact/list/'+listId, headers=self.header)
        return r.json()
