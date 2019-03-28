import tkinter as tk 
from tkinter import messagebox
from tkinter import font  as tkfont


#NOTES: The View is the module whose task is to display data to the user. Might call on model to display data

class ServerWindow(tk.Tk):

	def __init__(self, controller, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.CONTROLLER = controller

		#list of frames
		FrameTouple = (Login, ServerView)

		#basic font
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

		#self.bind('<Return>', self.CONTROLLER.Return_Key_Handler)

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
		try:
			self.destroy()
		except tk.TclError as er:
			#print("Window already closed")
			pass

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()
		self.currentFrame = frame

	def current_frame(self):
		return self.currentFrame

	def login_warning(self):
		messagebox.showerror("Login Warning", "Admin user not found. Incorrect username or password")


class ServerView(tk.Frame):

	def __init__(self, master, controller):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
		self.master = master
		self.controller = controller

		#Buttons, Lables, Entries
		self.quitButton = tk.Button(self, text = 'Quit', width = 15, command = self.controller.close)
		#self.sendButton = tk.Button(self, text= "Send", width = 20, command = self.Reply_Message)
		#self.ent_reply = tk.Entry(self, width = 40)
		#self.ent_reply.bind("<Return>", (lambda event: self.Reply_Message))

		self.lbl_Reply = tk.Label(self, text="Reply")

		#Text Field
		self.messages = tk.Text(self)
		self.messages.config(state="disabled")
		self.messages.pack(pady=10,padx=10)

		#Pack
		#self.lbl_Reply.pack(side="left", padx=15, pady=8)
		#self.ent_reply.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		#self.sendButton.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.quitButton.pack(side="right", padx=15)

	def update_messages(self, sMessage):
		self.messages.config(state="normal")
		self.messages.insert(tk.END, sMessage)
		self.messages.config(state="disabled")

	def reply_message(self):
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
		#self.ent_server = tk.Entry(self)
		#self.ent_server.insert(tk.END, self.controller.GetServerIP())
		#self.ent_port = tk.Entry(self)
		#self.ent_port.insert(tk.END, str(self.controller.GetServerPort()))
		self.ent_username = tk.Entry(self)
		self.ent_username.insert(tk.END, "UserName")

		self.ent_password = tk.Entry(self)
		self.ent_password.insert(tk.END, "Password")

		#Buttons
		self.btn_login = tk.Button(self, text = 'Login', command = self.login_button)
		self.btn_quit = tk.Button(self, text = 'Quit', command = self.controller.close)

		#set

		#Labels
		self.lbl_Username = tk.Label(self, text="Username")
		self.lbl_Password = tk.Label(self, text="Password")



		self.lbl_Username.pack(expand=True, fill='both')
		self.ent_username.pack(expand=False, fill='y')
		self.lbl_Password.pack(expand=True, fill='both')
		self.ent_password.pack(expand=False, fill='y')
		self.btn_login.pack(expand=False, fill='y', pady= 30)
		self.btn_quit.pack(expand=False, fill='y', pady= 20)

		#self.frame.place(x = 20, y = 270, width=120, height=25)

	def login_button(self):
		username = self.ent_username.get()
		password = self.ent_password.get()
		self.controller.login_handler(username, password)