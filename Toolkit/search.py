import AdminSearch.py
from colorama import Style  # So I can shut off ugly colors before exiting.


# Yes, program runs on an infinite loop, get over it.

while True:
	try:
		ApiTerm.TheMenu()

# Hides Keyboard interrupt exceptions from ctrl^C - more room for USEFUL DATA 

	except KeyboardInterrupt: 
		
		print(Style.RESET_ALL + "\n\nGoodbye!\n") 
		
		exit()
