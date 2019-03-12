
from ServerController import ServerController;
import util.utility as ut

if __name__ == '__main__':
    #ut.cls()
    try:
        s = ServerController()
        s.Run()
    
    except KeyboardInterrupt:
    
        print("\nCTRL-C: Server shutting down")
        print(" - Disconnecting all clients")
        
    finally:
        
        #Server.close()

        exit (0) # return 0 for successful completion