
import queue
import time
#from ClientController import ClientController
import threading
import struct
from socket import *

class ClientReciever():

	THREADS = []
	CLIENT = socket(AF_INET, SOCK_STREAM)

	OUT_MESSAGE_QUEUE = queue.Queue()

	i_RECIEVE_BUFFER_SIZE = 1024
	i_SEND_BUFFER_SIZE = 1024

	b_running_status = True
	b_client_connect = False
	i_CONNECT_DELAY=6 

	s_USERNAME = ""

	def __init__(self, controller):
		self.controller = controller

	def start(self, server, port, username):
		self.HOST = server
		self.PORT = port
		self.ADDR = (self.HOST, self.PORT)

		#try to connect to server
		i_close_time= time.time() + self.i_CONNECT_DELAY

		while ((not self.b_client_connect) and (time.time() < i_close_time)):
			try:
				print('Atempting to Connect...')
				self.CLIENT.connect(self.ADDR)
				self.b_client_connect = True
				print('Connected To Server')

			except ConnectionRefusedError:
				pass
			except Exception as er:
				print('Error thrown while connecting:')
				raise er

		if (self.b_client_connect == False):
			print('Connection with server failed. Please try again at a different time.')
			return self.b_client_connect
		else:
			self.USERNAME = username

			self.OUT_MESSAGE_QUEUE.put("User has Connected!")

			#print("Loaded previous users")
			sending_thread = threading.Thread(target = self.send_thread, args = ()) # generate a thread to accept connections
			sending_thread.daemon = True
			sending_thread.start() # start accepting connections
			self.THREADS.append(sending_thread) # catalog the thread in the master list

			#print("Accepting new connections")
			receiving_thread = threading.Thread(target = self.receive_thread, args = ()) # generate a thread to send all messages
			receiving_thread.daemon = True
			receiving_thread.start() # start asyncronusly sending messages
			self.THREADS.append(receiving_thread) # catalog the thread in the master list

			return self.b_client_connect

	def message(self, string):
		self.OUT_MESSAGE_QUEUE.put(string)
		pass

	def send_thread(self):
		while(self.b_running_status):
			self.send_method()

	def send_method(self):

		'''
		Sends message according to little endian 
		unsigned int using format characters '>I

		Prefix each message with a 4-byte length (network byte order)
		'>' means little endian, 'I' means unsigned integer
		CLIENT.sendall sends entire message as series of send commands. '''

		try:

			s_message = self.OUT_MESSAGE_QUEUE.get()
			if s_message is None:
				pass

			b_message = s_message.encode()
			i_length = len(b_message)

			self.CLIENT.sendall(struct.pack('>I', i_length))
			self.CLIENT.sendall(b_message)
		except ConnectionResetError as conError:
			pass
		except Exception as er:
			print("Exception occured in recieve thread")
			print (str(er))
			raise er

	def receive_thread(self):

		while(self.b_running_status):
			self.receive_method()
			pass

	def receive_method(self):
		try:

			b_length = self.receive_all(4)
			if b_length is None:
				return

			i_length = int.from_bytes(b_length, byteorder= 'big')
			s_message = self.receive_all(i_length).decode()
			
			self.controller.reply_handler(s_message)

		except ConnectionResetError as conError:
			self.controller.error_handler("Connection Error",
				"Server has disconnected. Program will now close, please try again at another time.")

		except Exception as e:
			print("Exception in Recieve Method")
			raise e

    
	def receive_all(self, length):

		'''Helper function to recv a number of bytes or return None if EOF is hit'''

		#byte sequence
		b_data = b''

		while (length):
			s_packet = self.CLIENT.recv(length)
			if not s_packet: 
				return None

			b_data += s_packet
			length -= len(s_packet)
		return b_data

	def close(self):

		'''Function for closing reciever'''

		if(self.b_running_status):
			self.b_running_status = False
			