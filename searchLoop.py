import Tools
from authy import Auth # To Authorize Through Authy, Authentically.
import json

while True:
	
	Auth()
	
	result = Tools.admin_search.validateInput(input("search $>"))
	
	print(json.dumps(result,indent=2))
