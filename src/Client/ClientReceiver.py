
from src.Receiver import *

class ClientReceiver(Receiver):

	s_USERNAME = ""

	def __init__(self, socket, controller):
		self.controller = controller
		self.CLIENT = socket
		self.b_connect = False

	def connect(self, server, port):
		self.HOST = server
		self.PORT = port
		self.ADDR = (self.HOST, self.PORT)

		#try to connect to server
		i_close_time= time.time() + self.i_CONNECT_DELAY

		print('b_connect is equal to: '+ str(self.b_connect))

		while ((not self.b_connect) and (time.time() < i_close_time)):
			try:
				print('Atempting to Connect...')
				self.CLIENT.connect(self.ADDR)
				self.b_connect = True
				print('Connected To Server')

			except ConnectionRefusedError:
				pass
			except Exception as er:
				print('Error thrown while connecting:')
				raise er

		if (self.b_connect == False):
			print('Connection with server failed. Please try again at a different time.')
			return self.b_connect
		else:
			self.OUT_MESSAGE_QUEUE.put("User has Connected!")

			return self.b_connect

	def authenticate(self, username, password):

		'''Sends username and password to server, recieves authentication confirmation. Returns boolean value.'''

		self.send_method(username + ',' + password)
		s_message = self.receive_method()
		l_message = s_message.split('>')

		if(l_message[0] == 'a'):
			self.USERNAME = username
			print('Its Good')
			return True
		elif(l_message[0] == 'f'):
			print('NOT good!')
			return False

	def send_thread(self):
		while(self.b_running_status):
			try:

				s_message = self.OUT_MESSAGE_QUEUE.get()
				if s_message is None: 
					pass
				else:
					self.send_method(s_message)

			except ConnectionResetError as conError:
				pass
			except Exception as er:
				print("Exception occured in send thread")
				print (str(er))
				raise er

	def receive_thread(self):
		while(self.b_running_status):
			try:
			
				s_message = self.receive_method()
				self.controller.reply_handler(s_message)

			except ConnectionResetError as conError:
				self.controller.error_handler("Connection Error",
					"Server has disconnected. Program will now close, please try again at another time.")
			except Exception as er:
				print("Exception in Recieve Method")
				print(str(er))
				raise er