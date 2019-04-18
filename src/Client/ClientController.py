
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

    model = ClientModel()
    b_close = False

    def __init__(self, *args, **kwargs):
        self.c_window = ClientWindow(self)
        self.reciever = ClientReciever(self)

    def run(self):
        self.c_window.run()

    def login_handler(self, server, port, username):

        b_start = self.reciever.start(server, port, username)

        if(b_start):

            self.reciever.message("Connected!")
            #set model info
            self.model.set_login(server, port, username)
            self.c_window.show_frame("ClientView")
            self.printmessage()
            logger.info("Login succesful")
        else:
            logger.info("Login failed.")
            self.c_window.error_box("Connection Error", "Connection failed. Please try again.")
        pass

    def reply_handler(self, reply):
        self.c_window.update_txt_messages(reply)
        pass

    def send_handler(self, s_message):
        self.reciever.message(s_message)
        pass

    def error_handler(self, title, s_message):
        self.c_window.error_box(title, s_message)
        self.close()

    def clear_ent_window(self):
        self.c_window.clr_ent_field()

    def update_txt(self, s_message):
        self.c_window.update_txt_messages(s_message)

    #Return key press handler
    def return_key_handler(self, event):
        frame = self.c_window.current_frame()
        frame.reply_message()
        pass

    def printmessage(self):
        self.reply_handler('PythonChat 2019 Client running')
        self.reply_handler('Host IP: ' + self.model.client_ip)    
        self.reply_handler('Server IP: ' + self.model.server_ip)  
        self.reply_handler('Listening on port: ' + str(self.model.client_port))
        self.reply_handler('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def get_server_port(self):
        return self.model.server_port

    def get_server_ip(self):
        return self.model.server_ip

    def close(self):
        if (not self.model.b_close):
            logger.info("Closing Client ClientController")
            self.model.THREADS_JOIN = True
            logger.info("Closing Reciever")
            self.reciever.close()
            logger.info("Reciever closed")
            self.c_window.close_windows()
            logger.info("Window closed")
            self.model.b_close = True
            print('\nPythonChat Client cleanup and exit...done!')