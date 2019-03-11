
from server import Server;
import util.utility as ut

if __name__ == '__main__':
    ut.cls()
    try:
        port = 1893
        server = Server(port)
        server.Run()
    
    #Error handling
    except Exception as ex:
        print("Exception occured")
        #ut.cls()
        print(ex)
        
    #if user quits program
    except KeyboardInterrupt:
    
        print("\nCTRL-C: Server shutting down")
        print(" - Disconnecting all clients")
        
    finally:
        
        #Server.close()

        exit (0) # return 0 for successful completion