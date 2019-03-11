
#!/usr/bin/env python3
import util.utility as ut
import hashlib
import getpass
import sched
import struct
import time
from datetime import datetime
import tkinter
import queue
import os
import threading
import logging

from socket import *

#NOTES: The Model interacts with the database. Acts as interface between data and the rest of the program

#set up logger
LOG_FORMAT = "%(levelname)s (%(asctime)s): [%(processName)s] - %(message)s"
logging.basicConfig(filename = "util/ClientChatLog.log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger() #root logger

class ClientModel:

	def __init__(self):
		self.clientIP = "localhost"
		self.serverIP = '120.000.1.1'
		self.clientPort = 8192
		self.serverPort = 8192
		self.username = "Anonymous"
		self.BUFSIZ = 1024
		self.CLIENT = socket(AF_INET, SOCK_STREAM)
		self.CLIENT.settimeout(10) #set time out value
		self.CHAT_TAG =  True
		self.THREADS_JOIN = False # Boolean flag for ending threads
		self.THREADS = []
		self.CLIENT_MESSAGE_QUEUE = queue.Queue()
		self.USERNAME = []

	def loginCommand(self, Server, Port, Username):
		self.server = Server
		self.port = Port
		self.username = Username
		print(self.server + ", " + str(self.port) + ", " + self.username)


		#sendMessage(request)



	def calculate(self):
		z = 1 + 1



#messages sent 






###################################################################
##########                  SystemList                  ###########
###################################################################

def SysList():

    '''SysList function for system messages to server'''

    message = 'SYSTEM,LIST'
    CLIENT.send(message.encode())

    # Waiting to receive the list from the server
    recvThread = ReceiveMsgThread(1, 'userList')
    recvThread.start()



def sendMessage(message):

    logger.debug('In sendMessageFunction')
    
    try:

        '''Sends message according to little endian 
        unsigned int using format characters '<I'''

        # Prefix each message with a 4-byte length (network byte order)
        #'>' means little endian, 'I' means unsigned integer
        #CLIENT.send sends entire message as series of send

        bMessage = message.encode()

        length = len(bMessage)

        CLIENT.sendall(struct.pack('>I', length))
        CLIENT.sendall(bMessage)
        
    except Exception as er:
        logger.warning('Exception in sendMessage function')
        logger.warning(er)
        raise er
    
def recvMessage():

    logger.debug('In recvMessage Function')
    
    try:

        # Read message length and unpack it into an integer
        bMessageLength = recieveAll(4)
        
        print(str(bMessageLength))
        
        intLength = int.from_bytes(bMessageLength, byteorder= 'big')
        
        print(str(intLength))
            
        serverMessage = recieveAll(intLength).decode()
        
        print(str(serverMessage))
        # Read the message data
        return serverMessage
    
    except Exception as e:
        s = str(e)
        print(s)
        logger.warning('Exception in recvMessage')
        logger.warning(s)
        raise e
    


def recieveAll(length):

    logger.debug('In recieve all function')

    '''Helper function to recv a number of bytes or return None if EOF is hit'''

    #byte sequence
    data = b''
    
    #Keep recieving message until end of data length
    while (length):
    
        #recieve data
        packet = CLIENT.recv(length)
        
        if not packet: return None
        data += packet
        
        length -= len(packet)
        
    return data
    
#validates user names for messages
def DestinationValidation(command):

    #variables
    message = ''
    chatWith = ''

    #get name of user to chat with
    chatWith = input(
      
         "Please enter username"\
         "or the word \"all\" for everyone, or <username>|<username>"\
         "for multiple people you want to chat with"
     )
    
    #combine username with
    message = chatWith + ',' + userName[0] + ':' + command

    sendMessage(message)
    
    #Get validation from server
    ErrorHandler(recvMessage(), 'DestinationValidation')
    
    
    
###################################################################
##########              Broadcast Message               ###########
###################################################################

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
    
    
###################################################################
##########                  SystemList                  ###########
###################################################################

def SysList():

    '''System '''

    message = 'SYSTEM,LIST'
    CLIENT.send(message.encode())

    # Waiting to receive the list from the server
    recvThread = ReceiveMsgThread(1, 'userList')
    recvThread.start()
    
########################USER AUTHENTICATE FUNCTIONS################################## 

def ReturningUser(userName):
    
    try:
    
        nameStatus = False
        
        while (not nameStatus):
        
            # Asking for the user's credentials
            password = userName + getpass.getpass("Password: ")

            # Assumes the default UTF-8
            hash_object = hashlib.sha256(password.encode()) # hashing the password username and salt
            hash1 = hash_object.hexdigest()  # printing the hashed password and username

            # Sending user's sign in credentials to the server
            cred = 'LOGIN,' + userName + ',' + hash1
            sendMessage(cred)

            # Correct username and password
            reply = recvMessage()

            print(str(reply.split(',')[0]))
            
            if(reply.split(',')[0] == 'LOGGEDIN'):
                nameStatus = True
                pass

            # Wrong password sent
            elif(reply.split(',')[0] == 'WRONGPASS'):
                print('Wrong password. Try Again')

            # User account locked for 5 minutes for trying too many times
            elif(reply.split(',')[0] == 'ACCOUNTLOCKED'):
                print('Account locked.')

            # Username does not exist
            elif(reply.split(',')[0] == 'NOACCOUNT'):
                print('No account exists with this username and password.')
            
    except ConnectionResetError:
        logger.debug('Connection reset error raised in authentication')
        raise ConnectionResetError
    except Exception as er:
        logger.debug(er)
        raise Exception
            

def NewUser(userName):

    '''New user authentication function'''

    logger.debug('In new user function')

    nameStatus = False
    
    try:

        while(nameStatus == False):
        
            #get password input
            password = userName + getpass.getpass("Password: ")
            passwordConf = userName + getpass.getpass("Confirm password: ")
            
            # Assumes the default UTF-8
            hash_object = hashlib.sha256(password.encode()) # hashing the password username and salt
            hash1 = hash_object.hexdigest()  # printing the hashed password and username
           
            # Assumes the default UTF-8
            hash_object1 = hashlib.sha256(passwordConf.encode()) # hashing the password username
            hash2 = hash_object1.hexdigest()  # printing the hashed password and username
            
            logger.debug('hash1= '+ str(hash1))
            logger.debug('hash2= '+ str(hash2))

            # Password confirmation
            if (hash1 == hash2):
                cred = 'CREATE,' + userName + ',' + hash1
                
                logger.debug(cred)

                # Sending the user's credentials to the server
                sendMessage(cred)
                reply = recvMessage()

                logger.debug('Reply from server = ' + reply)
                
                if (reply.split(',')[0] == 'CREATED'): #if username created successfully
                    nameStatus = True
                    print('Welcome '+ userName + '!')
                    USERNAME.append(userName)
                    
                elif(reply.split(',')[0] == ('TAKEN')):
                    print('Username is already taken.  Please try again.')                
            else:
                print('Passwords do not match. Please Re-Enter.')
                   
    except Exception as er:
        logger.debug('Error raised in new user function: ' + er)
        raise Exception

    
def Authenticate():

    '''Function for authenticating returning or new clients with server'''

    logger.info('In Authenticate function')
    
    #NewUser user name and password
    userStatus = 0
    username = ''
    
    #Get status as either returning user or new user
    while(userStatus != 1) and (userStatus != 2): #error correction
      
        try:
            userStatus = int(input('Enter 1 if signing up or 2 for returning user: '))
            if (userStatus != 1) and (userStatus != 2):
                print('Wrong Code, Please enter 2 if you are a returning user, otherwise enter 1.\n')
                
        except ValueError:
            print('Not a proper number.')
    
    # Asking for the username
    while (not username) or (',' in username) or ('|' in username): 
        username = input('Username: ')
        if (',' in username) or ('|' in username):
            print("Your username should not contain a comma , or a pipe |:")
            
    # Direct to either new user function or returning user function
    if(userStatus == 1):
        logger.debug(userStatus)
        
        logger.debug("Entering NewUser function")
        NewUser(username)
    elif(userStatus == 2):
        logger.debug("Entering ReturningUser function")
        ReturningUser(username)
        

######################################THREADS##############################################
def receive():
    #Handles receiving of messages.
    while True:
        try:
            msg = recvMessage()
            
            print(msg)
            #CLIENT_MESSAGE_QUEUE.put(msg)
            
        except OSError:  # Possibly client has left the chat.
            break
            
def ExitChoice():

    '''Handle exit choice decisions'''

    correctChoice = False
    
    while not correctChoice:
   
        try:
            ut.cls()
            print('Are you sure you want to exit the chat program?')
            print('(1 for yes, 2 for no)')

            user_choice = int(input('Answer: '))
            if (user_choice != 1) and (user_choice != 2):
                raise ValueError

            if(user_choice == 1):
                # disconnects the connection
                return True
                
            elif(user_choice == 2):
                return False

        except ValueError:
            print('Incorrect input. Please try again')
            
            
        
def Chat():

    while True:
        print('Who would you like to chat with?')
        username = input('Username: ')
        usermessage = input('What would you like to say?:')

        sendMessage('PRIVATE,' + username + ',' + usermessage)
        
        
    

    
        
        
def messageHandler():
    
    '''Handle commands for logged in customers'''

    EXIT = False

    while not EXIT:
        ut.cls()
        
        #print('What would you like to do?')
        #print('     Enter 1 to see our online users')
        #print('     Enter 2 to chat with a user')
        #print('     Enter 3 to exit this screen')
        
        
        
        try:
            userStatus = userChoice = int(input('Answer: '))
            
            if (userStatus < 0) or (userStatus > 4):
                raise ValueError   
            else:
                
                if(user_choice == 1):
                    # Ask server for a list of users
                    SysList()
                    os.system("PAUSE")

                if(user_choice == 2):
                    Chat(username)

                if(user_choice == 3):
                    EXIT = ExitChoice()


                #ut.cls()
        except ValueError:
            print('That is an invalid input: please try again...')
            os.system('PAUSE')
            
        
        
        
    
#######################################MAIN###############################################3
    
def Main():


    

    
    
    

            
            
    
    #logger.info('In Authenticate method')
    
    ##authenticate user
    #Authenticate()
    
    #logger.info('Out of Authenticate Method')
    
    #print("Loaded previous users")
    sendMessageThread = threading.Thread(target = Chat, args = ()) # generate a thread to accept connections
    sendMessageThread.daemon = True
    sendMessageThread.start() # start accepting connections
    THREADS.append(sendMessageThread) # catalog the thread in the master list
    logger.info('Send message thread 1 running')
    
    #print("Accepting new connections")
    readMessageThread = threading.Thread(target = receive, args = ()) # generate a thread to send all messages
    readMessageThread.daemon = True
    readMessageThread.start() # start asyncronusly sending messages
    THREADS.append(readMessageThread) # catalog the thread in the master list
    logger.info('Recieve message thread 2 running')



