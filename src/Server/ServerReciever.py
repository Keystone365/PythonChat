import queue
import time
#from ClientController import ClientController
import threading
import struct
from socket import *

class ServerReciever():

	THREADS = []
	OUT_MESSAGE_QUEUE = queue.Queue()

	RECIEVE_BUFFER_SIZE = 1024
	b_running_status = True
	client_connect = False
	delay=6

	def __init__(self, client, controller):
		self.CLIENT  = client
		self.controller = controller

	def start(self):

		"""Start process for sending and recieving threads"""

		self.b_running_status = True

		# generate a thread to send messages
		sending_thread = threading.Thread(target = self.send_thread, args = ()) 
		sending_thread.daemon = True
		sending_thread.start() # start accepting connections
		self.THREADS.append(sending_thread) # catalog the thread in the master list
		print("Sending Thread Created")

		# generate a thread to recieve messages
		receiving_thread = threading.Thread(target = self.receive_thread, args = ()) 
		receiving_thread.daemon = True
		receiving_thread.start() # start asyncronusly sending messages
		self.THREADS.append(receiving_thread) # catalog the thread in the master list
		print("Recieving Thread Created")

	def message(self, string):
		self.OUT_MESSAGE_QUEUE.put(string)
		pass

	def send_thread(self):

		'''Sends message according to little endian 
		unsigned int using format characters '<I

		Prefix each message with a 4-byte length (network byte order)
		'>' means little endian, 'I' means unsigned integer
		CLIENT.send sends entire message as series of send'''

		try:
			while(self.b_running_status):

				message = self.OUT_MESSAGE_QUEUE.get()

				if message is None:
					continue

				b_message = message.encode()

				length = len(b_message)

				self.CLIENT.sendall(struct.pack('>I', length))
				self.CLIENT.sendall(b_message)

		except ConnectionResetError as con_error:
			pass
		except Exception as er:
			raise er

	def receive_thread(self):
		try:
			while(self.b_running_status):

				# Read message length and unpack it into an integer
				b_message_length = self.receive_all(4)

				if b_message_length is None:
					continue

				print(str(b_message_length))

				i_length = int.from_bytes(b_message_length, byteorder= 'big')

				print(str(i_length))

				server_message = self.receive_all(i_length).decode()

				print(str(server_message))
				# Read the message data

				self.controller.reply_handler(server_message)

				#b_no = self.CLIENT.recv(self.RECIEVE_BUFFER_SIZE)
				#print(b_no)

		except ConnectionResetError as con_error:
			self.controller.reply_handler("User has disconnected")
			self.close()

		except Exception as e:
			print("Exception occured in recieve thread")
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

		'''Function for closing reciever'''

		if(self.b_running_status):
			self.b_running_status = False