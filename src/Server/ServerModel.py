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

	USER_CONNECTIONS = [] #For listing number of user connections
	# Each new connection is appended to the list in the following format (sublist, e.g. CONNECTIONS[0][1] == addr):
	# [0]: connection socket of the client, used to send/receive
	# [1]: address of client, not yet used, but stored if needed
	# [2]: status of connection. Statuses so far:
	#     "NEW": newly connected, accepted and stored, not yet authenticated
	#     "AUTH": started authentication, not yet logged in
	#     "VERIFIED": completed authentication, ready to start communication
	#     "ONLINE": communication set up and actively sending/recieving messages
	#     "DISCONNECTED": connection has been terminated, awaiting cleanup
	# [3]: username of validated login.  Defaults to "Guest" prior to authentication

	USER_RECIEVERS = [] #For lisiting number of user connections
	# Each new connection is given a reciever and each reciever is appended to this list

	#list of storing messages
	SERVER_MESSAGE_QUEUE = queue.Queue()

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
	SERVER.listen(5)
	b_close = False

	def __init__(self):
		pass

	def load_info(self):
		self.load_user_list()
		self.load_queue(self.MESSAGE_PATH, self.CLIENT_MESSAGE_QUEUE)

    #Check User CSV: returns list of CSV file contents
	def load_user_list(self):
		file = open(self.USER_PATH, "r") # open the authentication file for reading
		text = file.read().splitlines() # read in all lines of the file
		file.close() # close the file

		for line in text: # itterate through all the lines
			user_values = line.split(",") # parse out the username and password hash
			#UserValues.append(0) # number of failed login attempts
			#UserValues.append(time.time()) # filler to initialize the index, later used to note time of lockout
			self.AUTHENTIC_USERS.append(user_values) # store the object for later authentication
     
	#returns message list for user        
	def load_queue(self, filepath, list_queue):

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
	def save_user_list(self, Name, Pass):

		'''Save known users to CSV file at util/users.csv'''

		file = open(self.USER_PATH, "a") # open authentication file to permanently save account
		file.write(Name + "," + Pass + "\n") # write the data to file
		file.close()