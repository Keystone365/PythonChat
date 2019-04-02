
'''
PEP: 8
Title: Pythonchat Server
Author: Andrew Christianson
Status: Active
Type: Process
Created: March 20, 2019
Post-History:



NOTES: 
Since Model, View and Controller are decoupled, 
each one of the three can be extended, modified 
and replaced without having to rewrite the other two.

'''

from src.Server.ServerController import ServerController;
import util.utility as ut
import traceback

if __name__ == '__main__':
    #ut.cls()

    s = ServerController()

    try:
        s.run() 
    except KeyboardInterrupt: 
        print("\nCTRL-C: Server shutting down")
        print(" - Disconnecting all clients")
    except Exception as e:
        print("An Exception has occured while running the server.")
        print("Exception: " + str(e))
        traceback.print_exc()  
    finally:
        s.close()
        exit (0) # return 0 for successful completion