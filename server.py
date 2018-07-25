#!/usr/bin/env python3
import util.utility as ut
import csv
import threading
import sys
import struct
import queue
import time
from datetime import datetime
#from IOBlocking import sendMessage, recvMessage, recvAll 
from socket import *

#print_lock = threading.Lock()
THREADS_JOIN = False # Boolean flag for ending threads



HOST = ''
PORT = 5006
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
SERVER.settimeout(6) #set time out value
SERVER.listen(5)

THREADS = [] #list of threads for cleanup
#all threads will be appended to this list
#itterating through this list will be used for clean up


AUTHENTIC_USERS = [] #Authentic user list - for reading from and updating CSV file
# populated on startup
# for each element of AUTHENTIC_USERS
# [0]: user
# [1]: passhash


USER_CONNECTIONS = [] #For listing number of user connections
# Each new connection is appended to the list in the following format (sublist, e.g. CONNECTIONS[0][1] == addr):
# [0]: connection socket of the client, used to send/receive
# [1]: address of client, not yet used, but stored if needed
# [2]: status of connection. Statuses so far:
#     "NEW": newly connected, accepted and stored, not yet authenticated
#     "AUTH": started authentication, not yet logged in
#     "VERIFIED": completed authentication, ready to start communication
#     "ONLINE": communication set up and actively sending/recieving messages
#     "DISCONNECTED": connection has been terminated, awaiting cleanup
# [3]: username of validated login.  Defaults to "Guest" prior to authentication

#list of storing messages
SERVER_MESSAGE_QUEUE = queue.Queue()

MESSAGE_QUEUE = queue.Queue() # populated by receiveMessages threads, consumed by sendMessages thread
# each received message from clients, in the following format:
# [0]: sending user, may be "SYSTEM" for informative messages
# [1]: target user, may be "BROADCAST" for sending to all online users
# [2]: message
# [3]: is new? (messages for offline users will be recycled to the back of the queue, reporting to the messager should only happen the first time it cycles through)


STOREDMESSAGES = []
#[0] sender
#[1] reciever
#[2] message


#online user list - not related to CSV file
onlineUsers = []

#paths for CSV files
UserPath = 'util/users.csv'
MessagePath = 'util/messages.csv'


#sends message according to little endian unsigned int using format characters '<I'


