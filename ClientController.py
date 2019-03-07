import tkinter as tk # python 3

from ClientModel import ClientModel
from ClientView import ClientView, Login

#NOTE: Should handle I/O logic


class ClientController:

    def __init__(self):
        self.root = tk.Tk()
        self.model = ClientModel()
        self.view = Login(self.root, self.model)

    def run(self):
        self.root.title("Python Chat Application")
        self.root.deiconify()
        self.root.mainloop()


        '''try:
        logger.info("# Entering Main")
        #Main()
        
        logger.info("# Exiting Main")
        pass
    except Exception as ex:
        #ut.cls()
        logger.debug("Exception occured" + ex)
        print("Exception occured" + ex)
        #exit(-1)  # return -1 for error during execution
        pass
    except KeyboardInterrupt:
        logger.info("Keyboard interupt occured. Starting shutdown process")
        print("\nCTRL-C: Program shutting down")
    
        pass
    finally:
        #ut.cls()
        
        THREADS_JOIN = True # set flag to force threads to end
        
        for thread in THREADS:
            thread.join()
            THREADS.remove(thread)
        
        print(' - All threads ended')
        logger.info("All threads ended")
        
        CLIENT.close()
        print('\nPythonChat Client cleanup and exit...done!')
        
        logger.info("Closing program")
        exit(0)  # return 0 for successful completion'''



