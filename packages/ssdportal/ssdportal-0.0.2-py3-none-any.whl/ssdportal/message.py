from .config import *

class Messaging(SetUp):
    def __init__(self) -> None:
        super().__init__()

    def sendsms(
            self,
            template: str,
            senderId: str,
            phoneNumber: str,
            attr,
    ):
        body = {
            "template": template,
            "senderId": senderId,
            "phoneNumber": phoneNumber,
            "content": attr,
            "schedule": None
        }
        r = requests.post(self.baseUrl+'/messaging', json=body, headers=self.header)
        return r.json()