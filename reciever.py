
import queue
import time
import threading
from socket import *

class Reciever():

	THREADS = []
	

	#client socket setup
	CLIENT = socket(AF_INET, SOCK_STREAM)
	#CLIENT.settimeout(10) #set time out value

	recieveBufferSize = 1024
	sendBufferSize = 1024

	runningStatus = True
	clientConnect = False
	delay=6 #<- Change to 30. For debug purposes

	def __init__(self, in_queue, out_queue):
		self.REPLY_QUEUE = in_queue
		self.REQUEST_QUEUE = out_queue

	def Start(self, server, port):
		self.HOST = server
		self.PORT = port
		self.ADDR = (self.HOST, self.PORT)


		#try to connect to server
		closeAttempt= time.time() + 30

		while ((not self.clientConnect) and (time.time() < closeAttempt)):
			try:
				print('Atempting to Connect...')
				self.CLIENT.connect(self.ADDR)
				#self.CLIENT.setblocking(0)
				self.clientConnect = True

			except ConnectionRefusedError:
				pass
			except Exception as er:
				print('Error thrown while connecting:')
				raise er

		if self.clientConnect == False:
			print('Connection with server failed. Please try again at a different time.')
			return -1
		else:
			print('Connected to server.')

			#print("Loaded previous users")
			'''sendingThread = threading.Thread(target = Send_Thread, args = ()) # generate a thread to accept connections
			sendingThread.daemon = True
			sendingThread.start() # start accepting connections
			THREADS.append(sendMessageThread) # catalog the thread in the master list

			'''#print("Accepting new connections")
			receivingThread = threading.Thread(target = self.Receive_Thread, args = ()) # generate a thread to send all messages
			receivingThread.daemon = True
			receivingThread.start() # start asyncronusly sending messages
			self.THREADS.append(receivingThread) # catalog the thread in the master list


	def Send_Thread(self, message):



		while(self.runningStatus):
			print(self.runningStatus)
			self.SendMethod()



	def SendMethod(self):
		
		bMessage = REQUEST_QUEUE.get()

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

	def Receive_Thread(self):

		while(self.runningStatus):
			self.ReceiveMethod()
			pass

	def ReceiveMethod(self):

		#unexpected looping is occuring

		try:

			# Read message length and unpack it into an integer
			bMessageLength = self.receiveAll(4)
			if bMessageLength is None:
				#print(bMessageLength)
				return

			print(str(bMessageLength))

			intLength = int.from_bytes(bMessageLength, byteorder= 'big')

			print(str(intLength))
			    
			serverMessage = self.receiveAll(intLength).decode()

			print(str(serverMessage))
			# Read the message data
			self.REPLY_QUEUE.put(str(serverMessage))

			print("Finished Getting First Message")
			bNo = self.CLIENT.recv(1056)
			print(bNo)

		except Exception as e:
			raise e
    

	'''Helper function to recv a number of bytes or return None if EOF is hit'''
	def receiveAll(self, length):


		#byte sequence
		data = b''

		#Keep recieving message until end of data length
		while (length):

			#recieve data
			packet = self.CLIENT.recv(length)

			if not packet: return None
			data += packet

			length -= len(packet)

		return data

	def close(self):
		self.runningStatus = False # set flag to force threads to end

		for thread in self.THREADS:
			thread.join()
			self.THREADS.remove(thread)
			