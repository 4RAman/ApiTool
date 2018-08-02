import json
import os
"""
	general request variables  
	and file operations
"""
_my_userid = "61bf70e7-9899-4388-b6ba-7226b78e4fa0"
_login_auth = "6b7998db49cfe3e3e83aaa5a3a88d4b2d34e92c7;e7cd433a66cf708fdc723fce42e50a0c4088d3e6;1493392689;e574512d-1faf-4687-8bba-05c84d636f87;P100Y"


# Classic Admin API info - Should replace with Dashboard Auth string.

# _classicAuthKey = 'f13bc92b6684d4f527bc68bc2bed1cb25182ca42%3B7422146179df7e585a43be9c48791f01b9a8dd3f%3B1524172517%3B0067300c-5389-4158-abb7-5e701888b098%3BPT30M'
# _classicDeviceId = '0b806560-802d-4cfd-a6f8-9784fdf44e76'
# _classicUserAgent = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
# _classicCookie = {'authorization':classicAuthKey,'userDeviceId':classicDeviceId}


# Persistant memory for various authorization info
_filepath = os.getcwd() + "/"
_auth_file = _filepath + "api.json"
_header_file = _filepath + "headers.json"
_baseURL = "https://api.avantlink.com"

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

