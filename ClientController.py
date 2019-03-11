import tkinter as tk # python 3
import util.utility as ut
import queue

from datetime import datetime

from ClientModel import ClientModel
from ClientView import ClientWindow
from reciever import Reciever

#from Handlers import *

#NOTE: Should handle I/O logic


class ClientController():

    OUT_MESSAGE_QUEUE = queue.Queue()
    IN_MESSAGE_QUEUE = queue.Queue()
    model = ClientModel()
    reciever = Reciever(IN_MESSAGE_QUEUE, OUT_MESSAGE_QUEUE)
    
    

    def __init__(self, *args, **kwargs):
        self.cWindow = ClientWindow(self)

    def run(self):
        self.cWindow.run()

    def login_handler(self, server, port, username):
        
        #set model info
        self.model.loginCommand(server, port, username)
        self.cWindow.show_frame("ClientView")
        #self.reciever.Start(server, port)

        #change frame
        self.PrintMessage()

        pass

    def Reply_Handler(self, message):
        self.cWindow.show_frame("ClientView")
        frame = self.cWindow.frames["ClientView"]
        frame.Update_Messages(message)
        pass

    def Send_Handler(self, message):
        self.cWindow.show_frame("ClientView")
        frame = self.cWindow.frames["ClientView"]
        sMessage = "\n" + self.model.username + ":" + message
        frame.Update_Messages(sMessage)
        pass


    #Return key press handler
    def Return_Key_Handler(self, event):
        frame = self.cWindow.frames["ClientView"]
        frame.Reply_Message()
        pass

    def PrintMessage(self):
        self.Reply_Handler('PythonChat 2019 Client running\n')
        self.Reply_Handler('Host IP: ' + self.model.clientIP)    
        self.Reply_Handler('\nServer IP: ' + self.model.serverIP)  
        self.Reply_Handler('\nListening on port: ' + str(self.model.clientPort))
        self.Reply_Handler('\nStartup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.Reply_Handler("\nEstablishing connection....\nPress CTRL-C to Quit.")

    def GetServerPort(self):
        return self.model.serverPort

    def GetServerIP(self):
        return self.model.serverIP

    def close(self):
        self.cWindow.close_windows()






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



