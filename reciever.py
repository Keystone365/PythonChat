
import queue

class Reciever:

	THREADS = []
	MESSAGE_QUEUE = queue.Queue()

	#client socket setup
	CLIENT = socket(AF_INET, SOCK_STREAM)
	CLIENT.settimeout(10) #set time out value

	def __init__(self):
		self.bufferSize = 1024
		self.sendbufferSize = 1024

	def Start(self):
			   #print("Loaded previous users")
		sendingThread = threading.Thread(target = Chat, args = ()) # generate a thread to accept connections
		sendingThread.daemon = True
		sendingThread.start() # start accepting connections
		THREADS.append(sendMessageThread) # catalog the thread in the master list

		#print("Accepting new connections")
		receivingThread = threading.Thread(target = receivingMethod, args = ()) # generate a thread to send all messages
		recievingThread.daemon = True
		recievingThread.start() # start asyncronusly sending messages
		THREADS.append(readMessageThread) # catalog the thread in the master list

	def receivingMethod(self):


	def sendingMessage(self, message):
		MESSAGE_QUEUE.put(message)

	def sendingMethod(self):
		
		bMessage = MESSAGE_QUEUE[0]

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
	        raise er

	def close(self):