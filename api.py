#!/usr/bin/python3
"""
						Makes the API easier to use.
								
"""
#Library Imports
import requests
import sys
import json
import time

#File Imports
import authy
import ReqVars as ReqVars


class Chosen:
	""" 
		Holds dynamic request variables from the 
		initial request the user makes in a session
	"""
	merchantID = 1234
	publisherID = 1234
	userID = 1234
	email_address = 'hello'
	entityID = 1234
	deviceID = "NA"

class TheMenu:
	"""
		Displays a main menu
	"""

	def __init__(self):
		self.main_menu()

	def main_menu(self):
		print("=======Request Responsibly!=======")
		_selectro = input ("\033[92m\
Where to begin?\n\
1. User By ID \n\
2. Email Search \n\
3. Name Search \n>\
\033[0m")

		print (_selectro)
		if _selectro == "1":
			Chosen.userID = input("Enter User ID: ")
			GetRequest.userByID(Chosen.userID)

		elif _selectro == "2":
			Chosen.email_address = input("Enter Email Address: ")
			GetRequest.userByEmail(Chosen.email_address)

		elif _selectro == "3":
			userName = input("Enter a first & last name (separated by a space plz)")
			GetRequest.userByName(userName)

		else:
			print("What did you say?")
		print("===================================")

	def userMenu():
		_selectro = input("\033[92mWhat would you like to do with this?\n\
1. View User Accounts\n\
2. Try Again\n\
3. Go to Main Menu\n\033[0m>")

		if _selectro == "1":
			GetRequest.userAccounts(Chosen.userID)

class GetRequest:
	""" Class for Informational Requests """
	def userByID(userID):

		r = requests.get(ReqVars.base_url + "/users/" + userID, headers=ReqVars.headers)

		if r.status_code == 200:
			show_user_info(r.json())
		else:
			print(r.status_code)
			print(r.content)

	def userByEmail(emailAddress):
		# The info here is not useful to display unless it fails
		#so this just grabs the UUID and runs a userByID request

		r = requests.get(ReqVars.base_url + "/users/search?email_address=" + emailAddress, headers=ReqVars.headers)
		
		if r.status_code == 200:
			for item in r.json()["items"]:
				print ("UUID: " + item["user_id"])
				Chosen.userID = item["user_id"]
			GetRequest.userByID(Chosen.userID)
		else:
			print(r.status_code)
			print(r.content)

	def userByName(fullName):
		_full_name = fullName.split(" ")
		_first_name = _full_name[0]
		_last_name = _full_name[1]
		r = requests.get(ReqVars.base_url + "/users/search?first_name=" + _first_name + "\
&last_name=" + _last_name, headers=ReqVars.headers)
		
		if r.status_code == 200:
			# print(r.status_code)
			# print(r.content)
			for item in r.json()["items"]:
				print ("UUID: " + item["user_id"])
				Chosen.userID = item["user_id"]
			GetRequest.userByID(Chosen.userID)
		else:
			print(r.status_code)
			print(r.content)


	def userAccounts(userID):
		r = requests.get(ReqVars.base_url + "/users/" + Chosen.userID + "/accounts", headers=ReqVars.headers)
		print(r.status_code)
		#print(r.json())
		i = 0
		for item in r.json():
			print("Option: " + str(i))

			print("Group: " + item["entity_group_name"] + "\n\
Name: " + item["entity_name"] + "\nNetwork: " + item["entity_network"] + "\n\
Classic ID:" + str(item["classic_entity_id"]) + "2.0 ID: " + item["entity_id"])
			print()

			print("====")


class show_user_info:
	"""
		Gathers relevant user data into usable variables - and offers some decisions on what to do.	
	"""

	def __init__(self, userInfo):
		merchantID = list()
		publisherID = list()

		userString = userInfo["first_name"] + " " + userInfo["last_name"] + "\n\
UUID: " + userInfo["user_id"] + "\nEmail: " + userInfo["email_address"] + "\n\
Created: " + userInfo["created_at"] + " \nUpdated: " + userInfo["updated_at"] + "\n"
		print("\n\033[94m====USER INFO====")
		print(userString)
		print("=================\033[0m")
		TheMenu.userMenu()

class show_merchant_info:

	def __init__(self, merchantInfo):

		print (merchantInfo)

authy # see authy.py
TheMenu()
