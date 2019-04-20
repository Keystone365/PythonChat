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
from src.Server.ServerReciever import ServerReciever
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
            for reciever in self.model.USER_RECIEVERS: 
                try:
                    #self.sendMessage(client[0], "SYSTEM: Server closed")
                    reciever.close()
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

        if(not self.in_list(username, password, "1")):
            logger.info("user not in admin user list")
            self.s_window.error_box("Login Warning", 
                "Admin user not found. Incorrect username or password")
        else: 
            self.model.SERVER.listen(5)
            self.s_window.show_frame("ServerView")
            self.model.online_users.append(username)
            self.printmessage()

            logger.info("Entering Accept Thread")
            self.s_window.load_users(self.model.online_users)

            #Start Accept Thread
            manage_thread = threading.Thread(target = self.manage_connections, args = ()) 
            manage_thread.daemon = True
            manage_thread.start() 
            self.model.THREADS.append(manage_thread)

    def reply_handler(self, s_message):
        
        #TODO: Add code to parse for specific users
        for reciever in self.model.USER_RECIEVERS:
            reciever.message(s_message)

        self.s_window.update_txt_messages(s_message)

    def send_handler(self, s_message):
        self.reply_handler("Server(" + self.model.HOST + "): " + s_message)

    def in_list(self, username, passhash, admin):

        for account in self.model.AUTHENTIC_USERS: #itterate through account list
            # if username found, password correct and admin privliges
            if (account[0] == username) and (account[1] == passhash) and (account[2] == admin):
                return True
        #return false if no user match
        return False

    def manage_connections(self):

        '''Function for accepting incoming client socket connections'''

        logger.info("In Accept Thread")
        while not self.model.THREADS_JOIN:
            try:

                connectionSocket, addr = self.model.SERVER.accept() 

                print("Connected to new user.")

                reciever = ServerReciever(connectionSocket, self)
                reciever.start()
                self.model.USER_RECIEVERS.append(reciever)
                self.model.online_users.append(str(addr))
                self.s_window.update_users(str(addr))
                
            except timeout:
                pass
            except Exception as er:
                raise er

    def printmessage(self):
        self.reply_handler('PythonChat 2019 Server running')
        self.reply_handler('Host IP: ' + gethostname())     
        self.reply_handler('Listening on port: ' + str(self.model.PORT))
        self.reply_handler('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
    def private_message(self, message = []):
        pass

    def check_stored_messages(self, client): 

        '''Function checks whether stored messages are available, sends stored messages'''
        pass               
                       
    def send_logged_in_notification(self, client):

        '''Function sends notification to all online users that the client is online'''
        
        pass
                      
             
    #########################CVS LOAD AND SAVE FUNCTIONS##########################################

           
    #*************AUTHENICATE FUNCTIONS**************
        

    def new_user_auth(self, client, username, passhash):

        '''New user creation and authentication function'''

        username_exists = False # set flag

        for account in self.model.AUTHENTIC_USERS: 
            if account[0] == username: # if username already exists
                username_exists = True # set flag
                break # no sense continuing to search
               
        if username_exists == False: # unused name, create
        
            AUTHENTIC_USERS.append([username, passhash, 0, time.time()]) # create account in list
            
            save_user_list(username, passhash)
            
            
            client[2] = "VERIFIED" # flag the connection as verified
            client[3] = username # associate the connection with the account name
            
            SERVER_MESSAGE_QUEUE.put("CREATED," + username) # debug
            
            send_message(client[0], str("CREATED," + username)) # report account created to client
            CLIENT_MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " joined the server", True]) # queue a broadcast that the new user joined
        
        else: # username already exists

            SERVER_MESSAGE_QUEUE.put("TAKEN," + credentials[1]) # debug
            client[0].send(("TAKEN," + username).encode()) # report that the account already exists to the client
            client[0].close() # disconnect client
            client[2] = "DISCONNECTED" # flag connection for cleanup
                            
    def old_user_auth(self, client, username, passhash):

        '''Returning User authentication function'''

        for account in AUTHENTIC_USERS: #itterate through account list
            if (account[0] == username) and (account[1] == passhash): # if username found and password correct
               
               
                #if account[2] == 4: # if the account is locked out
                '''    SERVER_MESSAGE_QUEUE.put("ACCOUNTLOCKED," + account[1] + "," + str(time.time() - account[3])) # debug
                    client[0].send(("ACCOUNTLOCKED," + account[1] + "," + str(time.time() - account[3])).encode()) # report lockout to client
                    client[0].close() # disconnect client
                    client[2] = "DISCONNECTED" # flag connection for cleanup
                   ''' 
                #else: # if the account is not locked out
                client[2] = "VERIFIED" # flag the account as validated
                client[3] = account[0] # associate account name with client
                account[2] = 0 # reset failed login count
                SERVER_MESSAGE_QUEUE.put("LOGGEDIN," + account[1]) # debug
                client[0].send(("LOGGEDIN," + account[1]).encode()) # report the successful login
                CLIENT_MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " connected to the server", True]) # queue a broadcast that the user is now online
                     
                     
                     
            else: # if the client wasn't disconnected or verified
                SERVER_MESSAGE_QUEUE.put("NOACCOUNT," + username) # debug
                client[0].send(("NOACCOUNT," + username).encode()) # report that the username wasn't found
                client[0].close() # disconnect client
                client[2] = "DISCONNECTED" # flag connection for cleanup
                
                
            '''else: # if incorrect username or password
                
                account[2] += 1 # add one count to the failed login count
                if account[2] == 4: # if there are now 4 failed logins
                account[3] = time.time() # note time of 4th failed login
                SERVER_MESSAGE_QUEUE.put("WRONGPASS," + account[1] + "," + str(account[2])) # debug
                client[0].send(("WRONGPASS," + account[1] + "," + str(account[2])).encode()) # report the failed login and the failed login count
                client[0].close() # disconnect client
                client[2] = "DISCONNECTED" # flag connection for cleanup
                
                break # stop itterating when the right username has been found'''
                       
'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''