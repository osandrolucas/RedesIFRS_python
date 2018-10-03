import socket
import sys
from emoji import emojize
import threading
##End of imports##

### Variables ###
host = str.upper(socket.gethostname())
port = 5000
CONNECTION_LIST = []
PENDING_CONNECTION = [] #Guarda os nomes/portas dos vizinhos
RECV_BUFFER = 4096 #Aconselhável manter um valor potência de 2

### Functions ###
def prompt() :
    sys.stdout.write('>')
    sys.stdout.flush()

# Function to read the txt file and
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
        if socket != s and socket != sock :
            socket.sendall(message)

### Init ###

try:
    NODE_NAME = sys.argv[1]

    node_port = get_node_port(NODE_NAME)

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
    #thread_servidor = threading.Thread(target=server_connection, args=())
    #thread_servidor.start()

    #thread_cliente = threading.Thread(target=client_connection, args=())
    #thread_cliente.start()

    #thread_monitor = threading.Thread(target=message_monitor, args=())
    #thread_monitor.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #s.bind(('0.0.0.0', node_port))

    host = str.upper(socket.gethostname())
    #port = 5000

    print('INFORMAÇÃO: O servidor será iniciado no Host {} através da porta {}.'.format(host, node_port))
    s.bind((host,node_port)) #Ouvindo na porta que foi passada como argumento
    print(emojize('\nLigação do servidor ao host e porta realizada com sucesso! :satisfied:', use_aliases=True))
    print(emojize('Aguardando conexões :clock12: :clock2: :clock3: :clock4: :clock5: ...', use_aliases=True))
    print("")

    try:
        s.listen(1)
        conn, addr = s.accept()
        n = str(conn.getsockname())
        ns = n.split()
        print('\n{} Se conectou ao Chat P2P!'.format(ns[0]))
        print(emojize('Status da conexão: :on:', use_aliases=True))
        print('')
        while 1: #True
            #Enviando
            print('Escreva uma mensagem para o Cliente...')
            message = input(str('>> '))
            message = message.encode()
            conn.send(message)
            print('\nMensagem enviada com sucesso...')
            # Recebendo
            print(emojize('Aguardando uma mensagem do Cliente :clock12: :clock2: :clock3: :clock4: :clock5: ...',use_aliases=True))
            msg_entrada = conn.recv(1024)
            msg_entrada = msg_entrada.decode()
            print('Cliente: ', msg_entrada)
            print('')
    except Exception as e:
        print('Erro: ', e)
except:
    sys.exit("ERRO: Informe um parâmetro de entrada --> A, B, C ou D.")