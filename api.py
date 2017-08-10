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
	def userByID(user_id):

		r = requests.get(ReqVars.base_url + "/users/" + user_id, headers=ReqVars.headers)
		return(r)

	def userByEmail(email_address): 
		# The info here is not useful to display unless it fails
		#so this just grabs the UUID and runs a more helpful userByID request
		# Although, this can return multiple UUIDs, but I hope the first one is usually the right one

		r = requests.get(ReqVars.base_url + "/users/search?email_address=" + email_address, headers=ReqVars.headers)
		print(r.status_code)
		if r.status_code == 200:
			if r.json()["total_items"] == 0:
				return(0)
			else:
				for item in r.json()["items"]:
					Chosen.user_id = item["user_id"]
					user_info = GetRequest.userByID(Chosen.user_id)
				return(user_info)
		else:
			return(r) 

	def userByName(full_name):
		_full_name = full_name.split(" ")
		_first_name = _full_name[0]
		_last_name = _full_name[1]

		r = requests.get(ReqVars.base_url + "/users/search?first_name=" 
		"" + _first_name + ""
		"&last_name=" + _last_name, headers=ReqVars.headers)
		
		if r.status_code == 200:
			for item in r.json()["items"]:
				Chosen.user_id = item["user_id"]
				user_info = GetRequest.userByID(Chosen.user_id)
			return(user_info)
		else:
			print(r.status_code)
			print(r.content)

	def affiliateInfo(publisher_id):
		r = requests.get(ReqVars.base_url + "/affiliates/" + publisher_id, headers=ReqVars.headers)

		if r.status_code == 200:
			return(r.json())
		else:
			print(r.status_code)
			print(r.content)

	def merchantInfo(merchant_id):
		r = requests.get(ReqVars.base_url + "/users/" + str(merchant_id), headers=ReqVars.headers)

		if r.status_code == 200:
			return(r.json())
		else:
			print(r.status_code)
			print(r.content)

	def userAccounts(user_id):
		r = requests.get(ReqVars.base_url + "/users/" + str(user_id) + "/accounts", headers=ReqVars.headers)
		print(r.status_code)
		return(r.json())

class PostRequest:

	def deleteMfa(user_id):
		r = requests.get(ReqVars.base_url + "/users/" + str(user_id) + "/accounts", headers=ReqVars.headers)
		print(r.status_code)
		return(r.json())

	def updateUser	(user_id):
		_form_body = dict()

		_email_update = input("update email? (y/n)")
		if _email_update == "y":
			_new_email = input("Enter user's new email address")
			_form_body.append("email_address="+ new_email)
		_name_update = input("update Name? (y/n)")
		if _name_update == "y":
			_new_first_name = input("enter new First name")
			_form_body.append("first_name=" + _new_first_name)
			_new_last_name = input("Enter New Last Name")
			_form_body.append("last_name=" + _new_last_name)
		print(_form_body)


