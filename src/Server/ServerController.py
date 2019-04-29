#!/usr/bin/env python3

#import csv
import threading
import sys
import struct
import time
import logging

from datetime import datetime
from util.utility import *
from socket import *

from src.Server.ServerModel import ServerModel
from src.Server.ServerView import ServerWindow
from src.Server.ServerReceiver import ServerReceiver
#from IOBlocking import sendMessage, recvMessage, recvAll 


LOG_FORMAT = "%(levelname)s (%(asctime)s): [%(processName)s] - %(message)s"
logging.basicConfig(filename = "data/ServerChatLog.log",
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')
logger = logging.getLogger() #root logger

class ServerController():

    def __init__(self):
        logger.info('Initializing controller')
        self.s_window = ServerWindow(self)
        self.model = ServerModel()

    def run(self):
        print('PythonChat 2018 Server running')
        print(gethostname())  
        print('Listening on port: ' + str(self.model.PORT))
        print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
        self.model.load_info()
        self.s_window.run()

    def close(self):

        if (not self.model.b_close):
            logger.info("Closing ServerController")
            self.s_window.close_windows()
            self.model.b_close = True
            self.model.THREADS_JOIN = True

            logger.info('# - Disconnecting all clients')
            for receiver in self.model.USER_RECEIVERS: 
                try:
                    #self.sendMessage(client[0], "SYSTEM: Server closed")
                    receiver.close()
                except ConnectionResetError: # client closed program
                    pass
                    
            logger.info('# - Closing all Threads')        
            for thread in self.model.THREADS:
                logger.info('Thread Ending:' + str(thread))
                thread.join()
                self.model.THREADS.remove(thread)

            print('\nPythonChat Server cleanup and exit...done!')
            self.model.SERVER.close()

    def return_key_handler(self, event):
        pass

    def login_handler(self, username, password):

        '''This method handles the admin login. Checks username and password.'''

        if(not self.authenticate_handler(True, username, password)):
            logger.info("user not in admin user list")
            self.s_window.error_box("Login Warning", 
                "Admin user not found. Incorrect username or password")
        else: 
            self.model.SERVER.listen(5)
            self.USERNAME = username
            self.s_window.show_frame("ServerView")
            self.model.online_users.append(self.USERNAME)
            self.printmessage()

            logger.info("Entering Accept Thread")
            self.s_window.load_users(self.model.online_users)

            #Start Accept Thread
            manage_thread = threading.Thread(target = self.manage_connections, args = ()) 
            manage_thread.daemon = True
            manage_thread.start() 
            self.model.THREADS.append(manage_thread)

    def reply_handler(self, s_message):

        '''Method for handling incoming reply messages from clients.
            m - message,
            b - broadcast.
        '''

        l_message = s_message.split('>')
        if(l_message[0] == 'm'):
            self.send_handler('b>' + ''.join(l_message[1:]))

        #TODO: Add code to parse for specific users
        pass

    def send_handler(self, s_message):

        '''Send handler method. INPUT: string message.
            b = broadcast,
        '''

        l_message = s_message.split('>')
        s_text = ''.join(l_message[1:])
        print('<' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '>: ' + s_text)

        if(l_message[0] == 'b'):
            self.broadcast(s_text)
        elif(l_message[0] == 'p'):
            self.private(s_text)

        self.s_window.update_txt_messages(''.join(l_message[1:]))

    def authenticate_handler(self, b_admin, s_username, s_password):

        '''Checks string and returns true or false value if cleared.'''

        #print(self.model.AUTHENTIC_USERS)
        return self.model.is_authentic(b_admin, s_username, s_password)

    def manage_connections(self):

        '''Function for accepting incoming client socket connections'''

        logger.info("In Accept Thread")
        while not self.model.THREADS_JOIN:
                
                receiver = ServerReceiver(self.model.SERVER, self)
                b_connect = False
                
                while(not b_connect and not self.model.THREADS_JOIN):
                    b_connect = receiver.connect()

                if(b_connect and receiver.authenticate()):
                    receiver.start()
                    self.model.USER_RECEIVERS.append(receiver)
                    self.model.online_users.append(receiver.USERNAME)
                    self.s_window.update_users(receiver.USERNAME)

    def private(self, info):

        '''Private message handler method'''

        pass

    def update_txt_messages(self, string):
        self.s_window.update_txt_messages(string)

    def printmessage(self):
        self.update_txt_messages('PythonChat 2019 Server running')
        self.update_txt_messages('Host IP: ' + gethostname())     
        self.update_txt_messages('Listening on port: ' + str(self.model.PORT))
        self.update_txt_messages('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
        
    def private_message(self, message = []):
        pass

    def check_stored_messages(self, client): 

        '''Function checks whether stored messages are available, sends stored messages'''
        pass               
                       
    def send_logged_in_notification(self, client):

        '''Function sends notification to all online users that the client is online'''
        
        pass

    def broadcast(self, s_message):

        '''Sends string message to every online user'''

        for reciever in self.model.USER_RECEIVERS:
            reciever.message(s_message)

                    
                       
'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''