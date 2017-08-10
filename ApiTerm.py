"""
	The Terminal Interface for the Python Api Tool
"""
import api
from authy import Auth
import Chosen
import json

class TheMenu:
	"""
		A typed menu for terminal API sessions - Type numbers on your keyboard to select Menu Options
	"""
	def __init__(self):
		print("\n=======Request Responsibly!=======\n"
		"Remember to select menu options by number."
		)
		Auth()
		self.mainMenu()
		print("\033[0m") # Set terminal color to default

	def mainMenu(self):
		_selectro = input ("\033[92m"
			"Where to begin?\n"
			"1. User By ID \n"
			"2. Email Search \n"
			"3. Name Search \n"
			"4. Merchant By ID \n"
			"5. Affiliate By ID \n> "
		)
		if _selectro == "1":
			Chosen.user_id = input("Enter User ID: ")
			user_info = api.GetRequest.userByID(Chosen.user_id)
			ShowInfo.userInfo(user_info)

		elif _selectro == "2":
			Chosen.email_address = input("Enter Email Address: ")
			user_info = api.GetRequest.userByEmail(Chosen.email_address)
			ShowInfo.userInfo(user_info)

		elif _selectro == "3":
			Chosen.user_name = input("Enter a first & last name (separated by space plz)")
			user_info = api.GetRequest.userByName(Chosen.user_name)
			ShowInfo.userInfo(user_info)

		elif _selectro == "4":
			Chosen.merchant_id = input("Enter a Merchant ID: ")
			merchant_info = api.GetRequest.merchantById(Chosen.merchant_id)
			ShowInfo.merchantInfo(merchant_info)

		elif _selectro == "5":
			Chosen.publisher_id = input("Enter Affiliate ID: ")
			publisherInfo = api.GetRequest.userByName(Chosen.publisher_id)
			ShowInfo.affiliateInfo(publisher_info)		

		else:
			print("What did you say?")

	def userMenu():
		_selectro = input("\033[92mWhat would you like to do with this?\n"
			"1. View User Accounts\n"
			"2. Delete MFA"
			"3. Update User"
			"2. Go To Main Menu\n> "
		)

		if _selectro == "1":
			account_info = api.GetRequest.userAccounts(Chosen.userID)
			ShowInfo.userAccounts(account_info)

		elif _selectro == "2":
			TheMenu()
		elif _selectro == "3":
			user_id = input("user ID")
			api.PostRequest.updateUser(user_id)			
		else: 
			print("What did you say?")

	def merchantMenu(self):
		_selectro = input("\033[92mWhat would you like to do with this?\n"
			"1. View Users\n"
			"2. Go To Main Menu\n> "
		)
		if _selectro == "1":
			account_info = api.GetRequest.userAccounts(Chosen.userID)
			ShowInfo.userAccounts(account_info)

		elif _selectro == "2":
			TheMenu()

		else: 
			print("What did you say?")

	def affiliateMenu(self):
		_selectro = input("\033[92mWhat would you like to do with this?\n"
			"1. View Users\n"
			"2. Go To Main Menu\n> "
		)
		if _selectro == "1":
			account_info = api.GetRequest.userAccounts(Chosen.user_id)
			ShowInfo.userAccounts(account_info)

		elif _selectro == "2":
			TheMenu()

		else: 
			print("What did you say?")


class ShowInfo:

	def userInfo(req_data):
		if req_data == 0:
			print("no User found by email")
		elif req_data.status_code == 200:
			Chosen.user_id = req_data.json()["user_id"]
			print(json.dumps(req_data.json(), indent=2, separators=(',\033[94m', ':\033[92m ')))
			TheMenu.userMenu()
		else:
			print("Something Went Wrong. Details below")
			print(str(req_data.status_code) + user_info)

	def userAccounts(account_info):
		print("\033[94m") # Set terminal color
		i=0

		print(json.dumps(account_info))
		# for item in account_info:
		# 	print("item: " + str(i))
		# 	i = int(i) + 1

		# 	print(item["entity_group_name"][:-1].title() + ": "
		# 	"" + item["entity_name"] + ""
		# 	"\nNetwork: " + item["entity_network"] + "\n"
		# 	"Classic ID:" + str(item["classic_entity_id"]) + "\n"
		# 	"2.0 ID: " + item["entity_id"]
		# 	)

	def merchantInfo(merchant_info):
		print(merchant_info)

	def affiliateInfo(affiliate_info):
		print(affiliate_info)


while True:
	TheMenu()
	input("\033[93m< press Enter to Restart >\033[0m")