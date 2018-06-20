"""
	The Terminal Interface for the Python Api Tool
"""

# Program imports
from authy import Auth # To Authorize Through Authy, Authentically.
import Tools # This is where the tools are kept.

# 3rd party imports (A.K.A Dependencies )
from colorama import * #NowInTechnaColor
import json
import sys
import os
import Toolkit


class conf:
	redo = '0'
	selectro = 'x'

class TheMenu:

	"""
		A typed menu for terminal API sessions - Type numbers on your keyboard to select Menu Options
	"""

	def __init__(self):
		
		Auth()
		self.mainMenu()
		conf.redo = input(Fore.YELLOW + "< [R/r] to Restart [Enter] to Continue >\n" + Fore.RESET )


	def mainMenu(self): 
		"""
		The Main Menu does exactly what it sounds like.
		Displays a menu, and lets a user make a selection

		Add new menu items to the list below - add new Tools to Tools.py 
		If new Tools are added, please follow the Class structure in Tools.py

		"""

		menuItems = [

			{
		
			'name':'Admin Search',
			'funct':'Tools.admin_search.validateInput(input("search >"))'
		
			},{
		
			'name':'CopyPasta List',
			'funct':'Tools.copypasta_list()'
		
			},{
		
			'name':'Help',
			'funct':'help("modules")'
		
			}
		]

		# Passes through previous value, if user has chosen to restart

		if conf.redo == 'r' or conf.redo == "R": 
			print("Restarting Menu Item: " + conf.selectro)

		# Prints the menu

		else:
			selectro = conf.selectro
			print (
			Fore.GREEN + 
			'=== MAIN MENU ==================\n')

			for key,val in enumerate(menuItems):
				print(str(key) + " : " + val['name'])

			print('\n================================='
			+ Fore.WHITE + "\n")

		# Get user selection and passes to select_o_matic

		selectro = input("")
		self.select_o_matic(selectro, menuItems)


	def select_o_matic(self, selectro, menuItems):
		"""	
		
		The select_o_matic function is perfect for parsing a user's input 
		and running the function stored in the menuItems variable

		If the option is not in the dict, it's already handled. 
		The menu will restart and everything will be fine.
		
		Try it out today for a selector switch with capabilities like no other,
		and watch the beauty of plug & play menu items.
		
		"""
		if selectro.isdigit():
			conf.selectro == selectro
			if int(selectro) < len(menuItems):

				# eval is what runs the function from the menuItems dict

				response = eval(menuItems[int(selectro)]['funct'])

				print(json.dumps(response,indent=1))
			else:
				print(str(selectro) + ' is not yet an option')

		# Other options
		elif selectro.lower() == "x":
			exit()
		
		elif selectro.lower() == "r":
			print("retrying")
			exit()

		else:
			print(Fore.RED + "That\'s not an option... Yet." + Fore.RESET)