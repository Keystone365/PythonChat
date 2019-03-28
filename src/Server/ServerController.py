#!/usr/bin/env python3
from util.utility import *
import csv
import threading
import sys
import struct
import time
import logging
from datetime import datetime
from src.Server.ServerModel import ServerModel
from src.Server.ServerView import ServerWindow
from src.Server.ServerReciever import ServerReciever
#from IOBlocking import sendMessage, recvMessage, recvAll 
from socket import *


LOG_FORMAT = "%(levelname)s (%(asctime)s): [%(processName)s] - %(message)s"
logging.basicConfig(filename = "data/ServerChatLog.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger() #root logger

class ServerController():

    def __init__(self):
        logger.info('Initializing controller')
        self.window = ServerWindow(self)
        self.model = ServerModel()

    def run(self):

        print('PythonChat 2018 Server running')
        print(gethostname())  
        print('Listening on port: ' + str(self.model.PORT))
        print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

        logger.info("Starting window")
        self.model.load_info()
        self.window.run()

    def close(self):

        if (not self.model.b_close):
            logger.info("Closing ServerController")
            self.window.close_windows()
            self.model.bClose = True
            self.model.THREADS_JOIN = True

            logger.info('# - Disconnecting all clients')
            
            # notify all users and close connections
            for reciever in self.model.USER_RECIEVERS: 
                try:
                    #self.sendMessage(client[0], "SYSTEM: Server closed")
                    reciever.close()
                except ConnectionResetError: # client closed program
                    pass
                
            
            logger.info('# Clients successfully disconnected')        
            
            for thread in self.model.THREADS:
                logger.info('Thread Ending:' + str(thread))
                thread.join()
                self.model.THREADS.remove(thread)
            
            logger.info('# All threads ended') 

            #ut.cls()
            print('\nPythonChat Server cleanup and exit...done!')
            self.model.SERVER.close()

    def handler():
        pass

    def return_key_handler(self, event):
        pass

    def login_handler(self, username, password):

        if(not self.in_list(username, password, "1")):
            print("not in admin user list")
            self.window.login_warning()
        else: 
            self.window.show_frame("ServerView")

            logger.info("Entering Accept Thread")

            #Start Accept Thread
            manage_thread = threading.Thread(target = self.manage_connections, args = ()) 
            manage_thread.daemon = True
            manage_thread.start() 
            self.model.THREADS.append(manage_thread)

            '''#Start Accept Thread
            acceptThread = threading.Thread(target = self.acceptConnections, args = ()) 
            acceptThread.daemon = True
            acceptThread.start() 
            self.model.THREADS.append(acceptThread)'''

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

                print("Attempting to connect")
                # block until a connection arrives (timeout 1 second)
                connectionSocket, addr = self.model.SERVER.accept() 

                print("Connected!")

                reciever = ServerReciever(connectionSocket, SERVER_MESSAGE_QUEUE, self)
                self.model.USER_RECIEVERS.append(reciever)
                #TODO: Need to add loop to close section to remove recievers
                
                # store the connection to the list
                #self.model.USER_CONNECTIONS.append([connectionSocket, addr, "NEW", "Guest"]) 
                #self.model.CLIENT_MESSAGE_QUEUE.put("New chat member from " + addr[0] + ":" + str(addr[1]))


                #recieveThread = threading.Thread(target = self.recieveMessages, args = (connectionSocket, self.model.SERVER_MESSAGE_QUEUE, self))
                #recieveThread.daemon = True
                #recieveThread.start()
                #self.model.THREADS.append(recieveThread)
                
            except timeout:
                pass # not a problem, just loop back
            except Exception as er:
                raise er

    #sends message according to little endian unsigned int using format characters '<I'

    ###############################SEND#AND#RECIEVE#FUNCTIONS#####################################

    def send_message(self, client, message):

        '''Sends message according to little endian 
        unsigned int using format characters '<I'''
        
        # Prefix each message with a 4-byte length (network byte order)
        #'>' means little endian, 'I' means unsigned integer
        #CLIENT.send sends entire message as series of send
        
        b_message = message.encode()
        
        length = len(b_message)

        client.sendall(struct.pack('>I', length))
        client.sendall(b_message)
 
    def recv_message(client):

        # Read message length and unpack it into an integer
        b_messageLength = recieve_all(client, 4)
        
        i_Length = int.from_bytes(bMessageLength, byteorder= 'big')
            
        server_message = recieve_all(client, intLength).decode()
        # Read the message data
        return server_message        

    def recieve_all(client, length):

        '''Helper function to recv a number of bytes or return None if EOF is hit'''

        #byte sequence
        data = b''
        
        #keep recieving data and adding to message until entire message is recieved
        while (length):
        
            #recieve data
            packet = client.recv(length)
            
            if not packet: return None
            data += packet
            
            length -= len(packet)
        return data


    ###############################MESSAGING FUNCTIONS############################################

    def system_command(self, message = []):

        '''Handles system command requests by clients'''

        # parse out the command (command and arguments)
        command = message[2].split(",") 
        
        # if they wanted an online user list
        if command[0] == "LIST":
        
            user_list = ""
        
            for client in self.model.USER_CONNECTIONS: # find the sending user
                if message[0] == client[3]:
                    
                    # for each online authenticate user create name list
                    for user in USER_CONNECTIONS: 
                        if user[3] != "Guest": # if they have been authenticated
                            user_list += user[3] + "\n" # add their name to the list

               
                    
                    
                    # send the list
                    send_message(client[0], "Online Users:" + userList)
                    logger.debug(client[3] + ' has been sent online user list')
                    break # stop searching for the sending user
            
    def broadcast(self, message = []):

        '''Handles broadcast messages to all users'''

        for user in self.model.USER_CONNECTIONS:
        
        #if user[2] == "ONLINE":
            
            # in case they went offline by surprise
            try: 
                send_message(user[0], message[0] + ": " + message[2]) # send the message to this user
                
            # if client closed program flag and disconnect
            except ConnectionResetError: 
                client[0].close()
                user[2] = "DISCONNECTED"
                pass # no worries, it's just a broadcast
                
        self.model.SERVER_MESSAGE_QUEUE.put(message[0] + ": " + message[2]) # echo the message to the server terminal
    
    def private_message(self, message = []):

        '''Handles private messages requests from clients'''

        # flag incase the target user is offline
        user_online = False 

        # if this is a new message, not an offline queued message
        if message[3] == True: 
            for user in self.model.USER_CONNECTIONS: # check for the target user
                if message[1] == user[3]: # if the user is found
                    user_online = True
                    
                    try: # in case they went offline by surprise
                    
                        # send the message to the user
                        send_message(user[0], message[0] + " -> You: " + message[2])
                        logger.info(message[0] + " -> " + message[1] + ": " + message[2])
                        SERVER_MESSAGE_QUEUE.put(message[0] + " -> " + message[1] + ": " + message[2])
                        
                    # client closed program    
                    except ConnectionResetError:
                    
                        # disconnect client and flag them as offline
                        client[0].close() 
                        user[2] = "DISCONNECTED" 
                    
                    break #Do not check other users

            if user_online == False: # if the user wasn't online
                for user in USER_CONNECTIONS: # find the messager
                
                    if message[0] == user[3]: # if this is the messager
                        send_message(user[0], message[1] + " is offline. Message will be delivered when online") # send the message to the user
                        self.model.SERVER_MESSAGE_QUEUE.put("Offline queue: " + message[0] + " -> " + message[1] + ": " + message[2]) # echo the message to the server terminal
                        message[3] = False # flag the message as not new; offline queued
                        self.model.CLIENT_MESSAGE_QUEUE.put(message); # return the message to the end of the queue

        else: # offline queued message
            for user in USER_CONNECTIONS: # check for the target user
                if message[1] == user[3]: # if the user is found
                    user_online = True
                    # in case they went offline by surprise
                    try: 

                        send_message(user[0], "Message sent while you were offline: " 
                                        + message[0] + " -> You: " 
                                        + message[2])
                                        
                        logger.debug("Queued message sent:" + message[0] 
                                    + " -> " + message[1] 
                                    + ": " + message[2])
                    
                    # client closed program, disconnect and flag
                    except ConnectionResetError: 
                        client[0].close() 
                        user[2] = "DISCONNECTED" 
                        userOnline = False

            if user_online == False: # if the user still wasn't online
                self.model.CLIENT_MESSAGE_QUEUE.put(message) # return the message to the end of the queue

    def check_stored_messages(self, client): 

        '''Function checks whether stored messages are available, sends stored messages'''
        
        for sender, reciever, message in self.model.STOREDMESSAGES:
            if client[2] == reciever:
                send(client[2], "FROM " + client[3] + ": " + message)                   
                       
    def send_logged_in_notification(self, client):

        '''Function sends notification to all online users that the client is online'''
        
        for user in USER_CONNECTIONS:
            message = "USER " + client[1] + " IS ONLINE"
            # queue the message, from this user, to the server
            self.model.SERVER_MESSAGE_QUEUE.put([client[3], "BROADCAST", message, True]) 
                      
             
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
                 

    ##################################THREAD FUNCTIONS################################
            
    def client_message_handler(self):

        '''Function for handling send message request'''
        
        logger.debug('Handler for')

        while not self.model.THREADS_JOIN:
            try:
            
                message = CLIENT_MESSAGE_QUEUE.get(timeout=1) # pop the front message off the queue
             
             
                #IF SYSTEM COMMAND
                if message[0] == "SYSTEM": # if this is a command
                    system_command(message)
                         
                #IF BROADCAST MESSAGE
                elif message[0] == "BROADCAST":
                    broadcast(message)
                
             
                #IF PRIVATE MESSAGE
                else: # private message
                    private_message(message)
                
             
                CLIENT_MESSAGE_QUEUE.task_done() # report the gotten message as handled
            
            # timeout, not a problem 
            except queue.Empty: 
                pass 
            
            except Exception as er:
                logger.debug('Error occured in while sending message')
                raise er
             
    def printUserList(self):

        '''Print list of online users every 10 seconds'''
        
        while not self.model.THREADS_JOIN:
            time.sleep(10) # wait 10 seconds
            try:
            
                #print time
                ts = time.gmtime()
                timest = time.strftime("%Y-%m-%d %H:%M:%S", ts)
                list_of_Connections = "Update " + timest + " -- "

                #print users
                if not USER_CONNECTIONS:
                    list_of_Connections += "0 Users Online"
                else:
                    list_of_connections += str(len(USER_CONNECTIONS)) + " Online User(s):"
                    for user in USER_CONNECTIONS: # for all online users
                        username = ''
                        if username == 'Guest':
                            username = str(user[1])
                        else:
                            username = 'NAME:' + str(user[3]) + ', IP:' + str(user[1][0]) + ', PORT:' + str(user[1][1])
                        list_of_Connections = listOfConnections + "\n~ " + username # add their name to the list
                    
                SERVER_MESSAGE_QUEUE.put(listOfConnections)
            except timeout:
                pass
                            
    #authenticates and creates threads
    def authenticate(self, client):

        '''Authenticate client connections for returning or new users'''
        
        logger.info('# Now in Authenticate function')
        
        b_username_exists = False # flag to be set if the desired username already is taken

        try: 

            data = recv_message(client[0]) # get authetication data from client
            if data == "": # if the message is blank
                logger.debug('Empty String recieved from client')
                raise ConnectionResetError # assume client closed


            credentials = data.split(",") # parse data into list
            logger.debug('Data recieved for Authentication = ' + data)
            print(data)

            SERVER_MESSAGE_QUEUE.put("Client authenticating with message " + data) # debugging
            SERVER_MESSAGE_QUEUE.put(credentials[0] + "\n" + credentials[1]) # debugging

            if credentials[0] == "CREATE": # account creation
                NewUserAuth(client, credentials[1], credentials[2])
                 
            elif credentials[0] == "LOGIN": #login from old user
                OldUserAuth(client, credentials[1], credentials[2])
               
        except ConnectionResetError: # client closed program
            client[0].close() # disconnect client
            SERVER_MESSAGE_QUEUE.put("Disconnect: " + client[1][0] + ":" + str(client[1][1]))
            client[2] = "DISCONNECTED" # flag connection for cleanup       
            
    def receive_messages(self, client):

        '''Thread function for recieving messages from a client.'''

        logger.info('# RecieveMessages thread running') 
        #self.model.SERVER_MESSAGE_QUEUE.put("Starting to receive messages from " + client[3])
        client_disconnect = False
       
        while not self.model.THREADS_JOIN and not client_disconnect:
            try:
             
                data = recvMessage(client)
                #SERVER_MESSAGE_QUEUE.put("message received from " + client[3] + ": " + data)
                #message = data.split(",", 1)
                
                # message format: 
                # "reciever, user:message" if private message,
                # or "BROADCAST,message" for broadcast message, 
                # "SYSTEM, DISCONNECT" for a controlled close of the client
                # "SYSTEM, LIST"
                
                print(data)
                
                '''
                if message[0] == "SYSTEM": 
                    if message[1] == "DISCONNECT":
                        client[0].close() 
                        client[2] = "DISCONNECTED" # flag connection for cleanup
                        ClientDisconnect = True
                    else:
                        # queue the message, from this user, to the server
                        CLIENT_MESSAGE_QUEUE.put([client[3], "SYSTEM", message[1], True]) 
             
                elif message[0] == "BROADCAST":
                    CLIENT_MESSAGE_QUEUE.put([client[3], "BROADCAST", message[1], True])
                
                else: 
                    # private message
                    userExists = False
                
                    for user in AUTHENTIC_USERS: # scan the registered user list
                       if message[0] == user[0]: # if the specified user is found to exist
                          CLIENT_MESSAGE_QUEUE.put([client[3], message[0], message[1], True]) # queue the message
                          
                          userExists = True # flag that it is a valid username
                          break # stop searching
                          
                    if userExists == False: # if the username doesn't exist
                       CLIENT_MESSAGE_QUEUE.put(["SYSTEM", client[3], "No such user " + message[0], True]) # report this to the messager
            '''
            except timeout:
                pass
                
            # client closed program 
            except ConnectionResetError: 
                #client[0].close()
                #client[2] = "DISCONNECTED"
                print("ConnectionResetError occured.")
                client_disconnect = True        
             
    #################################MAIN##############################################         










'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''



'''
        #get list of Authentic user names and old messages
        LoadInfo()

        # generate a thread to accept connections


        # generate thread to asyncronusly send messages
        outgoingMessagesThread = threading.Thread(target = ClientMessageHandler, args = ()) 
        outgoingMessagesThread.daemon = True
        outgoingMessagesThread.start() 
        THREADS.append(outgoingMessagesThread)

        # generate a thread to list all users on a timer
        printUserListThread = threading.Thread(target = printUserList, args = ()) 
        printUserListThread.daemon = True
        printUserListThread.start()
        THREADS.append(printUserListThread)


        print('The server is ready to receive')

        #loop to handle user connections
        while True:
            for client in USER_CONNECTIONS:
            
                # if we have any new client connections
                if client[2] == "NEW": 
                    client[2] = "AUTH"

                    # asyncronusly handle authentication
                    # catalog the thread in the master list
                    authenticateThread = threading.Thread(target = Authenticate, args = (client,))
                    authenticateThread.start() 
                    THREADS.append(authenticateThread); 
                
                # newly verified connection, start thread for recieving messages
                elif client[2] == "VERIFIED": 
                    client[2] = "ONLINE"
                    
                    
                    # asyncronusly handle messages from client
                    # catalog the thread in the master list
                    incomingMessagesThread = threading.Thread(target = receiveMessages, args = (client,))
                    incomingMessagesThread.start() 
                    THREADS.append(incomingMessagesThread); 
                
                # if the client has been disconnected and needs to be cleaned up
                elif client[2] == "DISCONNECTED": 
                    if not client[3] == "Guest":
                       CLIENT_MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " disconnected", True])
                    USER_CONNECTIONS.remove(client)
            
            
            # thread cleanup for dead threads
            for thread in THREADS: 
                if not thread.isAlive(): 
                    thread.join()
                    THREADS.remove(thread)

            #print server message queue
            while SERVER_MESSAGE_QUEUE.qsize():
                text = SERVER_MESSAGE_QUEUE.get()
                print(text) # print the message
                SERVER_MESSAGE_QUEUE.task_done() '''

"""
def recvMessage(client):

    print('In recvMessage')
    
    # Read message length and unpack it into an integer
    MessageLength = recieveAll(con, 4)
    
    print('Retrieved length')
    
    print (MessageLength)
    
    i = int.from_bytes(MessageLength, byteorder= 'big')
    
    print(i)
        
    x = recieveAll(con, i).decode()
    # Read the message data
    return x

# Helper function to recv a number of bytes or return None if EOF is hit
def recieveAll(con, length):
    
    print('in recieveAll')
    
    #byte sequence
    data = b''
    
    while (length):
    
        #recieve data
        packet = con.recv(length)
        
        print(packet)
        
        if not packet: return None
        data += packet
        
        print(data)
        
        length -= len(packet)

    return data
    
    """