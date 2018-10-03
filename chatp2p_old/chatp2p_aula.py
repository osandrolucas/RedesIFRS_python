# -*- coding: utf-8 -*-
import socket, select, string, sys
import threading
import time

host = "localhost" #Mesmo IP do servidor

# Auxiliary function to read the txt file and
def get_node_port(node_name):
    fileLines = open('node_map.txt', 'r').readlines()
    for line in fileLines:
        # Remove o \n do final da linha
        line = line.rstrip()
        if node_name in line:
            return int(line.split('|')[1])
    sys.exit("ERROR: Node name ", node_name, " not found!")

#Funcao para transmitir mensagens de chat para todos os clientes conectados
def broadcast_data (sock, message):
    #Para cada cliente na lista de conexões
    for socket in CONNECTION_LIST:
    	#Nao envia a mensagem para o servidor e para o cliente que gerou a mensagem
        if socket != server_socket and socket != sock :
            socket.sendall(message)

def prompt() :
    sys.stdout.write('>')
    sys.stdout.flush()

try:
    NODE_NAME = sys.argv[1]
except:
    sys.exit("1st parameter = node name, ex: A, B, C...")

node_port = get_node_port(NODE_NAME)

# Start server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ok
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #ok
server_socket.bind(('0.0.0.0', node_port)) #Ouvindo na porta que foi passada como argumento
server_socket.listen(3) #vizinhos/conexões. Se tiver mais, aumentar

# Store socket objects used to establishes pending connection and send messages
CONNECTION_LIST = []
PENDING_CONNECTION = [] #Guarda os nomes/portas dos vizinhos
RECV_BUFFER = 4096 #Aconselhável manter um valor potência de 2

print("Node ", NODE_NAME, " initialized at port ", node_port)

client_args = []
if NODE_NAME == 'A':
    PENDING_CONNECTION.append("B")
    PENDING_CONNECTION.append("C")
elif NODE_NAME == 'B':
    PENDING_CONNECTION.append("A")
    #PENDING_CONNECTION.append("D")
elif NODE_NAME == 'C':
    PENDING_CONNECTION.append("A")
    #PENDING_CONNECTION.append("A")

# Criacao da thread do servidor
thread_servidor = threading.Thread(target=server_connection, args=())
thread_servidor.start()

thread_cliente = threading.Thread(target=client_connection, args=())
thread_cliente.start()

thread_monitor = threading.Thread(target=message_monitor, args=())
thread_monitor.start()

#O arquivo server.py da aula passada e o client.py nada mais são do que as threads que ele pede.
#O arquivo server.py tem o monitoramento.

print("Chat servidor iniciado na porta {}".format(str(node_port)))

while True:
    # Pega a lista de descritores de sockets que possuem dados disponíveis para serem enviados
    # Essa funao select é de I/O e retorna a lista de sockets que estao transmitindo
    # Como parametro eh passada a lista de objetos para checar por dados transmitidos
    read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

    for sock in read_sockets:
        # Nova conexao
        if sock == server_socket:
            # Trata o caso quando ha uma nova conexao recebida atraves do socket server_socket
            sock_client, client_addr = server_socket.accept()
            CONNECTION_LIST.append(sock_client)
            print("Cliente " + str(client_addr) + " conectado")

            broadcast_data(sock_client, str(client_addr) + " entrou no chat\n")

        # Alguma mensagem chegando de um cliente
        else:
            data = sock.recv(RECV_BUFFER)
            if data:
                broadcast_data(sock, data)

# Connecta-se ao servidor
client_socket.connect((host, port))

print('Conectado ao servidor do chat. Pronto para conversar')
prompt()

while True:
    socket_list = [sys.stdin, client_socket]

    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

    for sock in read_sockets:
        # incoming message from remote server
        if sock == client_socket:
            data = sock.recv(4096)
            if data:  # Se ha algum dado recebido, mostra ele
                print(data)
                prompt()

        # Aguarda o cliente digitar uma mensagem
        else:
            msg = sys.stdin.readline()
            client_socket.sendall(msg)
            prompt()