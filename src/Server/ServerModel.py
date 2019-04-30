import queue
from socket import *


class ServerModel:

	THREADS = [] #list of threads for cleanup
	#all threads will be appended to this list
	#itterating through this list will be used for clean up

	AUTHENTIC_USERS = [] #Authentic user list - for reading from and updating CSV file
	# populated on startup
	# for each element of AUTHENTIC_USERS
	# [0]: user
	# [1]: passhash
	# [2]: admin

	NEW_CONNECTIONS = [] #For lisiting number of new connections
	# Each new connection is given a reciever and each reciever is appended to this list

	USER_CONNECTIONS = []
	# Each authenticated connection has a reciever and each authenticated reciever is appended to this list

	CLIENT_MESSAGE_QUEUE = queue.Queue() # populated by receiveMessages threads, consumed by sendMessages thread
	# each received message from clients, in the following format:
	# [0]: sending user, may be "SYSTEM" for informative messages
	# [1]: target user, may be "BROADCAST" for sending to all online users
	# [2]: message
	# [3]: is new? (messages for offline users will be recycled to the back of the queue, reporting to the messager should only happen the first time it cycles through)

	STOREDMESSAGES = []
	#[0] sender
	#[1] reciever
	#[2] message

	#online user list - not related to CSV file
	online_users = []

	#paths for CSV files
	USER_PATH = 'data/users.csv'
	MESSAGE_PATH = 'data/messages.csv'

	THREADS_JOIN = False # Boolean flag for ending threads

	HOST = "127.0.0.1"
	PORT = 5006
	BUFSIZ = 1024
	ADDR = (HOST, PORT)

	SERVER = socket(AF_INET, SOCK_STREAM)
	SERVER.bind(ADDR)
	SERVER.settimeout(3) #set time out value
	b_close = False

	def __init__(self):
		pass

	def load_info(self):

		'''Loads user data info from csv files.'''

		self.load_user_list()
		self.load_queue(self.MESSAGE_PATH, self.CLIENT_MESSAGE_QUEUE)

	def load_user_list(cls):

		'''Loads authentic user list from users.csv file.'''

		file = open(cls.USER_PATH, "r") # open the authentication file for reading
		text = file.read().splitlines() # read in all lines of the file
		file.close() # close the file

		for line in text: # itterate through all the lines
			user_values = line.split(",") # parse out the username and password hash
			#UserValues.append(0) # number of failed login attempts
			#UserValues.append(time.time()) # filler to initialize the index, later used to note time of lockout
			cls.AUTHENTIC_USERS.append(user_values) # store the object for later authentication

	def load_queue(cls, filepath, list_queue):

		'''Load stored unsent messages from messages.csv '''

		# open the authentication file for reading
		file = open(filepath, "r") 
		text = file.read().splitlines()
		file.close()

		# itterate through all the lines
		for line in text: 
			message_values = line.split(",") #Get message values
			list_queue.put(message_values) # store the object for later authentication

	#Write CSV: writes user dictionary to users.CSV file and writes over previous information		
	def save_user_list(cls, Name, Pass):

		'''Save known users to CSV file at util/users.csv'''

		file = open(cls.USER_PATH, "a") # open authentication file to permanently save account
		file.write(Name + "," + Pass + "\n") # write the data to file
		file.close()

	def is_authentic(cls, b_admin, username, passhash):

		'''Checks if user is authentic valid user. Returns boolean value.'''

		for account in cls.AUTHENTIC_USERS: #itterate through account list
			# if username found, password correct and admin privliges
			if (account[0] == username) and (account[1] == passhash):
				if(b_admin and account[2] == '1') or (not b_admin):
					return True
		#return false if no user match
		return False

	def remove_receiver(cls):

		'''TODO: Add functionality for removing online users'''
		for account in cls.online_users:
			if(account[0] == username):
				pass
