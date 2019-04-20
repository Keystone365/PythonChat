import tkinter as tk 
from tkinter import messagebox
from tkinter import font  as tkfont


'''
NOTES: 
The ClientWindow view is the module whose task is to display 
data to the user. Might call on model to display data.
The view should try not to call it's own methods. A view can be 
any type of output representation, be it HTML, GUI,
or text.
'''

class ClientWindow(tk.Tk):

	def __init__(self, controller, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.CONTROLLER = controller

		#list of frames
		frame_touple = (Login, ClientView)

		#basic font
		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

		#self.bind('<Return>', self.CONTROLLER.return_key_handler)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in frame_touple: #login

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			page_name = F.__name__
			frame = F(container, self.CONTROLLER)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew", **kwargs)

		self.show_frame("Login")

	def run(self):
		self.title("Python Chat Application")
		self.deiconify()
		self.mainloop()

	def update_txt_messages(self, reply):
		self.current_frame.update_txt_messages("\n" + reply)

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
		self.current_frame = frame

	def current_frame(self):
		return self.current_frame

	def error_box(self, title, message):
		"""Functions creates error message window."""
		messagebox.showerror(title, message)


class ClientView(tk.Frame):
	def __init__(self, master, controller):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)
		self.master = master
		self.controller = controller

		#Buttons
		self.btn_quit = tk.Button(self, text = 'Quit', width = 15, command = self.controller.close)
		self.btn_send = tk.Button(self, text= "Send", width = 20, command = self.reply_message)
		#Entries
		self.ent_reply = tk.Entry(self, width = 40)
		self.ent_reply.bind("<Return>", (lambda event: self.reply_message))
		#Label
		self.lbl_Reply = tk.Label(self, text="Reply")
		#Text Field
		self.txt_messages = tk.Text(self)
		self.txt_messages.config(state="disabled")
		
		#Pack
		self.txt_messages.pack(pady=10,padx=10)
		self.lbl_Reply.pack(side="left", padx=15, pady=8)
		self.ent_reply.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.btn_send.pack(side="left", padx=15, pady=8, ipadx = 50, fill="x")
		self.btn_quit.pack(side="right", padx=15)
		

	def update_txt_messages(self, s_message):
		self.txt_messages.config(state="normal")
		self.txt_messages.insert(tk.END, s_message)
		self.txt_messages.config(state="disabled")

	def reply_message(self):
		self.controller.send_handler(self.ent_reply.get())
		self.ent_reply.delete(0, "end")

class Login(tk.Frame):
	def __init__(self, master, controller, **kwargs):
		tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2, borderwidth="20")
		self.master = master
		self.controller = controller

		#Entry widgets
		self.ent_server = tk.Entry(self)
		self.ent_server.insert(tk.END, self.controller.get_server_ip())
		self.ent_port = tk.Entry(self)
		self.ent_port.insert(tk.END, str(self.controller.get_server_port()))
		self.ent_username = tk.Entry(self)
		self.ent_username.insert(tk.END, "Anonymous")

		#Buttons
		self.btn_login = tk.Button(self, text = 'Login', command = self.login_button)
		self.btn_quit = tk.Button(self, text = 'Quit', command = self.controller.close)

		#Labels
		self.lbl_server = tk.Label(self, text="Server")
		self.lbl_port = tk.Label(self, text="Port")
		self.lbl_username = tk.Label(self, text="Username")

		#Pack entry widgets, buttons, labels
		self.lbl_server.pack(expand=True, fill='both', side="top")
		self.ent_server.pack(expand=False, fill='y')
		self.lbl_port.pack(expand=True, fill='both')
		self.ent_port.pack(expand=False, fill='y')
		self.lbl_username.pack(expand=True, fill='both')
		self.ent_username.pack(expand=False, fill='y')
		self.btn_login.pack(expand=False, fill='y', pady= 30)
		self.btn_quit.pack(expand=False, fill='y', pady= 20)

		#self.frame.place(x = 20, y = 270, width=120, height=25)

	def login_button(self):
		server = self.ent_server.get()
		port = int(self.ent_port.get())
		username = self.ent_username.get()
		self.controller.login_handler(server, port, username)

	def update_txt_messages(self, message):
		print("What happened?")
