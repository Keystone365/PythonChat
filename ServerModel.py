import queue


class ServerModel:

	THREADS = [] #list of threads for cleanup
	#all threads will be appended to this list
	#itterating through this list will be used for clean up


	AUTHENTIC_USERS = [] #Authentic user list - for reading from and updating CSV file
	# populated on startup
	# for each element of AUTHENTIC_USERS
	# [0]: user
	# [1]: passhash


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
	onlineUsers = []

	#paths for CSV files
	UserPath = 'util/users.csv'
	MessagePath = 'util/messages.csv'

	def __init__(self):
		pass