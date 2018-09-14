#Programa cliente
import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('>')
    sys.stdout.flush()
 
host = "localhost" #Mesmo IP do servidor
port = 5000 #Mesma porta do servidor
 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Connecta-se ao servidor
client_socket.connect((host, port))

 
print 'Conectado ao servidor do chat. Pronto para conversar'
prompt()
 
while True:
    socket_list = [sys.stdin, client_socket]
     
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
     
    for sock in read_sockets:
        #incoming message from remote server
        if sock == client_socket:
            data = sock.recv(4096)
            if  data: # Se ha algum dado recebido, mostra ele      
                print data
                prompt()
         
        #Aguarda o cliente digitar uma mensagem
        else :
            msg = sys.stdin.readline()
            client_socket.sendall(msg)
            prompt()