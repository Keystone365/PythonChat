
from src.Client.ClientController import ClientController
from datetime import datetime

'''
Author: Andrew Christianson
March 2019
Description:
TCP TKinter Multi Client Python Chat Project. 
'''
  
if __name__ == '__main__':

	print('PythonChat 2019 Client running')
	print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	print("Press CTRL-C to Quit.\n")
	
	c = ClientController()

	try:
		c.run()
	except KeyboardInterrupt:
		print("\nCTRL-C: Server shutting down")
		print(" - Disconnecting all clients")
		pass
	except Error as er:
		print("Error occured in client controller")
		print (er)
	finally:
		c.close()

	exit (0) # return 0 for successful completion
    
    
'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''