def sendMessage():
   while not THREADS_JOIN:
      try:
         message = MESSAGE_QUEUE.get(timeout=1) # pop the front message off the queue
         
         
         #############IF SYSTEM COMMAND#########################################
         if message[1] == "SYSTEM": # if this is a command
            command = message[2].split(",") # parse out the command (command and arguments)
            if command[0] == "LIST": # if they wanted an online user list
               for client in USER_CONNECTIONS: # find the sending user
                  if message[0] == client[3]: # if the user is found
                     userList = "" # prepare a string for a list of online users
                     for user in CONNECTIONS: # for each online user
                        if user[3] != "Guest": # if they have been authenticated
                           userList += user[3] + "\n" # add their name to the list
                     SERVER_MESSAGE_QUEUE.put("Online Users:" + userList) # debug
                     client[0].send(("Online Users:" + userList).encode()) # send the list
                     break # stop searching for the sending user
                     
         ###########################IF BROADCAST MESSAGE###########################
         elif message[1] == "BROADCAST": # if it is a broadcast message
            for user in USER_CONNECTIONS: # for all online users
               if user[2] == "ONLINE": # only send broadcasts to prepared users
                  try: # in case they went offline by surprise
                     user[0].send((message[0] + ": " + message[2]).encode()) # send the message to this user
                  except ConnectionResetError: # client closed program
                     client[0].close() # disconnect client
                     user[2] = "DISCONNECTED" # flag them as offline
                     pass # no worries, it's just a broadcast
            SERVER_MESSAGE_QUEUE.put(message[0] + ": " + message[2]) # echo the message to the server terminal
         
         ###########################IF PRIVATE MESSAGE###########################
         else: # private message
            if message[3] == True: # if this is a new message, not an offline queued message
               userOnline = False # flag incase the target user is offline
               for user in USER_CONNECTIONS: # check for the target user
                  if message[1] == user[3]: # if the user is found
                     userOnline = True
                     try: # in case they went offline by surprise
                        user[0].send((message[0] + " -> You: " + message[2]).encode()) # send the message to the user
                        SERVER_MESSAGE_QUEUE.put(message[0] + " -> " + message[1] + ": " + message[2]) # echo the message to the server terminal
                     except ConnectionResetError: # client closed program
                        client[0].close() # disconnect client
                        user[2] = "DISCONNECTED" # flag them as offline
                        userOnline = False # mark them back to offline
               
               if userOnline == False: # if the user wasn't online
                  for user in USER_CONNECTIONS: # find the messager
                     if message[0] == user[3]: # if this is the messager
                        user[0].send((message[1] + " is offline. Message will be delivered when online").encode()) # send the message to the user
                        SERVER_MESSAGE_QUEUE.put("Offline queue: " + message[0] + " -> " + message[1] + ": " + message[2]) # echo the message to the server terminal
                        message[3] = False # flag the message as not new; offline queued
                        MESSAGE_QUEUE.put(message); # return the message to the end of the queue
            
            else: # offline queued message
               userOnline = False # flag for if the target user is still offline
               for user in USER_CONNECTIONS: # check for the target user
                  if message[1] == user[3]: # if the user is found
                     userOnline = True
                     try: # in case they went offline by surprise
                        user[0].send(("Message sent while you were offline: " + message[0] + " -> You: " + message[2]).encode()) # send the message to the user
                        SERVER_DISPLAY_QUEUE.put("Queued message sent:" + message[0] + " -> " + message[1] + ": " + message[2]) # echo the message to the server terminal
                     except ConnectionResetError: # client closed program
                        client[0].close() # disconnect client
                        user[2] = "DISCONNECTED" # flag them as offline
                        userOnline = False # mark them back to offline
                        
               if userOnline == False: # if the user still wasn't online
                  MESSAGE_QUEUE.put(message); # return the message to the end of the queue
         
         MESSAGE_QUEUE.task_done() # report the gotten message as handled
      except queue.Empty:
         pass # timeout, not a problem
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

def checkStoredMessages(client): 
# checks whether stored messages are available, sends stored messages
          for sender, reciever, message in STOREDMESSAGES:
                if client[2] == reciever:
                   client[2].send(("FROM " + client[3] + ": " + message).encode())
                   
                   
def sendLoggedInNotification(client):
# sends notification to all online users that the client is online
    for user in CONNECTIONS:
            message = "USER " + client[1] + " IS ONLINE"
            SERVER_MESSAGE_QUEUE.put([client[3], "BROADCAST", message, True]) # queue the message, from this user, to the server
            
def receiveMessages(client):
   SERVER_MESSAGE_QUEUE.put("Starting to receive messages from " + client[3]) # debug
   ClientDisconnect = False
   
   while not THREADS_JOIN and not ClientDisconnect:
      try:
         data = client[0].recv(1024).decode() # block and wait for incoming message
         SERVER_DISPLAY_QUEUE.put("message received from " + client[3] + ": " + data) # debugging
         message = data.split(",", 1) # parse data into list
         # message format: "user,message" if private message, or "BROADCAST,message" for broadcast message, "DISCONNECT" for a controlled close of the client
         
         if message[0] == "SYSTEM": # message to the server (e.g. server command)
            if message[1] == "DISCONNECT":
               client[0].close() # disconnect client
               client[2] = "DISCONNECTED" # flag connection for cleanup
               ClientDisconnect = True # stop looping this receive thread
            else:
               MESSAGE_QUEUE.put([client[3], "SYSTEM", message[1], True]) # queue the message, from this user, to the server
         
         elif message[0] == "BROADCAST":
            MESSAGE_QUEUE.put([client[3], "BROADCAST", message[1], True]) # queue the message, from this user, to all
            
         else: # private message
            userExists = False # flag, in clase the specified username doesn't exist
            
            for user in AUTHENTIC_USERS: # scan the registered user list
               if message[0] == user[0]: # if the specified user is found to exist
                  MESSAGE_QUEUE.put([client[3], message[0], message[1], True]) # queue the message
                  
                  userExists = True # flag that it is a valid username
                  break # stop searching
                  
            if userExists == False: # if the username doesn't exist
               MESSAGE_QUEUE.put(["SYSTEM", client[3], "No such user " + message[0], True]) # report this to the messager
         
      except timeout: # will occur every second
         pass # not a problem, just loop back
         
      except ConnectionResetError: # client closed program
         client[0].close() # disconnect client
         client[2] = "DISCONNECTED" # flag connection for cleanup
         ClientDisconnect = True # stop looping this receive thread

