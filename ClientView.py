import tkinter as tk 
from tkinter import messagebox
from tkinter import font  as tkfont


#NOTES: The View is the module whose task is to display data to the user. Might call on model to display data

class ClientWindow(tk.Tk):


	def __init__(self, controller, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.CONTROLLER = controller

		#list of frames
		FrameTouple = (Login, ClientView)

		#basic font
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

		self.bind('<Return>', self.CONTROLLER.Return_Key_Handler)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in FrameTouple: #login
			page_name = F.__name__
			frame = F(container, self.CONTROLLER)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew", **kwargs)

		self.show_frame("Login")

	def run(self):
		self.title("Python Chat Application")
		self.deiconify()
		self.mainloop()

	def close_windows(self):
		self.destroy()

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()


class ClientView(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
		self.master = master
		self.controller = controller

		#Buttons, Lables, Entries
		self.quitButton = tk.Button(self, text = 'Quit', width = 15, command = self.controller.close)
		self.sendButton = tk.Button(self, text= "Send", width = 20, command = self.Reply_Message)
		self.ent_reply = tk.Entry(self, width = 40)
		self.ent_reply.bind("<Return>", (lambda event: self.Reply_Message))

		self.lbl_Reply = tk.Label(self, text="Reply")


		#Text Field
		self.messages = tk.Text(self)
		self.messages.config(state="disabled")
		self.messages.pack(pady=10,padx=10)

		#Pack
		self.lbl_Reply.pack(side="left", padx=15, pady=8)
		self.ent_reply.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.sendButton.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.quitButton.pack(side="right", padx=15)

	def Update_Messages(self, sMessage):
		self.messages.config(state="normal")
		self.messages.insert(tk.END, sMessage)
		self.messages.config(state="disabled")

	def Reply_Message(self):
		self.controller.Send_Handler(self.ent_reply.get())
		self.ent_reply.delete(0, "end")

class Login(tk.Frame):
	def __init__(self, master, controller, **kwargs):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2, borderwidth="20")
		self.master = master
		self.controller = controller
		#root.resizable(False, False)
		#self.frame = Frame(self.root)

		#Entry widgets
		self.ent_server = tk.Entry(self)
		self.ent_server.insert(tk.END, self.controller.GetServerIP())
		self.ent_port = tk.Entry(self)
		self.ent_port.insert(tk.END, str(self.controller.GetServerPort()))
		self.ent_username = tk.Entry(self)
		self.ent_username.insert(tk.END, "Anonymous")

		#Buttons
		self.btn_login = tk.Button(self, text = 'Login', command = self.loginButton)
		self.btn_quit = tk.Button(self, text = 'Quit', command = self.controller.close)

		#set

		#Labels
		self.lbl_Server = tk.Label(self, text="Server")
		self.lbl_Port = tk.Label(self, text="Port")
		self.lbl_Username = tk.Label(self, text="Username")



		self.lbl_Server.pack(expand=True, fill='both', side="top")
		self.ent_server.pack(expand=False, fill='y')
		self.lbl_Port.pack(expand=True, fill='both')
		self.ent_port.pack(expand=False, fill='y')
		self.lbl_Username.pack(expand=True, fill='both')
		self.ent_username.pack(expand=False, fill='y')
		self.btn_login.pack(expand=False, fill='y', pady= 30)
		self.btn_quit.pack(expand=False, fill='y', pady= 20)

		#self.frame.place(x = 20, y = 270, width=120, height=25)

	def loginButton(self):
		server = self.ent_server.get()
		port = int(self.ent_port.get())
		username = self.ent_username.get()
		self.controller.login_handler(server, port, username)


class LoginFrame(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="This is the login page", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)

		button1 = tk.Button(self, command=lambda: controller.show_frame("Page One"))
