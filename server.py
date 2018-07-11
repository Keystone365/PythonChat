#!/usr/bin/env python3
import util.utility as ut
import csv
import threading
import sys
import struct
from datetime import datetime
#from IOBlocking import sendMessage, recvMessage, recvAll 
from socket import *
serverPort = 5006
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
#serverSocket.settimeout(60 * 2) #set time out value
serverSocket.listen(1)

loginAttempts = []

#list of threads
threads = []

#For listing number of user sessions (AC- what is this needed for? Authentication?)
userSessions = []

#list of storing messages
messageList = []

#user dictionary - for reading from and updating CSV file
users = {}

#online user list - not related to CSV file
onlineUsers = []

#paths for CSV files
UserPath = 'util/users.csv'
MessagePath = 'util/messages.csv'


#sends message according to little endian unsigned int using format characters '<I'

def sendMessage(con, message):
    
    
    print ('Sending Message')
    
    # Prefix each message with a 4-byte length (network byte order)
    #'>' means little endian, 'I' means unsigned integer
    #con.send sends entire message as series of send
    
    bMessage = message.encode()
    
    print(bMessage)
    
    length = len(bMessage)
    
    print(length)
    
    #bMessage = message.encode()
    
    #print(message)
    
    con.sendall(struct.pack('>I', length))
    con.sendall(bMessage)

def recvMessage(con):

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


#*********************CSV FUNCTIONS*************************


#Check User CSV: returns dictionary list of CSV file contents
def UserDict():

    #creates dict
    dict = {}
    try:

        #opens CSV "users.csv"
        with open(UserPath, 'r') as csvfile:

            userReader = csv.reader(csvfile, delimiter= ",")

            #fills dict with usernames and passwords
            for row in userReader:
                
                dict[row[0]] = row[1]
                
            print('here')

    except Exception as e:
        print('Error: ' + e.message)
  
    #returns dict
    return dict

#Write CSV: writes user dictionary to users.CSV file and writes over previous information		
def WriteCSV(dataToWrite):

    print('Prepare to add user')
    
    #try to open file
    try:
        with open(UserPath, 'w', newline='') as file:
        
            print('Prepare to add user')

            writer = csv.writer(file)
            
            #write new users into file
            for key, value in dataToWrite.items():

                writer.writerow([key,value])

    except Exception as ex:
        print("unable to open file")
    finally:
        return 0
    
    
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

#*************AUTHENICATE FUNCTIONS**************
            

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


#authenticates and creates threads
def Authenticate(connectionSocket, loginAttempts):

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



def Main():

    #variables
    loginAttempts = 0

    print('PythonChat 2018 Server running')
    print(gethostname())
    print('Listening on port: ' + str(serverPort))
    print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')

    #get list of user names
    users = UserDict()
    print(users)

    #loop to connect with client sockets
    while True:

        #Connect socket
        connectionSocket, addr = serverSocket.accept()
        
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
            threads.append(t)
            t.start()
        else:
            print('Problem Authenticating')
            connectionSocket.close()
            exit()

if __name__ == '__main__':
    ut.cls()
    try:
        Main()
        
    except Exception as ex:
        #ut.cls()
        print(ex.message)
        
        exit(-1) # return -1 for error during execution
    except KeyboardInterrupt:
        pass
    finally:
        #ut.cls()
        print('PythonChat Server cleanup and exit...done!')
        serverSocket.close()
        exit (0) # return 0 for successful completion

'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''