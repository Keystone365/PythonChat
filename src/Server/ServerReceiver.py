
from src.Receiver import *

class ServerReceiver(Receiver):

	delay=6

	def __init__(self, socket, controller):
		
		self.controller = controller
		self.SERVER = socket

	def connect(self):

		try:
			connection_socket, addr = self.SERVER.accept()
			self.b_connect = True
			self.CLIENT = connection_socket
			self.address = addr
		except timeout:
			pass
		except Exception as er:
			raise er

		return self.b_connect

	def authenticate(self):
		s_message = self.receive_method()

		l_message = s_message.split(',')
		self.USERNAME = l_message[0]
		self.PASSWORD = l_message[1]
		self.send_method('Username: ' + self.USERNAME + ', Password: ' + self.PASSWORD)
		self.controller.reply_handler("m>" + self.USERNAME + " has connected.")
		

	def send_thread(self):

		'''Send thread method. Sends message according to little endian 
		unsigned int using format characters '<I

		Prefix message with a 4-byte length (network byte order)
		'>' means little endian, 'I' means unsigned integer.'''

		try:
			while(self.b_running_status):

				s_message = self.OUT_MESSAGE_QUEUE.get()
				if s_message is None:
					continue

				self.send_method(s_message)

		except ConnectionResetError as con_error:
			pass
		except Exception as er:
			raise er

	def receive_thread(self):

		"""Thread Method for recieving message from server."""

		try:
			while(self.b_running_status):
				s_message = self.receive_method()
				self.controller.reply_handler(s_message)

		except ConnectionResetError as con_error:
			self.controller.reply_handler("m>" + self.USERNAME + " has disconnected.")
			self.close()

		except Exception as e:
			print("Exception occured in recieve thread")
			raise e