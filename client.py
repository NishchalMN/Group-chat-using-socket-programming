# client side

import threading
from socket import *
import tkinter
from tkinter import *

name = "Nishchal"
click_flag = 0

host = '10.2.22.80'
port = 20001
buffer_size = 1024
addr = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(addr)


def printing(client_socket):
    while True:
        tdata = client_socket.recv(buffer_size)
        data = tdata.decode('utf-8')
        if(data.startswith(name)):
            # print(data)
            t1 = '                                                                            You' + data[len(name):]
            msg_list.insert(tkinter.END, t1)
        else:
            msg_list.insert(tkinter.END, data)
        msg_list.yview(END)
        # o_list.yview(END)

t1 = threading.Thread(target = printing , args = (client_socket,))
# t1.start()

def inp(event=None):
	# while True:
    tdata = my_msg.get()
    data = name + ' > ' + tdata
    client_socket.send(bytes(data, 'utf-8'))
    # if(tdata == 'bye'):
    #     break
    my_msg.set("")

def click_text(event=None):
    global click_flag
    if(click_flag==0):
        my_msg.set("")
        click_flag=1

top = tkinter.Tk()
top.title("Asynchronous Multi-Threaded Chat Room")

scrollbar = Scrollbar(top)
scrollbar.pack( side = RIGHT, fill = Y )
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your message!")

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=75, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

msg_list.pack()

t1.start()
# o_list = tkinter.Listbox(messages_frame, height=30, width=75, yscrollcommand=scrollbar.set)
# o_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

# o_list.pack()

scrollbar.config(command = msg_list.yview)
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", inp)
entry_field.bind("<Button-1>",click_text)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=inp)
send_button.pack()
client_socket.send(bytes(name, 'utf-8'))
mainloop()

t1.join()
print('c ended')
client_socket.close()