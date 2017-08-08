#!/usr/bin/python3
"""
						This file makes all the API request and captures the data.
						I designed it this way so that making a web or desktop app will be easy / separate from a terminal session						
"""
#Library Imports
import requests
import sys
import json
import time

#File Imports
import ReqVars as ReqVars
import Chosen

class GetRequest:
	""" Class for Informational Requests """
	def userByID(userID):

		r = requests.get(ReqVars.base_url + "/users/" + userID, headers=ReqVars.headers)

		if r.status_code == 200:
			return(r.json())
		else:
			print(r.status_code)
			print(r.content)

	def userByEmail(emailAddress): 
		# The info here is not useful to display unless it fails
		#so this just grabs the UUID and runs a more helpful userByID request
		# Although, this can return multiple UUIDs, but I hope the first one is usually the right one

		r = requests.get(ReqVars.base_url + "/users/search?email_address=" + emailAddress, headers=ReqVars.headers)
		
		if r.status_code == 200:
			for item in r.json()["items"]:
				Chosen.userID = item["user_id"]
				userInfo = GetRequest.userByID(Chosen.userID)
			return(userInfo)
		else:
			print(r.status_code)
			print(r.content)

	def userByName(fullName):
		_full_name = fullName.split(" ")
		_first_name = _full_name[0]
		_last_name = _full_name[1]

		r = requests.get(ReqVars.base_url + "/users/search?first_name=" 
		"" + _first_name + ""
		"&last_name=" + _last_name, headers=ReqVars.headers)
		
		if r.status_code == 200:
			for item in r.json()["items"]:
				Chosen.userID = item["user_id"]
				userInfo = GetRequest.userByID(Chosen.userID)
			return(userInfo)
		else:
			print(r.status_code)
			print(r.content)

	def userAccounts(userID):
		r = requests.get(ReqVars.base_url + "/users/" + Chosen.userID + "/accounts", headers=ReqVars.headers)
		print(r.status_code)
		return(r.json())