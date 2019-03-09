import tkinter as tk # python 3
from tkinter import font  as tkfont

from ClientModel import ClientModel
from ClientView import ClientView, Login

#from Handlers import *

#NOTE: Should handle I/O logic


class ClientController(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.model = ClientModel()
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ClientView, Login): #login
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def run(self):
        self.title("Python Chat Application")
        self.deiconify()
        self.mainloop()

    def close_windows(self):
        self.destroy()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def login_handler(self, server, port, username):
        self.show_frame("ClientView")
        pass



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