#*********************CSV FUNCTIONS*************************


#Check User CSV: returns list of CSV file contents
def LoadUserList():

    print("In loading user function")
    file = open(UserPath, "r") # open the authentication file for reading
    text = file.read().splitlines() # read in all lines of the file
    file.close() # close the file
    print("File Open")

    for line in text: # itterate through all the lines
        UserValues = line.split(",") # parse out the username and password hash
        UserValues.append(0) # number of failed login attempts
        UserValues.append(time.time()) # filler to initialize the index, later used to note time of lockout
        AUTHENTIC_USERS.append(UserValues) # store the object for later authentication

    # debuging validation, remove once working
    print("Loaded user authentication:")
    for UserValues in AUTHENTIC_USERS:
      print(" + User: " + UserValues[0])
      print("     Pass: " + UserValues[1])


#Write CSV: writes user dictionary to users.CSV file and writes over previous information		
def SaveUserList(Name, Pass):
    
    file = open(UserPath, "a") # open authentication file to permanently save account
    file.write(Name + "," + Pass + "\n") # write the data to file
    file.close()
    
def printUserList():
    
    while not THREADS_JOIN:
        time.sleep(10) # wait five seconds
        try:
           listOfConnections = ""
           for user in USER_CONNECTIONS: # for all online users
               username = user[3]
               if username == 'Guest':
                  username = str(user[1])
               listOfConnections = listOfConnections + username + "\n" # add their name to the list
           SERVER_MESSAGE_QUEUE.put("Online Users:\n" + listOfConnections)
        except timeout:
          pass
			   
        
         

"""         
#returns message list for user        
def MessageCSV():

    messageList = []

    #opens file "message.csv"
    with open(MessagePath, 'r') as csvfile:
        messageReader = csv.reader(csvfile, delimiter= ",")

        #Check for messages with the same username
        for user, message in messageReader:

            messageList.append((user, message))

        #returns list
        return messageList
        
        
        
"""
"""      
#append new messages to CSV file
def AppendMessages(userName, message):

    print('append messages')
    #append each message to csv file
    with open(MessagePath, 'a', newline='') as csvfile:
    
        writer = csv.writer(csvfile, delimiter= ',')
        
        print(message)
        writer.writerow([userName, message])
            
def DeleteOldMessages(list):

    #write over file with unused messages
    #opens file "message.csv"
    with open(MessagePath, 'w', newline='') as csvfile:

        writer = csv.writer(csvfile)

        #Check for messages with the same username
        for name, messageCopy in list:

            writer.writerow([name, messageCopy])
            
            
            
"""
"""
#sends messages to client           
def SendOldMessages(userName, conSocket):

    messagesToKeep = []

    #opens file "message.csv"
    with open(MessagePath, 'r') as csvfile:
        messageReader = csv.reader(csvfile, delimiter= ",")

        #Check for messages with the same username
        for row in messageReader:
            print(row)
            
            #if username is first paramater in row
            if (not row) or (row[0] == userName):
                message = (row[1])
                
                #send message
                sendMessage(conSocket, message)
                print(message)
            elif(row):
                #message not for user
                messagesToKeep.append(row)
        
        #special EOF message
        sendMessage(conSocket, 'EOF')

    return messagesToKeep

    """
    
#*************AUTHENICATE FUNCTIONS**************
    
