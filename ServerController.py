#!/usr/bin/env python3
import util.utility as ut
import csv
import threading
import sys
import struct
import queue
import time
import logging
from datetime import datetime
#from IOBlocking import sendMessage, recvMessage, recvAll 
from socket import *


class ServerController():


    #print_lock = threading.Lock()
    THREADS_JOIN = False # Boolean flag for ending threads

    #set up logger
    LOG_FORMAT = "%(levelname)s (%(asctime)s): [%(processName)s] - %(message)s"
    logging.basicConfig(filename = "util/ServerChatLog.log",
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')
    logger = logging.getLogger() #root logger



    HOST = "127.0.0.1"
    PORT = 5006
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)
    #SERVER.settimeout(6) #set time out value
    SERVER.listen(5)

    def __init__(self):
        pass

    def Run(self):

        #variables
        loginAttempts = 0

        print('PythonChat 2018 Server running')
        print(gethostname())  
        print('Listening on port: ' + str(self.PORT))
        print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')


        
        # block until a connection arrives (timeout 1 second)
        connectionSocket, addr = self.SERVER.accept() 
        
        print("Connected with Server")
        # store the connection to the list
        #USER_CONNECTIONS.append([connectionSocket, addr, "NEW", "Guest"]) 
        #CLIENT_MESSAGE_QUEUE.put("New chat member from " + addr[0] + ":" + str(addr[1]))

        message = "Hello World from the server!"
        bMessage = message.encode()

        length = len(bMessage)

        connectionSocket.sendall(struct.pack('>I', length))
        connectionSocket.sendall(bMessage)
        print("Sent first message")

    def close(self):

        logger.info('# nCTRL-C: Server shutting down')
        logger.info('# - Disconnecting all clients')
        
        # notify all users and close connections
        for client in USER_CONNECTIONS: 
            try:
                sendMessage(client[0], "SYSTEM: Server closed")
            except ConnectionResetError: # client closed program
                pass
            finally:
                client[0].close() # close connection
            
        
        logger.info('# Clients successfully disconnected')        
        print(" - All clients disconnected")

        # set flag to force threads to end
        THREADS_JOIN = True 
        
        for thread in THREADS:
            print('Thread Ending:' + str(thread))
            thread.join()
            THREADS.remove(thread)
        
        logger.info('# All threads ended') 
        print(" - All threads ended")

        #ut.cls()
        print('\nPythonChat Server cleanup and exit...done!')
        SERVER.close()


    #sends message according to little endian unsigned int using format characters '<I'

    ###############################SEND#AND#RECIEVE#FUNCTIONS#####################################

    def sendMessage(client, message):

        '''Sends message according to little endian 
        unsigned int using format characters '<I'''
        
        # Prefix each message with a 4-byte length (network byte order)
        #'>' means little endian, 'I' means unsigned integer
        #CLIENT.send sends entire message as series of send
        
        bMessage = message.encode()
        
        length = len(bMessage)

        client.sendall(struct.pack('>I', length))
        client.sendall(bMessage)
        
    def recvMessage(client):

        # Read message length and unpack it into an integer
        bMessageLength = recieveAll(client, 4)
        
        intLength = int.from_bytes(bMessageLength, byteorder= 'big')
            
        serverMessage = recieveAll(client, intLength).decode()
        # Read the message data
        return serverMessage
        


    def recieveAll(client, length):

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


    def SystemCommand(self, message = []):

        '''Handles system command requests by clients'''

        # parse out the command (command and arguments)
        command = message[2].split(",") 
        
        # if they wanted an online user list
        if command[0] == "LIST":
        
            userList = ""
        
            for client in USER_CONNECTIONS: # find the sending user
                if message[0] == client[3]:
                    
                    # for each online authenticate user create name list
                    for user in USER_CONNECTIONS: 
                        if user[3] != "Guest": # if they have been authenticated
                            userList += user[3] + "\n" # add their name to the list

               
                    
                    
                    # send the list
                    sendMessage(client[0], "Online Users:" + userList)
                    logger.debug(client[3] + ' has been sent online user list')
                    break # stop searching for the sending user

                    
    def Broadcast(self, message = []):

        '''Handles broadcast messages to all users'''

        for user in USER_CONNECTIONS:
        
            if user[2] == "ONLINE":
            
                # in case they went offline by surprise
                try: 
                    sendMessage(user[0], message[0] + ": " + message[2]) # send the message to this user
                    
                # if client closed program flag and disconnect
                except ConnectionResetError: 
                    client[0].close()
                    user[2] = "DISCONNECTED"
                    pass # no worries, it's just a broadcast
                
        SERVER_MESSAGE_QUEUE.put(message[0] + ": " + message[2]) # echo the message to the server terminal
        
    def PrivateMessage(self, message = []):

        '''Handles private messages requests from clients'''

        # flag incase the target user is offline
        userOnline = False 

        # if this is a new message, not an offline queued message
        if message[3] == True: 
            for user in USER_CONNECTIONS: # check for the target user
                if message[1] == user[3]: # if the user is found
                    userOnline = True
                    
                    try: # in case they went offline by surprise
                    
                        # send the message to the user
                        sendMessage(user[0], message[0] + " -> You: " + message[2])
                        logger.info(message[0] + " -> " + message[1] + ": " + message[2])
                        SERVER_MESSAGE_QUEUE.put(message[0] + " -> " + message[1] + ": " + message[2])
                        
                    # client closed program    
                    except ConnectionResetError:
                    
                        # disconnect client and flag them as offline
                        client[0].close() 
                        user[2] = "DISCONNECTED" 
                    
                    break #Do not check other users

            if userOnline == False: # if the user wasn't online
                for user in USER_CONNECTIONS: # find the messager
                
                    if message[0] == user[3]: # if this is the messager
                        sendMessage(user[0], message[1] + " is offline. Message will be delivered when online") # send the message to the user
                        SERVER_MESSAGE_QUEUE.put("Offline queue: " + message[0] + " -> " + message[1] + ": " + message[2]) # echo the message to the server terminal
                        message[3] = False # flag the message as not new; offline queued
                        CLIENT_MESSAGE_QUEUE.put(message); # return the message to the end of the queue

        else: # offline queued message
            for user in USER_CONNECTIONS: # check for the target user
                if message[1] == user[3]: # if the user is found
                    userOnline = True
                    # in case they went offline by surprise
                    try: 

                        sendMessage(user[0], "Message sent while you were offline: " 
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

            if userOnline == False: # if the user still wasn't online
                CLIENT_MESSAGE_QUEUE.put(message) # return the message to the end of the queue





    def checkStoredMessages(self, client): 

        '''Function checks whether stored messages are available, sends stored messages'''
        
        for sender, reciever, message in STOREDMESSAGES:
            if client[2] == reciever:
                send(client[2], "FROM " + client[3] + ": " + message)
                       
                       
    def sendLoggedInNotification(self, client):

        '''Function sends notification to all online users that the client is online'''
        
        for user in USER_CONNECTIONS:
            message = "USER " + client[1] + " IS ONLINE"
            # queue the message, from this user, to the server
            SERVER_MESSAGE_QUEUE.put([client[3], "BROADCAST", message, True]) 
                      
             
    #########################CVS LOAD AND SAVE FUNCTIONS##########################################


    #Check User CSV: returns list of CSV file contents
    def LoadUserList(self):

        '''Load stored list of authenticated users from user.csv '''

        logger.info("In loading user function")
        file = open(UserPath, "r") # open the authentication file for reading
        text = file.read().splitlines() # read in all lines of the file
        file.close() # close the file
        logger.info("File Open in LoadUserList function")

        for line in text: # itterate through all the lines
            UserValues = line.split(",") # parse out the username and password hash
            UserValues.append(0) # number of failed login attempts
            UserValues.append(time.time()) # filler to initialize the index, later used to note time of lockout
            AUTHENTIC_USERS.append(UserValues) # store the object for later authentication
        
        logger.info("Successfully loaded csv in LoadUserList function")

          
          
    #returns message list for user        
    def LoadMessageList(self):

        '''Load stored unsent messages from messages.csv '''

        logger.info('Loading messages in LoadMessageList function')
        
        # open the authentication file for reading
        file = open(MessagePath, "r") 
        text = file.read().splitlines()
        file.close()

        # itterate through all the lines
        for line in text: 
            MessageValues = line.split(",") #Get message values
            CLIENT_MESSAGE_QUEUE.put(MessageValues) # store the object for later authentication
        
        logger.info("Successfully loaded csv in LoadMessageList function")


    #Write CSV: writes user dictionary to users.CSV file and writes over previous information		
    def SaveUserList(self, Name, Pass):

        '''Save known users to CSV file at util/users.csv'''
        
        file = open(UserPath, "a") # open authentication file to permanently save account
        file.write(Name + "," + Pass + "\n") # write the data to file
        file.close()
       
        
    #*************AUTHENICATE FUNCTIONS**************
        

    def NewUserAuth(self, client, username, passhash):

        '''New user creation and authentication function'''

        usernameExists = False # set flag

        for account in AUTHENTIC_USERS: 
            if account[0] == username: # if username already exists
                usernameExists = True # set flag
                break # no sense continuing to search
               
        if usernameExists == False: # unused name, create
        
            AUTHENTIC_USERS.append([username, passhash, 0, time.time()]) # create account in list
            
            SaveUserList(username, passhash)
            
            
            client[2] = "VERIFIED" # flag the connection as verified
            client[3] = username # associate the connection with the account name
            
            SERVER_MESSAGE_QUEUE.put("CREATED," + username) # debug
            
            sendMessage(client[0], str("CREATED," + username)) # report account created to client
            CLIENT_MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " joined the server", True]) # queue a broadcast that the new user joined
        
        else: # username already exists

            SERVER_MESSAGE_QUEUE.put("TAKEN," + credentials[1]) # debug
            client[0].send(("TAKEN," + username).encode()) # report that the account already exists to the client
            client[0].close() # disconnect client
            client[2] = "DISCONNECTED" # flag connection for cleanup
                
                
    def OldUserAuth(self, client, username, passhash):

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
        
    def acceptConnections(self):

        '''Function for accepting incoming client socket connections'''

        while not THREADS_JOIN:
            try:
                # block until a connection arrives (timeout 1 second)
                connectionSocket, addr = SERVER.accept() 
                
                # store the connection to the list
                USER_CONNECTIONS.append([connectionSocket, addr, "NEW", "Guest"]) 
                CLIENT_MESSAGE_QUEUE.put("New chat member from " + addr[0] + ":" + str(addr[1]))
                
            except timeout:
                pass # not a problem, just loop back
                
    def ClientMessageHandler(self):

        '''Function for handling send message request'''
        
        logger.debug('Handler for')

        while not THREADS_JOIN:
            try:
            
                message = CLIENT_MESSAGE_QUEUE.get(timeout=1) # pop the front message off the queue
             
             
                #IF SYSTEM COMMAND
                if message[0] == "SYSTEM": # if this is a command
                    SystemCommand(message)
                         
                #IF BROADCAST MESSAGE
                elif message[0] == "BROADCAST":
                    Broadcast(message)
                
             
                #IF PRIVATE MESSAGE
                else: # private message
                    PrivateMessage(message)
                
             
                CLIENT_MESSAGE_QUEUE.task_done() # report the gotten message as handled
            
            # timeout, not a problem 
            except queue.Empty: 
                pass 
            
            except Exception as er:
                logger.debug('Error occured in while sending message')
                raise er

                
                
    def printUserList(self):

        '''Print list of online users every 10 seconds'''
        
        while not THREADS_JOIN:
            time.sleep(10) # wait 10 seconds
            try:
            
                #print time
                ts = time.gmtime()
                timest = time.strftime("%Y-%m-%d %H:%M:%S", ts)
                listOfConnections = "Update " + timest + " -- "

                #print users
                if not USER_CONNECTIONS:
                    listOfConnections += "0 Users Online"
                else:
                    listOfConnections += str(len(USER_CONNECTIONS)) + " Online User(s):"
                    for user in USER_CONNECTIONS: # for all online users
                        username = ''
                        if username == 'Guest':
                            username = str(user[1])
                        else:
                            username = 'NAME:' + str(user[3]) + ', IP:' + str(user[1][0]) + ', PORT:' + str(user[1][1])
                        listOfConnections = listOfConnections + "\n~ " + username # add their name to the list
                    
                SERVER_MESSAGE_QUEUE.put(listOfConnections)
            except timeout:
                pass
                
                
    #authenticates and creates threads
    def Authenticate(self, client):

        '''Authenticate client connections for returning or new users'''
        
        logger.info('# Now in Authenticate function')
        
        usernameExists = False # flag to be set if the desired username already is taken

        try: 

            data = recvMessage(client[0]) # get authetication data from client
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
            
            
            
    def receiveMessages(self, client):

        '''Thread function for recieving messages from a client.'''

        logger.info('# RecieveMessages thread running') 
        SERVER_MESSAGE_QUEUE.put("Starting to receive messages from " + client[3])
        ClientDisconnect = False
       
        while not THREADS_JOIN and not ClientDisconnect:
            try:
             
                data = recvMessage(client[0])
                SERVER_MESSAGE_QUEUE.put("message received from " + client[3] + ": " + data)
                message = data.split(",", 1)
                
                # message format: 
                # "reciever, user:message" if private message,
                # or "BROADCAST,message" for broadcast message, 
                # "SYSTEM, DISCONNECT" for a controlled close of the client
                # "SYSTEM, LIST"
                
                print(message)
                
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
                client[0].close()
                client[2] = "DISCONNECTED"
                ClientDisconnect = True

             
             
    #################################MAIN##############################################         
     
    def LoadInfo(self):
        LoadUserList()
        LoadMessageList()









'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''



'''
        #get list of Authentic user names and old messages
        LoadInfo()

        # generate a thread to accept connections
        acceptThread = threading.Thread(target = acceptConnections, args = ()) 
        acceptThread.daemon = True
        acceptThread.start() 
        THREADS.append(acceptThread) 

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