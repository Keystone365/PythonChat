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
		sending_thread.start()
		self.THREADS.append(sending_thread)

		# generate a thread to recieve messages
		receiving_thread = threading.Thread(target = self.receive_thread, args = ()) 
		receiving_thread.daemon = True
		receiving_thread.start()
		self.THREADS.append(receiving_thread)

	def message(self, string):

		"""Method appends message to outgoing queue for thread"""
		
		self.OUT_MESSAGE_QUEUE.put(string)
		pass

	def send_thread(self):

		'''Send thread method. Sends message according to little endian 
		unsigned int using format characters '<I

		Prefix message with a 4-byte length (network byte order)
		'>' means little endian, 'I' means unsigned integer.'''

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

		"""Thread Method for recieving message from server."""

		try:
			while(self.b_running_status):

				# Read message length and unpack it into an integer
				b_message_length = self.receive_all(4)
				if b_message_length is None:
					continue

				i_length = int.from_bytes(b_message_length, byteorder= 'big')
				server_message = self.receive_all(i_length).decode()
				self.controller.reply_handler(server_message)

		except ConnectionResetError as con_error:
			self.controller.reply_handler("User has disconnected")
			self.close()

		except Exception as e:
			print("Exception occured in recieve thread")
			raise e
    
	def receive_all(self, length):

		'''Helper function to recv a number of bytes or return None if EOF is hit'''

		data = b''
		while (length):

			packet = self.CLIENT.recv(length)
			if not packet: return None
			data += packet
			length -= len(packet)

		return data

	def close(self):

		'''Function for seting flag to closing reciever threads'''

		if(self.b_running_status):
			self.b_running_status = False