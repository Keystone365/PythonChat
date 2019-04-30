
import queue
import threading
import logging
import tkinter as tk # python 3

from socket import *
from datetime import datetime
from util.utility import *

from src.Client.ClientModel import ClientModel
from src.Client.ClientView import ClientWindow
from src.Client.ClientReceiver import ClientReceiver

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
    b_connect = False

    def __init__(self, *args, **kwargs):
        self.c_window = ClientWindow(self)
        self.receiver = ClientReceiver(self.model.CLIENT, self)

    def run(self):
        self.c_window.run()

    def login_handler(self, server, port, username, password):

        b_connect = self.connect(server, port)
        s_Error = ''

        if(not self.b_connect):
            logger.info("Connection failed.")
            self.c_window.error_box("Connection Error", "Connection failed. Please try again.")
        else:
            if(self.authenticate(username, password)):
                #set model info
                self.receiver.start()
                self.model.set_login(server, port, username)
                self.c_window.show_frame("ClientView")
                self.printmessage()
                logger.info("Login succesful")
            else:
                logger.info("Authentication failed.")
                self.c_window.error_box("Authentication Error", "Wrong username or password. Please try again.")

    def connect(self, server, port):
        if(not self.b_connect):
            self.b_connect = self.receiver.connect(server, port)

    def authenticate(self, receiver, username, password):

        self.receiver.send_method(username + ',' + password)
        s_message = self.receiver.receive_method()
        l_message = s_message.split('>')

        if(l_message[0] == 'a'):
            self.USERNAME = username
            print('Its Good')
            return True
        elif(l_message[0] == 'f'):
            print('NOT good!')
            return False

    def reply_handler(self, reply):
        self.c_window.update_txt_messages(reply)
        pass

    def send_handler(self, s_message):
        self.receiver.message("m>" + self.model.username + ": " + s_message)
        pass

    def error_handler(self, title, s_message):
        self.c_window.error_box(title, s_message)
        self.close()

    def clear_ent_window(self):
        self.c_window.clr_ent_field()

    def update_txt_messages(self, s_message):
        self.c_window.update_txt_messages(s_message)

    #Return key press handler
    def return_key_handler(self, event):
        frame = self.c_window.current_frame()
        frame.reply_message()
        pass

    def printmessage(self):
        self.update_txt_messages('PythonChat 2019 Client running')
        self.update_txt_messages('Host IP: ' + self.model.client_ip)    
        self.update_txt_messages('Server IP: ' + self.model.server_ip)  
        self.update_txt_messages('Listening on port: ' + str(self.model.client_port))
        self.update_txt_messages('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

    def get_server_port(self):
        return self.model.server_port

    def get_server_ip(self):
        return self.model.server_ip

    def close(self):
        if (not self.model.b_close):
            logger.info("Closing Client ClientController")
            self.model.THREADS_JOIN = True 
            logger.info("Closing Receiver")
            self.receiver.close()
            logger.info("Receiver closed")
            self.c_window.close_windows()
            logger.info("Window closed")
            self.model.b_close = True
            print('\nPythonChat Client cleanup and exit...done!')