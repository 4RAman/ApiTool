""" 
			Admin Search Module 

* Meant to be used with ApiTerm.py
* Intended for searching effectively across all channels
* multiple results may be returned, 
* broader details will be fetched if only one result is returned
*
* Validate input function will automaticall decide which path to go to.
*
*

	Taman 2018

"""


# response = validateInput(input(Fore.YELLOW + Style.DIM + "search > ")) # Runs user input through validation
# print(Style.RESET_ALL + Fore.WHITE)
# print(json.dumps(response, indent=1))
import ReqVars
import requests
from urllib.parse import quote_plus
import json

from os import listdir, getcwd
from os.path import isfile, join



def __init__(submission):

	validateInput(submission)
	
def validateInput(submission):
	"""
		There are some meat and potatoes here.
		Shouldn't need much future alteration.

	"""
	import re

	# Check for Lack of response
	if re.match(r"^$", submission):
		return({"Y U NO":"."})	

	# Check for Email
	elif re.match(r"^.*@.*\..*", submission):
		result = email_search(submission)
		return(result)
	
	# Check for UUID
	elif re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", submission) or submission.isdigit():

		# If UUID, Ask what kind. (eliminates excess requests.)
		groupType = input("Do you know what kind of UUID this is?\n1. Merchants\n2. Affiliates\n3. Users\n4. Not Sure ")

		if groupType == '1':
			result = get_merchant_info(submission)
		elif groupType == '2':
			result = get_affiliate_info(submission)
		elif groupType == '3': 
			result = get_user_info(submission)
		elif groupType == '4': 
			result = id_search(submission)
		else:
			print('You know, \"Not Sure\" was an option. Just throwing that out there.')
			result = id_search(submission)
		
		return(result)

	# Decide between User, or Business Name search
	elif re.match(r"^.*[A-z].*$", submission):	
		
		searchType = input("What kind of search is this?\n1. Business Name Search | 2. User Name Search \n")
			
		if searchType == '1':

			# "Account" (business name) Search
			result = account_search(submission)
			return (result.json())
		
		elif searchType == '2':
			
			# User Search
			if re.match(r"^[A-z]* [A-z]*$", submission):
				result = name_search(submission)				
				return (result)

# To get here, there were only 2 requests with null results. Validation rulezz
			else:
				return({submission:"Please Enter a Valid First and Last Name"})
		else:
			return({"NOTE FROM THE CREATOR":"NOT A VALID SEARCH"})

	else: 
		print("Stop trying to hack shit.")
		exit()


	return("Congratulations, you found a rare, exciting, never before seen error!")


def name_search(nameString):
	"""
		Search By First and Last Name - specifically separated by a space

	"""

	first, last = nameString.split()

	url = ReqVars._baseURL + "/users/search?first_name=" + first + "&last_name=" + last
	try:
		r = requests.get(url , headers=ReqVars.headers)

	except requests.exceptions.HTTPError as err:
		print(err)
		exit()

	if r.status_code == 200:
		return(r.json())
	else:
		return(200)


def email_search(email):

	""" 
	
	Email Search - needs an @ and a . to qualify as an email address search
	
	"""

	url = ReqVars._baseURL + "/users/search?email_address=" + quote_plus(email)
	r = requests.get(url , headers=ReqVars.headers)
	
	try:
		userUUID = r.json()["items"][0]["user_id"]
		result = get_user_info(userUUID)
	except IndexError:
		
		return({email:"No Email found"})


	return(result)
	

def account_search(searchString):

	url = ReqVars._baseURL + "/login/search/" + searchString + "/any/any/"
	r = requests.get(url , headers=ReqVars.headers)

	return(r)



def id_search(searchID): 
	"""
	
	This module is for if you know the UUID, but do not know what group your searhc belongs to.
	Use sparingly.
	
	"""

	# Merchant Search

	url = ReqVars._baseURL + "/merchants/" + searchID
	r = requests.get(url , headers=ReqVars.headers)

	if r.status_code == 200:
		return(r.json())

	url = ReqVars._baseURL + "/affiliates/" + searchID
	r = requests.get(url , headers=ReqVars.headers)

	if r.status_code == 200:
		return(r.json())


	url = ReqVars._baseURL + "/users/" + searchID
	r = requests.get(url , headers=ReqVars.headers)
	if r.status_code == 200:
		
		r = r.json()

		noPerm = r
		del noPerm['user_permissions']
		
		print(json.dumps(noPerm, indent=1))

		showPermissions = input("Push 1 to show user permissions")
		
		if showPermissions == '1':
			return(r['user_permissions'])
		
		else:
			return
	else:

		return({"ERROR":"UUID NOT FOUND"})

def aff_site_search(searchString):


	url = ReqVars._baseURL + "/affiliates/websites/search/"

	if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", searchString):

		data = {"affiliate_id":searchString}

	elif re.match(r"^.*\..*", searchString):
		
		data = {"website_url":quote_plus(searchString)}

	elif re.match(r"^$"):

		return({"Y":"U NO"})

	r = requests.get(url , headers=ReqVars.headers, data=data)

	return(r.json())


def get_user_info(searchID):

	url = ReqVars._baseURL + "/users/" + searchID

	r = requests.get(url , headers=ReqVars.headers)
	r = r.json()

	noPerm = r
	r = noPerm['user_permissions']

	del noPerm['user_permissions']
	
	print(json.dumps(noPerm, indent=1))

	showPermissions = input("Push 1 to show user permissions")
	
	if showPermissions == '1':
		return(r)
	
	else:
		return


def get_merchant_info(searchID):

	url = ReqVars._baseURL + "/merchants/" + searchID
	r = requests.get(url , headers=ReqVars.headers)

	return(r.json())		


def get_affiliate_info(searchID):

	url = ReqVars._baseURL + "/affiliates/" + searchID
	r = requests.get(url , headers=ReqVars.headers)

	return(r.json())		


def get_user_accounts(permissions):
	
	r = r.json()

	r['user_permissions'] = {}
	i = 1


	for permission in permissions:
		r['user_permissions'] = {'entity_id':permission['entity_id'],'entity group name':permission['entity_group_name'], 'classic_login_id':permission['classic_login_id']}
		
		i = i+1

	return(r)