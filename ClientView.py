from tkinter import * 


#NOTES: The View is the module whose task is to display data to the user. Might call on model to display data

class ClientView:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.frame = Frame(self.root, width = 400, height = 300)
        self.quitButton = Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.messages = Text(self.root)

        self.messages.pack()
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.root.destroy()

        #<create the rest of your GUI here>

class Login:
    def __init__(self, root, model):
        self.root = root
        root.geometry("170x300")
        root.resizable(False, False)
        self.model = model
        #self.frame = Frame(self.root)

        #Entry widgets
        self.txt_server = Entry(self.root)
        self.txt_port = Entry(self.root)
        self.txt_username = Entry(self.root)

        #Buttons
        self.btn_login = Button(self.root, text = 'Login', command = self.loginButton)
        self.btn_quit = Button(self.root, text = 'Quit', command = self.close_windows)

        #set

        #Labels
        self.lbl_Server = Label(root, text="Server")
        self.lbl_Port = Label(root, text="Port")
        self.lbl_Username = Label(root, text="Username")
        


        self.lbl_Server.place(x = 20, y = 30, width=120, height=25)
        self.txt_server.place(x = 20, y = 60, width=120, height=25)
        self.lbl_Port.place(x = 20, y = 90, width=120, height=25)
        self.txt_port.place(x = 20, y = 120, width=120, height=25)
        self.lbl_Username.place(x = 20, y = 150, width=120, height=25)
        self.txt_username.place(x = 20, y = 180, width=120, height=25)
        self.btn_login.place(x = 20, y = 210, width=120, height=25)
        self.btn_quit.place(x = 20, y = 240, width=120, height=25)
        
        #self.frame.place(x = 20, y = 270, width=120, height=25)
        
    def close_windows(self):
        self.root.destroy()

    def loginButton(self):
    	server = self.txt_server.get()
    	port = self.txt_port.get()
    	username = self.txt_username.get()
    	self.model.loginCommand(server, port, username)
