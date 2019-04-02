
import queue
import threading
import logging
import tkinter as tk # python 3

from socket import *
from datetime import datetime
from util.utility import *

from src.Client.ClientModel import ClientModel
from src.Client.ClientView import ClientWindow
from src.Client.ClientReciever import ClientReciever

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
    clientmodel = ClientModel()
    b_close = False

    def __init__(self, *args, **kwargs):
        self.c_window = ClientWindow(self)
        self.reciever = ClientReciever(self, self.OUT_MESSAGE_QUEUE)

    def run(self):
        self.c_window.run()

    def login_handler(self, server, port, username):

        b_start = self.reciever.start(server, port)

        if(b_start):
            #set clientmodel info
            self.clientmodel.set_login(server, port, username)
            self.c_window.show_frame("ClientView")
            self.printmessage()
        else:
            self.c_window.error_box("Connection Error", "Connection failed. Please try again.")
        pass

    def reply_handler(self, reply):
        frame = self.c_window.current_frame()
        frame.update_messages("\n" + reply)
        pass

    def send_handler(self, message):
        frame = self.c_window.current_frame()
        s_message = "\n" + self.clientmodel.username + ":" + message
        frame.update_messages(s_message)
        pass

    #Return key press handler
    def return_key_handler(self, event):
        frame = self.c_window.current_frame()
        frame.reply_message()
        pass

    def printmessage(self):
        self.reply_handler('PythonChat 2019 Client running')
        self.reply_handler('Host IP: ' + self.clientmodel.clientIP)    
        self.reply_handler('Server IP: ' + self.clientmodel.serverIP)  
        self.reply_handler('Listening on port: ' + str(self.clientmodel.clientPort))
        self.reply_handler('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.reply_handler("Establishing connection....")

    def get_server_port(self):
        return self.clientmodel.server_port

    def get_server_ip(self):
        return self.clientmodel.server_ip

    def close(self):
        if (not self.b_close):
            logger.info("Closing Client ClientController")
            self.reciever.close()
            self.c_window.close_windows()
            self.b_close = True
            print('\nPythonChat Client cleanup and exit...done!')