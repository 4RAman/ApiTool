#!/usr/bin/env python3

"""
~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

	Main program execution wrapper.
	
	Puts the whole program in a loop.
	Most of the program can run modularly. 
	This is helpful for more programmatic solutions.
	Can be used for One-Offs.
	Can import major features.

	This is the future.

~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

	DEPENDENCIES


pip3 install requests colorama json time re urllib



Designed by Tony Aman &copy; 2018

"""
import ApiTerm # This is where the main menu is stored.
from colorama import *  # So I can shut off ugly colors before exiting.
from authy import Auth
import Tools
import json

# Yes, program runs on an infinite loop, get over it.

while True:
	try:
		Auth()
		
		search = input(Fore.YELLOW + "search>")
		print(Style.RESET_ALL)
		if search == 'switch':
			selectedClass = input(Fore.CYAN + "select class>")
			selectedMethod = input(Fore.CYAN + "select method>")
			methodToUse = getattr(getattr(Tools, selectedClass), selectedMethod)
			search = input(Fore.YELLOW + methodToUse.__name__ + ">")
			result = methodToUse(search)
		else:
			result = Tools.admin_search.validateInput(search)
			print(json.dumps(result, indent=2))

# Hides Keyboard interrupt exceptions from ctrl^C - more room for USEFUL DATA 

	except KeyboardInterrupt: 
		
		print(Style.RESET_ALL + "\n\nGoodbye!\n") 
		
		exit()
