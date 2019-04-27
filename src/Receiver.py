import queue
import threading
import time
import struct
from socket import *

class Receiver():

	THREADS = []

	b_running_status = True
	b_connect = False
	i_CONNECT_DELAY=6 

	i_RECIEVE_BUFFER_SIZE = 1024
	i_SEND_BUFFER_SIZE = 1024

	OUT_MESSAGE_QUEUE = queue.Queue()

	def __init__():
		pass

	def connect():
		pass

	def authenticate():
		pass

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
	
	def receive_all(self, length):

		'''Helper function to recv a number of bytes or return None if EOF is hit'''

		data = b''
		while (length):

			packet = self.CLIENT.recv(length)
			if not packet: return None
			data += packet
			length -= len(packet)

		return data

	def send_method(self, s_message):

		'''
		Sends message according to little endian 
		unsigned int using format characters '>I

		Prefix each message with a 4-byte length (network byte order)
		'>' means little endian, 'I' means unsigned integer
		CLIENT.sendall sends entire message as series of send commands. '''

		b_message = s_message.encode()
		i_length = len(b_message)

		self.CLIENT.sendall(struct.pack('>I', i_length))
		self.CLIENT.sendall(b_message)

	def receive_method(self):

		'''Method for recieving messages'''

		# Read message length and unpack it into an integer
		b_message_length = self.receive_all(4)
		if b_message_length is None:
			return None

		i_length = int.from_bytes(b_message_length, byteorder= 'big')
		server_message = self.receive_all(i_length).decode()
		return server_message

	def close(self):

		'''Function for seting flag to closing reciever threads'''

		if(self.b_running_status):
			self.b_running_status = False