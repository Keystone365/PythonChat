
from src.Client.ClientController import ClientController
from datetime import datetime

'''
Author: Andrew Christianson
Febuary 2019
Description:
TCP TKinter Multi Client Python Chat Project. 
'''
  
if __name__ == '__main__':

	print('PythonChat 2019 Client running')
	print('Startup: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	print("Press CTRL-C to Quit.")
	
	
	c = ClientController()

	try:
		c.run()

	except KeyboardInterrupt:

		print("\nCTRL-C: Server shutting down")
		print(" - Disconnecting all clients")

	except Error as er:
		print("Error occured in client controller")
		print (er)

	finally:
		c.close()

	exit (0) # return 0 for successful completion
    
    


'''*******************************************************************************************************************************
    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF    EOF
*******************************************************************************************************************************'''


'''

top = tkinter.Tk()
top.title("Chat Window")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)



tkinter.mainloop()


'''
    
    
"""

def send(event=None):  # event is passed by binders.
    #Handles sending of messages.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    #This function is to be called when the window is closed.
    my_msg.set("{quit}")
    send()
    
    
"""
