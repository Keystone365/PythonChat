import queue
import time
#from ClientController import ClientController
import threading
from socket import *

class ServerReciever():

	THREADS = []
	#CLIENT.settimeout(10) #set time out value

	RECIEVE_BUFFER_SIZE = 1024

	running_status = True
	client_connect = False
	delay=6 #<- Change to 30. For debug purposes

	def __init__(self, Client, out_queue, Controller):
		self.CLIENT  = Client
		self.OUT_MESSAGE_QUEUE = out_queue
		self.Controller = controller



	def start(self):

			#print("Loaded previous users")
			sending_thread = threading.Thread(target = send_thread, args = ()) # generate a thread to accept connections
			sending_thread.daemon = True
			sending_thread.start() # start accepting connections
			THREADS.append(sending_thread) # catalog the thread in the master list

			#print("Accepting new connections")
			receiving_thread = threading.Thread(target = self.receive_thread, args = ()) # generate a thread to send all messages
			receiving_thread.daemon = True
			receiving_thread.start() # start asyncronusly sending messages
			self.THREADS.append(receiving_thread) # catalog the thread in the master list

	def send_thread(self):

		while(self.runningStatus):
			self.send_method()

	def send_method(self):

		try:

			'''Sends message according to little endian 
			unsigned int using format characters '<I'''

			# Prefix each message with a 4-byte length (network byte order)
			#'>' means little endian, 'I' means unsigned integer
			#CLIENT.send sends entire message as series of send

			message = self.OUT_MESSAGE_QUEUE.get()

			if message is None:
				pass

			b_message = message.encode()

			length = len(bMessage)

			CLIENT.sendall(struct.pack('>I', length))
			CLIENT.sendall(b_message)
        
		except Exception as er:
			raise er

	def receive_thread(self):

		while(self.running_status):
			self.receive_method()
			pass

	def receive_method(self):

		#unexpected looping is occuring

		try:

			# Read message length and unpack it into an integer
			b_message_length = self.receiveAll(4)
			if bMessageLength is None:
				#print(bMessageLength)
				return

			print(str(b_message_length))

			i_length = int.from_bytes(b_message_length, byteorder= 'big')

			print(str(i_length))
			    
			server_message = self.receive_all(i_length).decode()

			print(str(server_message))
			# Read the message data
			
			self.controller.reply_handler(server_message)

			print("Finished Getting First Message")
			bNo = self.CLIENT.recv(RECIEVE_BUFFER_SIZE)
			print(bNo)

		except Exception as e:
			raise e
    
	'''Helper function to recv a number of bytes or return None if EOF is hit'''
	def receive_all(self, length):


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
		self.running_status = False # set flag to force threads to end

		for thread in self.THREADS:
			thread.join()
			self.THREADS.remove(thread)