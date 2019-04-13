import queue
import time
#from ClientController import ClientController
import threading
from socket import *

class ServerReciever():

	THREADS = []
	RECIEVE_BUFFER_SIZE = 1024
	running_status = True
	client_connect = False
	delay=6

	def __init__(self, client, out_queue, controller):
		self.CLIENT  = client
		self.OUT_MESSAGE_QUEUE = out_queue
		self.controller = controller

	def start(self):

			"""Start process for sending and recieving threads"""

			# generate a thread to send messages
			sending_thread = threading.Thread(target = send_thread, args = ()) 
			sending_thread.daemon = True
			sending_thread.start() # start accepting connections
			self.THREADS.append(sending_thread) # catalog the thread in the master list

			# generate a thread to recieve messages
			receiving_thread = threading.Thread(target = self.receive_thread, args = ()) 
			receiving_thread.daemon = True
			receiving_thread.start() # start asyncronusly sending messages
			self.THREADS.append(receiving_thread) # catalog the thread in the master list

	def send_thread(self):

		'''Sends message according to little endian 
		unsigned int using format characters '<I

		Prefix each message with a 4-byte length (network byte order)
		'>' means little endian, 'I' means unsigned integer
		CLIENT.send sends entire message as series of send'''

		try:
			while(self.running_status):

				message = self.OUT_MESSAGE_QUEUE.get()

				if message is None:
					continue

				b_message = message.encode()

				length = len(bMessage)

				CLIENT.sendall(struct.pack('>I', length))
				CLIENT.sendall(b_message)
		except Exception as er:
			raise er

	def receive_thread(self):
		try:
			while(self.running_status):

				# Read message length and unpack it into an integer
				b_message_length = self.receiveAll(4)

				if bMessageLength is None:
					continue

				print(str(b_message_length))

				i_length = int.from_bytes(b_message_length, byteorder= 'big')

				print(str(i_length))

				server_message = self.receive_all(i_length).decode()

				print(str(server_message))
				# Read the message data

				self.controller.reply_handler(server_message)

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