"""
	The Terminal Interface for the Python Api Tool
"""
import api
from authy import Auth
import Chosen

class TheMenu:
	"""
		A typed menu for terminal API sessions - Type numbers on your keyboard to select Menu Options
	"""
	def __init__(self):
		print("\n=======Request Responsibly!=======\n"
		"Remember to select menu options by number.\n"
		"I don't want to validate strings all day.\n"
		)
		Auth()
		self.main_menu()
		print("\033[0m") # Set terminal color to default

	def main_menu(self):
		_selectro = input ("\033[92m"
			"Where to begin?\n"
			"1. User By ID \n"
			"2. Email Search \n"
			"3. Name Search \n>"
		)

		print (_selectro)
		if _selectro == "1":
			Chosen.userID = input("Enter User ID: ")
			userInfo = api.GetRequest.userByID(Chosen.userID)
			show_user_info(userInfo)

		elif _selectro == "2":
			Chosen.email_address = input("Enter Email Address: ")
			userInfo = api.GetRequest.userByEmail(Chosen.email_address)
			show_user_info(userInfo)

		elif _selectro == "3":
			Chosen.userName = input("Enter a first & last name (separated by space plz)")
			userInfo = api.GetRequest.userByName(Chosen.userName)
			show_user_info(userInfo)

		else:
			print("What did you say?")



class show_user_info:
	"""
		Gathers relevant user data into usable variables - and offers some decisions on what to do.	
	"""
	def __init__(self, userInfo):
		merchantID = list()
		publisherID = list()

		# Eventually save this as a key : val dict, rather than str
		# then print the key + value
		# This will let you fetch specific information later.

		userString = ("\n\033[94m====USER INFO===="
		"" + userInfo["first_name"] + " "
		"" + userInfo["last_name"] + "\n"
		"UUID: " + userInfo["user_id"] + "\n"
		"Email: " + userInfo["email_address"] + "\n"
		"Created: " + userInfo["created_at"] + "\n"
		"Updated: " + userInfo["updated_at"] + "\n"
		"MFA: " + str(userInfo["mfa"]) + "\n"
		"=================\033[0m"
		)
		
		print(userString)

		self.userMenu()

	def userMenu(self):
		_selectro = input("\033[92mWhat would you like to do with this?\n"
			"1. View User Accounts\n"
			"2. Go To Main Menu\n> "
		)

		if _selectro == "1":
			account_info = api.GetRequest.userAccounts(Chosen.userID)
			self.showAccounts(account_info)

		if _selectro == "2":
			TheMenu()

	def showAccounts(self,account_info):
		print("\033[94m") # Set terminal color
		i=0
		for item in account_info:
			print("item: " + str(i))
			i = int(i) + 1

			print(item["entity_group_name"][:-1].title() + ": "
			"" + item["entity_name"] + ""
			"\nNetwork: " + item["entity_network"] + "\n"
			"Classic ID:" + str(item["classic_entity_id"]) + "\n"
			"2.0 ID: " + item["entity_id"]
			)

class show_merchant_info:

	def __init__(self, merchantInfo):

		print (merchantInfo)

while True:
	TheMenu()
	input("\033[93m< press Enter to Restart >\033[0m")