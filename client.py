#!/usr/bin/env python3
import hashlib
import getpass
import sched
import struct
import time
import tkinter
from socket import *

serverName = gethostname() #if on same computer uncomment this line
#serverName = 'cs-vus-00.principia.local' #if on remote server uncomment this line

serverPort = 5006
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(5) #set time out value

CHAT_TAG =  True

threadList  = ['SendThread', 'ReceiveThread']
threadQueue = queue.Queue(10)
sendThreads = []
recvThreads = []

userName = []

#sends message according to little endian unsigned int using format characters '<I'

def ErrorHandler(errorCode, nameOfFunction) :
    if(nameOfFunction == 'DestinationValidation') :
        if(errorCode == '0') :
            message = input("User doesn't exist! Please enter a message: ")
            DestinationValidation(message)
        elif(errorCode == '1') :
            print('Message Sent')
    elif(nameOfFunction == 'Returning') :
        if(errorCode == '0') :
            print('Error: problem with username/password. Please retry\n')
            Returning()
        elif errorCode == '1':
            print("Welcome Back Returning user")
        elif errorCode == '2':
            print("timeout too many logon attempts, you are locked out for five minutes")
            time.sleep(300)
            Returning()
    elif(nameOfFunction == 'NewUser') :
        if(errorCode == '0') :
            print('You cant change your password that easily billy!\n')
            NewUser()
        elif errorCode == '1':
            print("Welcome back -new- user")
        elif errorCode == '2':
            print("timeout too many logon attempts, you are locked out for five minutes")
            time.sleep(300)
            NewUser()

#sends message according to little endian unsigned int using format characters '<I'

def sendMessage(message):
    
    # Prefix each message with a 4-byte length (network byte order)
    #'>' means little endian, 'I' means unsigned integer
    #clientSocket.send sends entire message as series of send
    
    bMessage = message.encode()
    
    length = len(bMessage)

    clientSocket.sendall(struct.pack('>I', length))
    clientSocket.sendall(bMessage)

def recvMessage():

    # Read message length and unpack it into an integer
    MessageLength = recieveAll(4)
    
    i = int.from_bytes(MessageLength, byteorder= 'big')
        
    x = recieveAll(i).decode()
    # Read the message data
    return x

# Helper function to recv a number of bytes or return None if EOF is hit
def recieveAll(length):
    #byte sequence
    data = b''
    
    while (length):
    
        #recieve data
        packet = clientSocket.recv(length)
        
        if not packet: return None
        data += packet
        
        length -= len(packet)
    return data



#prints messages sent from server, ends loop when special message sent            
def GetMessages():

    bFlag = True
    
    while bFlag:

        message = recvMessage()
        
        if (message == 'EOF'): bFlag = False
        else: print(message)
    
#validates user names for messages
def DestinationValidation(command):

    #variables
    message = ''
    chatWith = ''

    #get name of user to chat with
    chatWith = input(
     """\ 
         Please enter <username> (where <username> is the username of the person you want to send a message to),
         or the word <all> for everyone, or <username>|<username> for multiple people you want to chat with\
     """)
    
    #combine username with
    message = chatWith + ',' + userName[0] + ':' + command

    sendMessage(message)
    
    #Get validation from server
    ErrorHandler(recvMessage(), 'DestinationValidation')


def GetUserInfo():

    #variables
    name = ''
    password = ''

    name = input("what is your user name: ") #inserting user name
    
    while ',' in name or '|' in name:
        name = input("Your username should not contain a comma , or a pipe |:")
        
    #get password
    password = GetPassword(name)
    return (name, password)
        
        
   #returns password     
def GetPassword(name):

    #variables
    bFlag = True

    while(bFlag):
    
        #get password input
        pw = getpass.getpass("Enter Password: ") #inserting passsword
        mystring = name + pw
        
        # Assumes the default UTF-8
        hash_object = hashlib.sha256(mystring.encode()) # hashing the password username and salt
        hash1 = hash_object.hexdigest()  # printing the hashed password and username
        pw2 = getpass.getpass("Re-Enter Password: ") # Confirming password

        mystring1 = name + pw2
        
        # Assumes the default UTF-8
        hash_object1 = hashlib.sha256(mystring1.encode()) # hashing the password username
        hash2 = hash_object1.hexdigest()  # printing the hashed password and username
        
        #if both passwords entered are the same
        if (hash1 == hash2):
            print('Welcome '+ name + '!')
            bFlag = False
        else:
            print('Passwords do not match. Please Re-Enter.')
    
    #return password
    return hash1

def Returning():
    
    #get name and password
    name, hash1 = GetUserInfo()
    sendMessage('1')
    
    sendMessage(name)
    sendMessage(hash1)
    ErrorHandler(recvMessage(), 'Returning')
    userName.append(name)

def NewUser():
        
        #get name and password
        name, hash1 = GetUserInfo()

        sendMessage('2')

        sendMessage(name)

        sendMessage(hash1)

        ErrorHandler(recvMessage(), 'NewUser')
            
        userName.append(name)
            
#command could be message, wait or close
def ChatRoulette(command) :

    #if refresh
    if command == 'wait':
        time.sleep(2)
        sendMessage('refresh:>>')
        message = recvMessage()

        if message != '0':
            return True
        else:
            print('Server offline')
            return False
        
    #if message
    elif (command != 'close'):
    
        #validate message
        DestinationValidation(command)
        return True
    #if command is close

    sendMessage('close')
    return False
    
    
def Main():
    
    serverName = gethostname() #if on same computer uncomment this line
    #serverName = 'cs-vus-00.principia.local' #if on remote server uncomment this line

    #try to connect to server
    try:
        clientSocket.connect((serverName, serverPort))
    except:
        print('Unable to make connection. Server not online. Please try again later.')
        return 1;
    
    #NewUser user name and password
    userStatus = input('Enter 2 if you are a returning user, otherwise enter 1')
    while(userStatus != '2') and (userStatus != '1'):
        userStatus = input('Wrong Code, Please enter 2 if you are a returning user, otherwise enter 1')
    if(userStatus == '1'):
        NewUser()
    elif(userStatus == '2'):
        Returning()
    else :
        print('You Done messed up A-aron')
    
    Chat()

def Chat():
    bFlag = True
    
    while bFlag:
        #get messages from csv file
        GetMessages()
        #Ask User to enter the name of the person they want to chat with
        cmd = input("Please enter a message you want to send, the word 'wait' or the word 'close' to quit: ")
        bFlag = ChatRoulette(cmd);
        
    clientSocket.close()
    
if __name__ == '__main__':
    #ut.cls()
    try:
        Main()
    except Exception as ex:
        #ut.cls()
        print(ex.message)
        exit(-1)  # return -1 for error during execution
    except KeyboardInterrupt:
        pass
    finally:
        #ut.cls()
        print('PythonChat Client cleanup and exit...done!')
        clientSocket.close()
        exit(0)  # return 0 for successful completion


'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''
