import ReqVars
import requests
from urllib.parse import quote_plus
import json
import re
from colorama import *

class admin_search:

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
			result = admin_search.email_search(submission)
			return(result)
		
		# Check for UUID

		elif re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", submission) or submission.isdigit():

			# If UUID, Ask what kind. (eliminates excess requests.)

			groupType = input("Do you know what kind of UUID this is?\n1. Merchants\n2. Affiliates\n3. Users\n4. Not Sure ")

			#
			# Yes, another numeric menu. Sorry!
			#


			if groupType == '1':
				result = get_account.merchant_info(submission)
			elif groupType == '2':
				result = get_account.affiliate_info(submission)
			elif groupType == '3': 
				result = get_account.user_info(submission)
			elif groupType == '4': 
				result = admin_search.id_search(submission)
			else:
				print('You know, \"Not Sure\" was an option. Just throwing that out there.')
				result = admin_search.id_search(submission)
			
			return(result)

		# Decide between User, or Business Name search

		elif re.match(r"^.*[A-z].*$", submission):	
			
			searchType = input("What kind of search is this?\n1. Business Name Search | 2. User Name Search \n")
				
			if searchType == '1':

				# "Account" (business name) Search
				
				result = admin_search.account_search(submission)
				return (result.json())
	

			elif searchType == '2':
				
				# User Search
				if re.match(r"^[A-z]* [A-z]*$", submission):
					result = admin_search.name_search(submission)				
					return (result)

				else:
					return({submission:"Please Enter a Valid First and Last Name"})
			else:
				return({"NOTE FROM THE CREATOR":"NOT A VALID SEARCH"})



		else: 

			print("<(+ +)> Stop trying to hack shit. <(+ +)>")
			exit()


		return("Congratulations, you found a rare, exciting, unhandled error!\n"
				"Please tell an adult how this happened.") 

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
			result = get_account.user_info(userUUID)
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


class get_account:
	"""
		Gather various account information with this class.

	"""
	def user_info(searchID):

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

	def merchant_info(searchID):

		url = ReqVars._baseURL + "/merchants/" + searchID
		r = requests.get(url , headers=ReqVars.headers)

		return(r.json())		
	
	def affiliate_info(searchID):

		url = ReqVars._baseURL + "/affiliates/" + searchID
		r = requests.get(url , headers=ReqVars.headers)

		return(r.json())		

	def user_accounts(permissions):
		
		r = r.json()

		r['user_permissions'] = {}
		i = 1


		for permission in permissions:
			r['user_permissions'] = {'entity_id':permission['entity_id'],'entity group name':permission['entity_group_name'], 'classic_login_id':permission['classic_login_id']}
			
			i = i+1

		return(r)



class reset_2fa:

	"""
	
	1. Ask for User UUID - This ONLY works with UUID
	2. double checks for admin confirmation
	3. Resets 2FA

	"""

	def __init__(self):

		self.userUUID = input("Enter User UUID to reset\n\n")
		self.prepareRequest()

		confirmation = input("Make sure user is thoroughly validated. [Y] to continue, [N] to go back. \n")
		print(json.dumps(self.submitRequest(confirmation), indent=1)) # beautifies json



	def prepareRequest(self):

		""" Fetch user information to ensure you have the right UUID. 
		Please don\'t allow unauthorized access """ 

		url = ReqVars._baseURL + "/users/" + self.userUUID
		r = requests.get(url , headers=ReqVars.headers)
		
		if r.status_code == 200:
			response = r.json()
			del response["user_permissions"]

			print(json.dumps(response, indent=2))


	def submmitReset(self, confirmation):

		""" Submit the request for 2fa Reset and return result """

		if confirmation == "Y":

				url = ReqVars._baseURL + "/authy/setup/" + self.userUUID
				r = requests.get(url , headers=ReqVars.headers)
				return(r.json())
		else:

			# Taunt User
			print("...`1")
		


