# -*- coding: utf-8 -*-
import socket, select, string, sys
import threading
import time


def server_connection():
	while True:
		print "Trabalhando no servidor"
		time.sleep(1)

def client_connection():
	while True:
		print "Trabalhando no cliente"
		time.sleep(1)

def message_monitor():
	while True:
		print "Trabalhando no monitor"
		time.sleep(1)

#Auxiliary function to read the txt file and 
def get_node_port(node_name):
	fileLines = open('node_map.txt', 'r').readlines()
	for line in fileLines:
		#Remove o \n do final da linha
		line = line.rstrip()
		if node_name in line:
			return int(line.split('|')[1]) 
	sys.exit("ERROR: Node name ", node_name, " not found!") 


try:
	NODE_NAME 	= sys.argv[1]
except:
	sys.exit("1st parameter = node name, ex: A, B, C...")

node_port = get_node_port(NODE_NAME)

#Start server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', node_port))
server_socket.listen(3)

#Store socket objects used to establishes pending connection and send messages
CONNECTIONS = []
PENDING_CONNECTION = []

print ("Node ",NODE_NAME ," initialized at port ", node_port)

client_args = []
if NODE_NAME == 'A':
	PENDING_CONNECTION.append("B")
	PENDING_CONNECTION.append("C")
elif NODE_NAME == 'B':
	PENDING_CONNECTION.append("A")
elif NODE_NAME == 'C':
	PENDING_CONNECTION.append("A")

#Criacao da thread do servidor
thread_servidor = threading.Thread(target=server_connection, args=())
thread_servidor.start()

thread_cliente = threading.Thread(target=client_connection, args=())
thread_cliente.start()

thread_monitor = threading.Thread(target=message_monitor, args=())
thread_monitor.start()