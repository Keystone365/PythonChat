import tkinter as tk # python 3
import queue
import threading
import logging

from socket import *
from datetime import datetime

from src.Client.ClientModel import ClientModel
from src.Client.ClientView import ClientWindow
from src.Client.ClientReciever import ClientReciever
from util.utility import *

#from Handlers import *

#NOTE: Controller should handle I/O logic

#set up logger
LOG_FORMAT = "%(levelname)s (%(asctime)s): [%(processName)s] - %(message)s"
logging.basicConfig(filename = "data/ClientChatLog.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger() #root logger

class ClientController():

    OUT_MESSAGE_QUEUE = queue.Queue()
    model = ClientModel()
    bClose = False
    
    

    def __init__(self, *args, **kwargs):
        self.cWindow = ClientWindow(self)
        self.reciever = ClientReciever(self, self.OUT_MESSAGE_QUEUE)

    def run(self):
        self.cWindow.run()


    def Connect(self):
        try:
            bStart = self.reciever.Start("127.0.0.1", 5006)
            return bStart

        except Error as er:
            print("Exception occured with connect")
            raise er  


    def login_handler(self, server, port, username):
        
        #set model info
        self.model.SetLogin(server, port, username)



        bStart = self.Connect()



        if(bStart):
            self.cWindow.show_frame("ClientView")
            #self.reciever.Start(server, port)

        #change frame
        self.PrintMessage()
        

        pass

    def Reply_Handler(self, reply):
        frame = self.cWindow.current_frame()
        frame.Update_Messages("\n" + reply)
        pass

    def Send_Handler(self, message):
        frame = self.cWindow.current_frame()
        sMessage = "\n" + self.model.username + ":" + message
        frame.Update_Messages(sMessage)
        pass


    #Return key press handler
    def Return_Key_Handler(self, event):
        frame = self.cWindow.current_frame()
        frame.Reply_Message()
        pass

    def PrintMessage(self):
        self.Reply_Handler('PythonChat 2019 Client running')
        self.Reply_Handler('Host IP: ' + self.model.clientIP)    
        self.Reply_Handler('Server IP: ' + self.model.serverIP)  
        self.Reply_Handler('Listening on port: ' + str(self.model.clientPort))
        self.Reply_Handler('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.Reply_Handler("Establishing connection....")

    def GetServerPort(self):
        return self.model.serverPort

    def GetServerIP(self):
        return self.model.serverIP

    def close(self):
        if (not self.bClose):
            logger.info("Closing Client ClientController")
            self.reciever.close()
            self.cWindow.close_windows()
            self.bClose = True
            print('\nPythonChat Client cleanup and exit...done!')






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



