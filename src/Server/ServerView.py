import tkinter as tk 
from tkinter import messagebox
from tkinter import font as tkfont


#NOTES: The View is the module whose task is to display data to the user. Might call on model to display data

class ServerWindow(tk.Tk):

	def __init__(self, controller, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.CONTROLLER = controller
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

		#list of frames
		FrameTouple = (Login, ServerView)
		
		#self.bind('<Return>', self.CONTROLLER.Return_Key_Handler)

		# main container frame for Server Window
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in FrameTouple: #login
			page_name = F.__name__
			frame = F(container, self.CONTROLLER)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew", **kwargs)

		self.show_frame("Login")

	def run(self):

		"""Run method for Server side TKinter window"""

		self.title("Python Server Application")
		self.deiconify()
		self.mainloop()

	def close_windows(self):

		"""Close method for Server side TKinter window"""

		try:
			self.destroy()
		except tk.TclError as er:
			pass

	def show_frame(self, s_page_name):

		'''Method for showing a TKinter window frame. Requires page name string'''

		frame = self.frames[s_page_name]
		frame.tkraise()
		self.current_frame = frame

	def current_frame(self):

		"""Method for returning current top TKinter window frame"""

		return self.currentFrame

	def error_box(self, title, message):

		"""Method for displaying login error warning box."""
		
		messagebox.showerror(title, message)

	def update_txt_messages(self, reply):
		self.current_frame.update_txt_messages("\n" + reply)

	def update_users(self, string):
		self.current_frame.update_users(string)

	def load_users(self, list):
		self.current_frame.load_users(list)


class ServerView(tk.Frame):

	def __init__(self, master, controller):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
		self.master = master
		self.controller = controller

		#TODO: Fix return binding bug
		#self.ent_reply.bind("<Return>", (lambda event: self.Reply_Message))

		#Frame
		self.fr_top = tk.Frame(self, background="Light Gray")
		self.fr_users = ActiveUsersWidget(self.fr_top)

		#Buttons, Lables, Entries
		self.quitButton = tk.Button(self, text = 'Quit', width = 15, command = self.controller.close)
		self.sendButton = tk.Button(self, text= "Broadcast", width = 20, command = self.reply_message)
		self.ent_reply = tk.Entry(self, width = 40)
		self.lbl_Reply = tk.Label(self, text="Reply")

		#Text Field
		self.txt_messages = tk.Text(self.fr_top)
		self.txt_messages.config(state="disabled")
		self.txt_users = tk.Text(self.fr_top, width= 25, background= self.master["bg"])#"Light Gray")
		self.txt_users.config(state="disabled")
		
		#Pack
		self.txt_messages.pack(side="left",pady=10,padx=15)
		#self.txt_users.pack(side="right",pady=10,padx=15)
		self.fr_users.pack(side="right",pady=10,padx=15, fill="both")
		self.fr_top.pack(pady=10, ipadx=0)
		self.lbl_Reply.pack(side="left", padx=15, pady=8)
		self.ent_reply.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.sendButton.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.quitButton.pack(side="right", padx=15)

	def load_users(self, list):
		for user in list:	
			self.fr_users.add_new_label(user)

	def update_txt_messages(self, s_message):
		self.txt_messages.config(state="normal")
		self.txt_messages.insert(tk.END, s_message)
		self.txt_messages.config(state="disabled")

	def update_users(self, s_user):
		self.fr_users.add_new_label(s_user)
		pass

	def reply_message(self):
		self.controller.send_handler(self.ent_reply.get())
		self.ent_reply.delete(0, "end")


class Login(tk.Frame):
	def __init__(self, master, controller, **kwargs):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2, borderwidth="20")
		self.master = master
		self.controller = controller

		#Entries
		self.ent_username = tk.Entry(self)
		self.ent_username.insert(tk.END, "UserName")
		self.ent_password = tk.Entry(self)
		self.ent_password.insert(tk.END, "Password")

		#Buttons
		self.btn_login = tk.Button(self, text = 'Login', command = self.login_button)
		self.btn_quit = tk.Button(self, text = 'Quit', command = self.controller.close)

		#Labels
		self.lbl_Username = tk.Label(self, text="Username")
		self.lbl_Password = tk.Label(self, text="Password")

		#Pack
		self.lbl_Username.pack(expand=True, fill='both')
		self.ent_username.pack(expand=False, fill='y')
		self.lbl_Password.pack(expand=True, fill='both')
		self.ent_password.pack(expand=False, fill='y')
		self.btn_login.pack(expand=False, fill='y', pady= 30)
		self.btn_quit.pack(expand=False, fill='y', pady= 20)

	def login_button(self):

		"""Method for login button press"""

		username = self.ent_username.get()
		password = self.ent_password.get()
		self.controller.login_handler(username, password)

	def update_txt_message(self, message):
		print("What happened?")

class ToolBar(tk.Frame):
	def __init__():
		#TODO: Add server side toolbar widget
		pass

class ActiveUsersWidget(tk.Frame):

	frames = []
	i = 1
	
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.master = master
		self.fnt_title = tkfont.Font(family='Helvetica', size= 12, weight="bold")
		self.lbl_title = tk.Label(self, text="Active Users", font=self.fnt_title, relief="groove")

		self.lbl_title.pack(side="top",expand=False, fill='y')

	def remove_label(self, s_name):

		"""Method for removing user label from active user widget. Needs string name to remove"""

		i_flag = -1
		# Loop over the list of rames
		for frm_user in self.frames:
			i_flag += 1
			if frm_user.winfo_children()[0].name == s_name:
				frm_user.destroy()
				self.frames = self.frames[:i_flag] + self.frames[i_flag+1:]
				return

	def add_new_label(self, s_name):

		"""Method for adding user label to active user widget. requires name"""

		frm_user = tk.Frame(self, relief="groove")
		self.frames.append(frm_user)
		 
		lbl_name = tk.Label(frm_user, text=s_name, anchor='w')
		lbl_name.name = s_name

		btn_remove = tk.Button(frm_user, text="Remove", command=lambda: self.remove_label(name))    
		
		frm_user.pack(side="top")  
		lbl_name.pack(side="top") 
		#btn_remove.pack(side="right")

		pass