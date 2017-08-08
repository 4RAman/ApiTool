"""
						HOW TO SET THIS UP

		Check if your device is set up via api.json
		Check if authorization is expired via headers.json
		execute login depending on first two checks
		for statuses other than 200 - exit with status code + content

"""

import json
import ReqVars
import time
import requests

class Auth:
	""" 
		Authorization requests
	"""
	def __init__(self):

		self.loginCount = 0 # to keep login requests low
		self.check_auth()

	def check_auth(self):
		""" 
			This pulls authorization values from file
		"""
		print ("===Authorization===========")
		#print ("Auth String: " + ReqVars.headers["Authorization"])

		_parsed = ReqVars.headers["Authorization"].split(";")
		_exp_time = int(_parsed[2]) + 1800
		_now = int(time.time())


		print("Expires: " + time.strftime('%m/%d %H:%M:%S', time.gmtime(_exp_time)))
		print("Currently: " + time.strftime('%m/%d %H:%M:%S', time.gmtime(_now)))

		if 'user_device_id' not in ReqVars.auth_body.keys():
			print("No Device ID - Reverifying Device")
			self.setup_device()
		if _parsed[4] == "PT100Y":
			print("need some additional programming for initial setup")
			# Should go to login then set up device???

		if _exp_time <= _now:
			if _parsed[4] == "PT30M":
				ReqVars.headers["Authorization"] = ReqVars._login_auth
				print("Auth Expired")
				self.login()
		else:
			print("Authy still valid - Skipping re-authorization\n")

	def login(self):
		"""
			Initial Login. Checks Device ID and re-verifies if necessary
		"""
		self.loginCount += 1 # of login attempts per session

		if self.loginCount == 3:
			print("Too many login authentications this session. Goodbye")
			exit()

		r = requests.post(ReqVars.login, headers=ReqVars.headers, data=ReqVars.auth_body)

		print(r.content)

		if r.status_code == 200:
			ReqVars.headers["Authorization"] = r.json()["authorization"]
			with open(ReqVars._header_file, "w") as file:
				json.dump(ReqVars.headers, file)
				print("\nFinished writing auth to file.\n")

		elif r.status_code == 401:
			print("unauthorized")
			exit()
		else:
			print("Check your JSON, Status Code:")
			print(r.status_code)
			print(r.content)

	def setup_device(self):
		print("Initial Device Setup")
		_sendMethod = "sms"
		_phoneNumber = input("Enter phone number for Device Verification\n> ")
		_countryCode = 1
		

		_form = {"send_method":_sendMethod, "country_code":_countryCode, "phone_number":_phoneNumber}

		r = requests.post(ReqVars.setupdevice, headers=ReqVars.headers, data=_form)
		print(r.json)

		if r.status_code ==	 200:
			self.verify_device()
		else:
			print(r.content)
			print(r.status_code)

	def verify_device(self):
		_vCode = input("Verification Code\n> ")

		# Device Nickname is hardcoded for ease of automation
		_form = {"verification_code": _vCode, "device_nickname": "Support_Python_Requests"}
		r = requests.post(ReqVars.verifydevice, headers=ReqVars.headers, data=_form)
		print(r.content)
		print("Now run a request in Postman to get your Device ID\n\
			Look for the one labeled Support Python Requests\n\
			Then append it to your api.json file under device_id...\n\
			 I was too lazy to program this part myself")

Auth()