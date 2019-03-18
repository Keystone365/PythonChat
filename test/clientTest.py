#!/usr/bin/env python3
import hashlib
import getpass
from socket import *
serverPort = 5006
clientSocket = socket(AF_INET, SOCK_STREAM)


def Main():
    
    
    serverName = gethostname() #if on same computer uncomment this line
    
    clientSocket.connect((serverName, serverPort))
    print('here')
    
    while(True):
        print('here')
    
        name = input("Enter test input: ") #inserting user name
        clientSocket.send((name).encode())
        
        bR = input('recieve messages? 1 for true: ')
        if (bR == 1):
            input = clientSocket.recv(1024).decode()
            print(input)
        if (bR == 'exit'):
            clientSocket.close()
            exit()
    
 
    
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