"""    

def AuthMessageRecipients(recipient):

    #variables
    list = []

    #split recient data into multiple recipients if necesary 
    list = recipient.split('|')
        
    #check that all recipients are correctly spelled
    users = UserDict()
    print(users)
    for name in list:
        if (name not in users.keys()) and (name != 'all'):
            return False
    return True

#Checks for messages with username and sends them to user
def GetNewMessages(userName, conSocket):
    
    print('getting new messages')
    
    #list of messages that are not for the user
    list = []
    list = SendOldMessages(userName, conSocket)

    DeleteOldMessages(list)
        
#writes message to messages.csv
def UpdateMessageList (userName, recipient, message, conSocket):
    print('Updating message list')
    
    bFlag = True
    users = UserDict()
    print(users)

    #authentication
    bFlag = AuthMessageRecipients(recipient)
    if(bFlag == False):
        sendMessage(conSocket, '0')
        print('error, user(s) do not exist!')
    else:
        sendMessage(conSocket, '1')
        print('Authenticated recipients')
        if(recipient == 'all'):
            for everyone in users.keys():
                if(everyone != userName):
                    AppendMessages(everyone, message)
        else:
            # adds messages to csv file
            AppendMessages(recipient, message)
        print('Messages sent')
        
        
def ChatThread(address, conSocket, userName):

    print(userName + ' now in chat')
    
    # --------------------variables---------------------------

    
    print('Chat thread Started')
    
    #Loop for incoming messages, input and outgoing messages
    while(True):

            #get messages from the list for self
            GetNewMessages(userName, conSocket)

            UpdateMessageList(userName, 'all', userName + ' is online', conSocket)

            print("user inputting")
            
            #get input/refresh from user
            input =  recvMessage(conSocket)
            print('User Message: ' + input)

            #update based on input
            if(input == 'close'):
                onlineUsers.remove(userName)
                conSocket.close()
                exit()
            elif(input == 'refresh:>>'):
                sendMessage(conSocket, '1')
            else:
                #Update message list with new written messages
                recipient, message = input.split(',')
                UpdateMessageList(userName, recipient, message, conSocket)

"""
                
                
#authenticates and creates threads
def Authenticate(client):

    try: 
    
      data = client[0].recv(1024).decode() # get authetication data from client
      if data == "": # if the message is blank
         raise ConnectionResetError # assume client closed
         
         
      credentials = data.split(",") # parse data into list
      
      SERVER_MESSAGE_QUEUE_QUEUE.put("Client authenticating with message " + data) # debugging
      SERVER_MESSAGE_QUEUE.put(credentials[0] + "\n" + credentials[1]) # debugging
      
      if credentials[0] == "CREATE": # account creation
         usernameExists = False # flag to be set if the desired username already is taken
         
         for account in AUTHENTICATION: 
            if account[0] == credentials[1]: # if username already exists
               usernameExists = True # set flag
               break # no sense continuing to search
               
         if usernameExists == False: # unused name, create
            AUTHENTICATION.append([credentials[1], credentials[2], 0, time.time()]) # create account in list
            
            SaveUserList(credentials[1], credentials[2])
            
            
            client[2] = "VERIFIED" # flag the connection as verified
            client[3] = credentials[1] # associate the connection with the account name
            
            SERVER_DISPLAY_QUEUE.put("CREATED," + credentials[1]) # debug
            
            client[0].send(("CREATED," + credentials[1]).encode()) # report account created to client
            MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " joined the server", True]) # queue a broadcast that the new user joined
            
            
         else: # username already exists
         
            SERVER_DISPLAY_QUEUE.put("TAKEN," + credentials[1]) # debug
            client[0].send(("TAKEN," + credentials[1]).encode()) # report that the account already exists to the client
            client[0].close() # disconnect client
            client[2] = "DISCONNECTED" # flag connection for cleanup
            
      else: #login
         for account in AUTHENTICATION: #itterate through account list
            if account[0] == credentials[0]: # if username found
               if account[1] == credentials[1]: # and if password hash matches
               
               
                  if account[2] == 4: # if the account is locked out
                     SERVER_DISPLAY_QUEUE.put("ACCOUNTLOCKED," + account[1] + "," + str(time.time() - account[3])) # debug
                     client[0].send(("ACCOUNTLOCKED," + account[1] + "," + str(time.time() - account[3])).encode()) # report lockout to client
                     client[0].close() # disconnect client
                     client[2] = "DISCONNECTED" # flag connection for cleanup
                  else: # if the account is not locked out
                     client[2] = "VERIFIED" # flag the account as validated
                     client[3] = account[0] # associate account name with client
                     account[2] = 0 # reset failed login count
                     SERVER_DISPLAY_QUEUE.put("LOGGEDIN," + account[1]) # debug
                     client[0].send(("LOGGEDIN," + account[1]).encode()) # report the successful login
                     MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " connected to the server", True]) # queue a broadcast that the user is now online
                     
                     
                     
               else: # if incorrect password
                  account[2] += 1 # add one count to the failed login count
                  if account[2] == 4: # if there are now 4 failed logins
                     account[3] = time.time() # note time of 4th failed login
                  SERVER_DISPLAY_QUEUE.put("WRONGPASS," + account[1] + "," + str(account[2])) # debug
                  client[0].send(("WRONGPASS," + account[1] + "," + str(account[2])).encode()) # report the failed login and the failed login count
                  client[0].close() # disconnect client
                  client[2] = "DISCONNECTED" # flag connection for cleanup
               break # stop itterating when the right username has been found
         
         if client[2] == "AUTH": # if the client wasn't disconnected or verified
            SERVER_DISPLAY_QUEUE.put("NOACCOUNT," + credentials[1]) # debug
            client[0].send(("NOACCOUNT," + credentials[0]).encode()) # report that the username wasn't found
            client[0].close() # disconnect client
            client[2] = "DISCONNECTED" # flag connection for cleanup
            
            
            
            
    except ConnectionResetError: # client closed program
        client[0].close() # disconnect client
        SERVER_DISPLAY_QUEUE.put("Disconnect: " + client[1][0] + ":" + str(client[1][1]))
        client[2] = "DISCONNECTED" # flag connection for cleanup
    
    
    
    
    
    """
    #------VARIABLES------

    bFlag = True
    code = int()
    username = ''
    password = ''
    users = UserDict()
    print(users)
    #get code, username and password
    code = recvMessage(connectionSocket)
    print('Code Is:' + code)

    #if code less than 2
    if (int(code) > 2):
        #connectionSocket.send(("Error: wrong paramaters").encode())
        sendMessage(connectSocket, "Error wrong paramaters")
        return (False, '')
    elif (code == '1'): #Returning user
        #while (bFlag):
        print('In Authenticate')
        
        username = recvMessage(connectionSocket)
       
        password = recvMessage(connectionSocket)
        
        #check if username in list. If not in list, send 0
        if(username not in users.keys()):
            sendMessage(connectionSocket, "0")  #sending 0
            print("Username not found. Please try again")
            return (False, loginAttempts)
        elif(users.get(username) != password):
            print('here')
            if(loginAttempts < 4):
                sendMessage(connectionSocket, "0")
                print("Password not found. Please try again")
                loginAttempts += 1
            else :
                sendMessage(connectionSocket, "2")
                loginAttempts = 0
            return (False, loginAttempts)
        else:
            sendMessage(connectionSocket, "1")
            print("User Logged on")
            return (True, username)
    elif(code == '2'):
        print('In Authenticate')
        
        username = recvMessage(connectionSocket)
        
        password = recvMessage(connectionSocket)
        print('new user')
        
        #check if #New User
        if(username not in users):
        
            print('happened')
            #need to put username and password into dictionary
            users[username] = password
            print('happened2')
            WriteCSV(users)
            print('here')
            sendMessage(connectionSocket, "1")
            return (True, username)
        #returning user
        else: 
            #returning user
            if password == users[username]:
                sendMessage(connectionSocket, "1")
                return (True, username)
            else :
                sendMessage(connectionSocket, "0")
                return (False, '')
        
        print('happened2')
            
    #missing paramaters        
    else:
        print("Error: paramaters missing")
        sendMessage(connectionSocket, "1")
        return (False, '')
    return (False, '')
"""
    
    
def acceptConnections():
    while not THREADS_JOIN:
        try:
            print('Worked')
            connectionSocket, addr = SERVER.accept() # block until a connection arrives (timeout 1 second)
            print('Worked')
            USER_CONNECTIONS.append([connectionSocket, addr, "NEW", "Guest"]) # store the connection to the list
            print('Worked')
            MESSAGE_QUEUE.put("New chat member from " + addr[0] + ":" + str(addr[1])) # debugging
            print('Worked')
        except timeout:
            pass # not a problem, just loop back

