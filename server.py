# server side

MAX = 2

global clients    # for managing the clients/ members of the group

clients = []

import threading
from socket import *

host = '10.2.22.80'
port = 20001
buffer_size = 1024
addr = (host, port)
tcp_server_socket = socket(AF_INET, SOCK_STREAM)
tcp_server_socket.bind(addr)
tcp_server_socket.listen(5)   # five clients can be in the queue

def broadcast(data):
    for client in clients:
        client.send(bytes((data.decode('utf-8')),'utf-8'))

def recieve(sock):
    while True:
        try:
            data = sock.recv(buffer_size)
            broadcast(data)
        except:
            print(sock, ' left the chat')
            clients.remove(sock)

def start_accepting(num):
    count = 0
    l = ['i' for i in range(MAX)]
    while True:
        print("Waiting for a connection...")
        client_sock, client_addr = tcp_server_socket.accept()
        print("connected from client : ",client_sock)
        if(count > MAX-1):
        	data = client_sock.recv(buffer_size)
        	tdata1 = 'Sorry, Maximum connections reached!'
        	client_sock.send(bytes(tdata1, 'utf-8'))
        	# temp.start()
        else:
	        l[count] = threading.Thread(target = recieve, args = (client_sock,))
	        clients.append(client_sock)
	        data = client_sock.recv(buffer_size)
	        tdata = data.decode('utf-8') + ' has joined the chat!'
	        broadcast(bytes(tdata, 'utf-8'))
	        l[count].start()
        count += 1
   
t1 = threading.Thread(target = start_accepting, args = (MAX,))
t1.start()

t1.join()
print('ending')
tcp_server_socket.close()