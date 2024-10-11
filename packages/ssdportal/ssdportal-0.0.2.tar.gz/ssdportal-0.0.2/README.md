# My Package

A simple python package to interact with SSDPortal APIs

## Installation

```bash
pip install ssdportal
```
## API Keys
To get API Keys, create your account [here](https://ssdportal.com)
Go to API and generate a key.
Add it to your environment variables as `ssdportal_key = "xxxxx"`

## Profile
This is used to test authentication and get account balance
```python
from ssdport import Profile

profile = Profile()

test = profile.test() # Returns True or False
print(test)

balance = profile.balance() # Returns integer value
print(balance)
```

## Contacts
Create and Manage Contacts and Contact Lists
```python
from ssdportal import Contact

c = Contact()

allContacts = c.all() # List all contacts. Returns an array

c.add(name='David', phoneNumber='+211920123456', listId = None) # Add new contact
```
## Messaging
Send a message.

```python
from ssdportal import Messaging

message = Messaging()

allContacts = c.sendsms(
    template = 'OTP', # Predefined from the dashboard
    senderId = 'YourBrand', # Set up from the dashboard
    phoneNumber = '+21192123456',
    {
        "otp": "12345"
    } # Attributes object as defined from the template
) # Returns a message ID
```