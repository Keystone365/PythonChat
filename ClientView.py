import tkinter as tk 


#NOTES: The View is the module whose task is to display data to the user. Might call on model to display data

class ClientView(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
		self.master = master
		self.controller = controller
		self.quitButton = tk.Button(self, text = 'Quit', width = 25, command = self.controller.close_windows)
		self.messages = tk.Text(self)
		self.txt_reply = tk.Entry(self)

		self.messages.pack(pady=10,padx=10)
		self.txt_reply.pack()
		self.quitButton.pack()

	#<create the rest of your GUI here>

class Login(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
		self.grid(sticky="nsew")
		self.master = master
		self.controller = controller
		#root.resizable(False, False)
		#self.frame = Frame(self.root)

		#Entry widgets
		self.txt_server = tk.Entry(self)
		self.txt_port = tk.Entry(self)
		self.txt_username = tk.Entry(self)

		#Buttons
		self.btn_login = tk.Button(self, text = 'Login', command = self.loginButton)
		self.btn_quit = tk.Button(self, text = 'Quit', command = self.controller.close_windows)

		#set

		#Labels
		self.lbl_Server = tk.Label(self, text="Server")
		self.lbl_Port = tk.Label(self, text="Port")
		self.lbl_Username = tk.Label(self, text="Username")



		self.lbl_Server.grid(row=0, column=0)
		self.txt_server.grid(row=0, column=1)
		self.lbl_Port.grid(row=1, column=0)
		self.txt_port.grid(row=1, column=1)
		self.lbl_Username.grid(row=2, column=0)
		self.txt_username.grid(row=2, column=1)
		self.btn_login.grid(row=3, column=0, columnspan= 2, sticky="wens", padx=5, pady=5)
		self.btn_quit.grid(row=5, column=0, columnspan= 2, sticky="wens", padx=30, pady=5)

		#self.frame.place(x = 20, y = 270, width=120, height=25)

	def loginButton(self):
		server = self.txt_server.get()
		port = self.txt_port.get()
		username = self.txt_username.get()
		print(server + ", " + port + ", " + username)
		self.controller.login_handler(server, port, username)


class LoginFrame(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="This is the login page", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)

		button1 = tk.Button(self, command=lambda: controller.show_frame("Page One"))