class copypasta_list:
	"""
	
	List Files In CopyPasta Folder. Okay, not that interesting

	"""
	def __init__(self):
		print(json.dumps(self.counter(), indent=1)) # beautifies json
	
	def counter(self):
		from os import listdir # Cuz I don't want to import this unless it is being used
		from os.path import isfile, join
		
	# Count files and populate dict

		i=0
		onlyfiles = [f for f in listdir("/home/tony/copypasta/") if isfile(join("/home/tony/copypasta/", f))]
		data = {}
		for file in onlyfiles:
			i += 1
			data[i] = file

		return(data)



class outage_estimate:
	""" 
	This will automatically build outage estimates.

	"""
	import time
	def __init__():
		self.questionnaire()
		
	def questionnaire(self): 
		self.merchantId = input("Enter Merchant ID\n>")
		self.outageStart = input ("Enter Outage Start Date (format: 2018-06-09 23:59:59)")
		self.outageEnd = input("Enter Outage End Date (format: 2018-06-09 23:59:59)")
		self.baselineStart = input ("Enter Baseline Start Date (format: 2018-06-09 23:59:59)")
		self.baselineEnd = input("Enter Baseline End Date (format: 2018-06-09 23:59:59)")
		self.today = time.strftime("%I:%M:%S")


	#
	#
	# INSTRUCTIONS UNCLEAR - DICK STUCK IN SPREADSHEET
	#


# class classic_reports:

# 	def mainMenu():
# 		picker = input ("pick your report\n1. Performance Summary | 2. Sales / Commission Detail\n 3. Referral Group Summary ")


# 	def performanceSummary():


# 	def saleDetail():

# 	def oldReport():
# 		""" 
# 		This probably wont work but it's here for reference
# `		"""

# 		merchantId = 11707
# 		reportId = 1
# 		fetchIntervalDays = 7

# 		# IMPORTANT!
# 		# MAKE SURE TO COPY authorization,userDeviceId FROM COOKIES IN YOUR BROWSER. 
# 		# AND GET YOUR USER AGENT

# 		# File to save results in
# 		myfile = open('UA_Sales.csv','w')

# 		# Set request session - this allows headers to be re-used quickly and efficiently. 
# 		session = requests.Session() 	
# 		session.headers.update(userAgent)

# 		urlList = ""
# 		dateStr = startDate
# 		iteration = 0
# 		info = ""
# 		blnHeaderWritten = 0 



# 		# Loop through date ranges
# 		while dateStr < endDate:
# 			iteration = iteration + 1
# 			print("iteration:" + str(iteration))

# 			oldDateStr = dateStr
# 			dateStr += datetime.timedelta(days=fetchIntervalDays) # THIS WILL INCREMENT EVERY 7 DAYS

# 			# Format the request URL	
# 			formattedDateString = "&rsd[F]=" + str(oldDateStr.month) + "&rsd[d]=" + str(oldDateStr.day) + "&rsd[Y]=" + str(oldDateStr.year) + "&red[F]=" + str(dateStr.month) + "&red[d]=" + str(dateStr.day) + "&red[Y]=" + str(dateStr.year)
# 			formattedURL = "https://classic.avantlink.com/admin/reports.php?m=" + str(merchantId) + "r=" + str(reportId) + "&d=" + formattedDateString + "&Download=1&Type=csv"
			
# 			info = session.get(formattedURL, cookies=cookie)

# 			print(info.text)

# 			# Read CSV and add column for Date Range
# 			ugh = csv.DictReader(info.text.split("\n"))
# 			ugh.fieldnames.append('Date Range')

# 			myWriter = csv.DictWriter(myfile, fieldnames=ugh.fieldnames, delimiter=",")

# 			for dictRow in ugh:

# 				# Write Header Row
# 				if blnHeaderWritten == 0:
# 					myWriter.writeheader()
# 					blnHeaderWritten = 1

# 				# Write content rows
# 				dictRow['Date Range'] = str(oldDateStr) + " - " + str(dateStr)
# 				myWriter.writerow(dictRow)
