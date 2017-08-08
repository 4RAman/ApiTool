import json
import os
"""
	general request variables  
	and file operations
"""
_my_userid = "61bf70e7-9899-4388-b6ba-7226b78e4fa0"
_login_auth = "6b7998db49cfe3e3e83aaa5a3a88d4b2d34e92c7;e7cd433a66cf708fdc723fce42e50a0c4088d3e6;1493392689;e574512d-1faf-4687-8bba-05c84d636f87;P100Y"

_filepath = os.getcwd() + "/"
_auth_file = _filepath + "api.json"
_header_file = _filepath + "headers.json"
base_url = "https://api.avantlink.com"
_baseURL = "https://api.avantlink.com"

# Going to work on removing all these and placing them directly 
# in the request functions instead
#
affiliate = _baseURL + "/affiliate"
login = _baseURL + "/login"

sendcode = _baseURL + "/authy/verification/"
verifycode = _baseURL + "/authy/verification/" + _my_userid + "/verify"
devices = _baseURL + "/users/" + _my_userid + "/devices"
setupdevice = _baseURL + "/authy/setup"
verifydevice = _baseURL + "/authy/setup/verify"
usersearch = _baseURL + "/users/search"
#
#
auth_body = dict()
headers = dict()

with open(_auth_file, "r") as file:
	auth_body = json.loads(file.read())

with open(_header_file, "r") as file:
	headers = json.loads(file.read())

def write_auth_file(self):
	with open(_auth_file, "w") as file:
		json.dump(auth_body, file)
		print("\nFinished writing auth file.\n")

