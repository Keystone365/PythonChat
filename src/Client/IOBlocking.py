import util.utility as ut
import sys
from socket import *

#sends message according to little endian unsigned int using format characters '<I'

def sendMessage(con, message):

    # Prefix each message with a 4-byte length (network byte order)
    #'>' means little endian, 'I' means unsigned integer
    #con.send sends entire message as series of send
    bMessage = message.encode()
    
    bMessage = struct.pack('>I', len(bMessage)) + bMessage
    con.sendall(bMessage)

def recvMessage(con):

    # Read message length and unpack it into an integer
    rawMessageLength = recvAll(con, 4)
    
    #returns None if no message length
    if not rawMessageLength:
        return None
        
    messageLength = struct.unpack('>I', rawMessageLength)[0] 
    # Read the message data
    return recvall(sock, messageLength)

# Helper function to recv a number of bytes or return None if EOF is hit
def recvAll(con, length):
    
    #byte sequence
    data = b''
    
    while len(data) < length
    
        #recieve data
        packet = con.recv(length - len(data))
        if not packet:
            return None
        data += packet
        
    #return data
    return data.decode()