def Main():

    #variables
    loginAttempts = 0

    print('PythonChat 2018 Server running')
    print(gethostname())  
    print('Listening on port: ' + str(PORT))
    print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

    #get list of Authentic user names
    LoadUserList()
    
    print("Loaded previous users")
    
    
    acceptThread = threading.Thread(target = acceptConnections, args = ()) # generate a thread to accept connections
    acceptThread.daemon = True
    acceptThread.start() # start accepting connections
    THREADS.append(acceptThread) # catalog the thread in the master list
    print("Accepting new connections")
    
    outgoingMessagesThread = threading.Thread(target = sendMessage, args = ()) # generate a thread to send all messages
    outgoingMessagesThread.daemon = True
    outgoingMessagesThread.start() # start asyncronusly sending messages
    THREADS.append(outgoingMessagesThread) # catalog the thread in the master list
    print("Sending all messages")

    printUserListThread = threading.Thread(target = printUserList, args = ()) # generate a thread to list all users on a timer
    printUserListThread.daemon = True
    printUserListThread.start()
    THREADS.append(printUserListThread)
   
    
    print('The server is ready to receive')

    #loop to connect with client sockets
    while True:

    
        for client in CONNECTIONS:
            if client[2] == "NEW": # if we have any new client connections
                client[2] = "AUTH"

                authThread = threading.Thread(target = Authenticate, args = (client,))
                authThread.start() # asyncronusly handle authentication
                THREADS.append(authenticateThread); # catalog the thread in the master list
            
            elif client[2] == "VERIFIED": # newly verified connection, prepare for communication
                client[2] = "ONLINE"
                client[0].settimeout(1) # force recv() to timeout every second so it will join when closing the program
                
                incomingMessagesThread = threading.Thread(target = receiveMessages, args = (client,))
                incomingMessagesThread.start() # asyncronusly handle authentication
                THREADS.append(incomingMessagesThread); # catalog the thread in the master list
            
            elif client[2] == "DISCONNECTED": # if the client has been disconnected and needs to be cleaned up
                if not client[3] == "Guest":
                   MESSAGE_QUEUE.put(["SYSTEM", "BROADCAST", client[3] + " disconnected", True])
                CONNECTIONS.remove(client)
     
        for thread in THREADS: # threads cleanup
            if not thread.isAlive(): # if this thread has finished
                thread.join() # explicitly join it back
                THREADS.remove(thread) # and erase the thread


        while SERVER_MESSAGE_QUEUE.qsize(): # for each message in queue
            text = SERVER_MESSAGE_QUEUE.get() # pop the front message off the queue
            print(text) # print the message
            SERVER_MESSAGE_QUEUE.task_done() # report the task of writing the message done
        
        
        """
        #authenticates and creates thread
        correct = False
        while(not correct):
            correct, userName = Authenticate(connectionSocket, loginAttempts)
            if(isinstance(userName, int)):
                loginAttempts = userName

        print('Got out of Authentication')
        print(correct)
        
        if(correct):
            print(str(addr) + ': ' + str(userName) + ' online')
            print(userName)
            print(addr)

            for userOnline in onlineUsers:
                sendMessage(connectionSocket, userOnline)

            # add username to list of online users
            onlineUsers.append(userName)

            #start thread
            t = threading.Thread(target=ChatThread, args=(addr, connectionSocket, userName))
            Threads.append(t)
            t.start()
        else:
            print('Problem Authenticating')
            connectionSocket.close()
            exit()"""

if __name__ == '__main__':
    ut.cls()
    try:
        print("Entering main")
        Main()
        print("Exiting main")
        
    except Exception as ex:
        print("Hello1")
        #ut.cls()
        print(ex.message)
        
        exit(-1) # return -1 for error during execution
    except KeyboardInterrupt:
    
        print("CTRL-C: Server shutting down")
        print(" - Disconnecting all clients")
    
        for client in CONNECTIONS: # notify all users
            try:
                client[0].send(("SYSTEM: Server closed").encode()) # final message
                client[0].close() # close connection
            except ConnectionResetError: # client closed program
                client[0].close() # close connection
            pass # doesn't matter, on to the next
            
        print(" - All clients disconnected")
        
        #Save authentic user
        SaveUserList()
    
        pass
    finally:
    
        THREADS_JOIN = True # set flag to force threads to end
        for thread in THREADS:
            thread.join()
            THREADS.remove(thread)
    
        #ut.cls()
        print('PythonChat Server cleanup and exit...done!')
        SERVER.close()
        
        exit (0) # return 0 for successful completion

'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''