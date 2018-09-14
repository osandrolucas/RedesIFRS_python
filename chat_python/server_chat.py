# -*- coding: utf-8 -*-
#Server
import socket, select
 
#Funcao para transmitir mensagens de chat para todos os clientes conectados
def broadcast_data (sock, message):
    #Para cada cliente na lista de conexões
    for socket in CONNECTION_LIST:
    	#Nao envia a mensagem para o servidor e para o cliente que gerou a mensagem
        if socket != server_socket and socket != sock :
            socket.sendall(message)
           
     
# Lista que armazena os decritores de sockets criados
CONNECTION_LIST = []
RECV_BUFFER = 4096 # Aconselhável manter um valor potência de 2
PORT = 5000 #Porta qualquer desde que livre para uso
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Habilita reutilizar o socket naquele endereço e porta caso ele ainda esteja em seu TIME_WAIT
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Permite ligações com qualquer endereço IPv4 local
server_socket.bind(("0.0.0.0", PORT))

#Numero máximo de conexões suportadas
server_socket.listen(10) 

# Adiciona a conexão do server a lista de conexões
CONNECTION_LIST.append(server_socket)

print "Chat servidor iniciado na porta " + str(PORT)

while True:
    # Pega a lista de descritores de sockets que possuem dados disponíveis para serem enviados
    #Essa funao select é de I/O e retorna a lista de sockets que estao transmitindo
    #Como parametro eh passada a lista de objetos para checar por dados transmitidos
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

    for sock in read_sockets:
        #Nova conexao
        if sock == server_socket:
            #Trata o caso quando ha uma nova conexao recebida atraves do socket server_socket
            sock_client, client_addr = server_socket.accept()
            CONNECTION_LIST.append(sock_client)
            print "Cliente "+str(client_addr)+" conectado"
             
            broadcast_data(sock_client, str(client_addr)+" entrou no chat\n")
         
        #Alguma mensagem chegando de um cliente
        else:
            data = sock.recv(RECV_BUFFER)
            if data:
                broadcast_data(sock, data)                
             
           
 
server_socket.close()