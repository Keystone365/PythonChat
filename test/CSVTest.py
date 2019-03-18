#!/usr/bin/env python3
import util.utility as ut
import csv

import sys
from socket import *
serverPort = 5006
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

#Check CSV: returns dictionary list of CSV file contents
def CheckCSV(fileName):

	#creates dict
	list = {}
	
	#opens CSV "users.csv"
	with open(fileName, 'r') as csvfile:
		userReader = csv.reader(csvfile, delimiter= ",")
		
		#fills dict with usernames and passwords
		for userName, password in userReader:
			list[userName] = password
		
		#returns dict
		return list

#Check Username in CSV: returns hash if found, false if not
def CheckUserName(userName, Dict):
	
	#Try to get value of hash from dicionary
	try:
		hash = Dict[userName]
		return true;
		
	except Exception as ex:
		return false
		
	finally:
		return false
		
def MakeAccount(fileName, Dict):

	#WriteCSV(Dict,fileName)
		
		
#GetHash: returns hash
def GetHash(fileName, Dict):

	#user name flag
	#UserNameBool = True
	
	#while UserNameBool:
		
	#Check Username
	username = input("Please enter username for look up:")
		
	#if username not on list
	if (username not in Dict):
		
		#ask for new account?
		print("This username is not in our database.")
		return "false"
		
		
	#username
	else:
		print(Dict[username])
		#hash = GetUserName(username, fileName)
		return Dict[username]
	

		
		
def WriteCSV(dataToWrite, fileName):

	file = open(fileName, 'w', newline='') 

	with file:

		writer = csv.writer(file)
    
		for key, value in dataToWrite.items():

			writer.writerow([key,value])	
			
def YNInput(choice):

	yes = {'yes', 'y', 'ye', ''}
	no = {'no', 'n'}
	exitProgram = {'c'}
	
	while True:
	
		#check choice
		if(choice in yes):
			return true
		elif(choice in no):
			return false
		elif(choice in exitProgram):
			exit(0)
		else:
			choice = input("Please answer Y or N:")
			
			
GetNewMessages(username, conSocket):

	#list of messages that are not for the user
	list = []

	#opens file "message.csv"
    with open(fileName, 'r') as csvfile:
        messageReader = csv.reader(csvfile, delimiter= ",")

        #Check for messages with the same username
        for user, message in messageReader:
		
			#if username is first paramater in row
            if user == userName:
				
				#send message
				conSocket.send(message)
			
			else :
				
				#message not for user
				list.append((user, message))
				
				
	#write over file with unused messages
	#opens file "message.csv"
    with open(fileName, 'r') as csvfile:
	
		writer = csv.writer(file)

        #Check for messages with the same username
        for name, messageCopy in list:

            writer.writerow([name, messageCopy])	

		
		
def Main():
	print('PythonChat Server startup in progress...')

	fileName = 'util/users.csv'
	
	#Check List
	list = CheckCSV(fileName)
	#print (list)
	
	#write list
	#list["newKey"] = "newValue"
	#WriteCSV(list, fileName)
	#print (list)
	
	hash = GetHash(fileName, list)
	
	while True:
		connectionSocket, addr = serverSocket.accept()
		sentence = connectionSocket.recv(1024).decode()
		connectionSocket.send(str.upper(sentence).encode())
		sys.stdout.write(sentence)
		if(sentence == 'close') :
			connectionSocket.send('close'.encode())
			connectionSocket.close()
			break
			


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
		exit (0) # return 0 for successful completi