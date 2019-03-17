
from ServerController import ServerController;
import util.utility as ut

if __name__ == '__main__':
    #ut.cls()

    s = ServerController()

    try:
        s.Run()
    
    except KeyboardInterrupt:
    
        print("\nCTRL-C: Server shutting down")
        print(" - Disconnecting all clients")

    except Error as er:
        print("An error has occured while running the server")
        raise er
        
    finally:
        
        s.close()

        exit (0) # return 0 for successful completion