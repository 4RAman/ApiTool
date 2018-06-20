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
		

		result = Tools.admin_search.validateInput(search)
		print(json.dumps(result,indent=2))
		


# Hides Keyboard interrupt exceptions from ctrl^C - more room for USEFUL DATA 

	except KeyboardInterrupt: 
		
		print(Style.RESET_ALL + "\n\nGoodbye!\n") 
		
		exit()
