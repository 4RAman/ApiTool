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
from colorama import *
import getpass

class Auth:
	""" 
		Authorization requests
	"""
	def __init__(self):

		self.loginCount = 0  # to keep login requests low
		self.check_auth()


	def check_auth(self):

		""" 
			This pulls authorization values from file and 
			determines if re-auth is needed
		"""
		# DEBUG print ("Auth String: " + ReqVars.headers["Authorization"])

		_parsed = ReqVars.headers["Authorization"].split(";")
		if len(_parsed) < 3:
			_expired = int(time.time()) - 1800
			_parsed = [0, 0, _expired, 0, "PT30M"]
		_exp_time = int(_parsed[2]) + 1800
		_now = int(time.time())
		_time_diff = _exp_time - _now

		# If there is no device ID, we need to get one
		
		if 'user_device_id' not in ReqVars.auth_body.keys():
			print("No Device ID - Reverifying Device")
			self.inital_setup()

		# If there is a device ID, Check if Auth String is expired
		
		else: 
			if _parsed[4] == "PT30M":
				if _exp_time <= (_now + 300):  # add 5 minutes, so auth doesn't interrupt workflow

					print(
						Fore.RED + Style.BRIGHT + 
						"Expired: " + time.strftime('%m/%d %H:%M:%S', time.gmtime(_exp_time)) +
						"\nCurrently: " + time.strftime('%m/%d %H:%M:%S', time.gmtime(_now))
						)
					
					ReqVars.headers["Authorization"] = ReqVars._login_auth

					# print("Auth Expired")
					input("< Push Enter to re-authorize >" + Style.RESET_ALL)

					self.login()
				else: 
					print(Fore.GREEN + Style.BRIGHT + "Authy valid for: " + time.strftime('%H:%M:%S', time.gmtime(_time_diff)) + Style.RESET_ALL)
			else:
				print("something is wrong with your auth string.")
				exit()
		return

	def login(self):

		"""
			Initial Login. Checks Device ID and re-verifies if necessary
		"""

		_auth = ReqVars.auth_body
		_auth["password"] = getpass.getpass("Dashboard Password")
		r = requests.post(ReqVars._baseURL + "/login", headers=ReqVars.headers, data=_auth)
		
		print(json.dumps(r.json(), indent=1))

		if r.status_code == 200:

			ReqVars.headers["Authorization"] = r.json()["authorization"]

			with open(ReqVars._header_file, "w") as file:

				json.dump(ReqVars.headers, file)
				print("\nFinished writing auth to file.")

		elif r.status_code == 401:

			print("unauthorized")
			exit()

		else:

			print("Check your JSON, Status Code:")
			print(r.status_code)
			print(r.content)

		return	

	def setup_device(self):
		
		print("Initial Device Setup")

		_form = {"send_method":"sms"}

		# Place Request

		r = requests.post(ReqVars._baseURL + "/authy/setup/", headers=ReqVars.headers, data=_form)
		print(r.json)

		if r.status_code ==	 200:
			print('Account found - sending verification Code to phone number on file.')
			self.verify_device()

		else:

			print(r.content)
			print(r.status_code)
		
		return


	def verify_device(self):
		
		_vCode = input("Verification Code\n> ")

		# Device Nickname is hardcoded for ease of automation
		_form = {"verification_code": _vCode, "device_nickname": "Support_Python_Requests"}
		r = requests.post(ReqVars._baseURL + "/authy/setup/verify/", headers=ReqVars.headers, data=_form)
		

		print(r.content)
		print("Now run a 'User Devices' request in Postman to get your Device ID\n"
			"GET /users/[your_user_id]/devices"
			"Look for the one labeled Support Python Requests\n"
			"Then append it to your api.json file as device_id ...\n"
			 "I was too lazy to program this part myself")

		return
