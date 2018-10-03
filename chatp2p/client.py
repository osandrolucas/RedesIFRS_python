import socket
import sys
from emoji import emojize

### Functions ###

def prompt():
    sys.stdout.write('>>')
    sys.stdout.flush()

# Auxiliary function to read the txt file and
def get_node_port(node_name):
    fileLines = open('node_map.txt', 'r').readlines()
    for line in fileLines:
        # Remove o \n do final da linha
        line = line.rstrip()
        if node_name in line:
            return int(line.split('|')[1])
    sys.exit("ERROR: Node name ", node_name, " not found!")

### Init ###

try:
    NODE_NAME = sys.argv[1]

    host = str.upper(input('SEJA BEM VINDO! Por favor, insira o nome do servidor para se conectar: '))
    s = socket.socket()
    node_port = get_node_port(NODE_NAME)

    try:
        print(emojize('Tentando se conectar ao servidor :clock12: :clock2: :clock3: :clock4: :clock5: ...', use_aliases=True))
        s.connect((host, node_port))
        print('\nSucesso! Você entrou no Chat P2P através do servidor "{}" na porta "{}".'.format(host, node_port))
        print(emojize('Status da conexão: :on:', use_aliases=True))
        print(emojize('Aguardando uma mensagem do Servidor :clock12: :clock2: :clock3: :clock4: :clock5: ...',use_aliases=True))
        while 1:
            # Recebendo
            msg_entrada = s.recv(1024)
            msg_entrada = msg_entrada.decode()
            print('Servidor: ', msg_entrada)
            print('')
            # Enviando
            print('Escreva uma mensagem para o Servidor...')
            message = input(str('>> '))
            message = message.encode()
            s.send(message)
            print('\nMensagem enviada com sucesso...')
            print(emojize('Aguardando uma mensagem do Servidor...  :clock12: :clock2: :clock3: :clock4: :clock5: ...',use_aliases=True))
            print('')
    except Exception as e:
        print(emojize('\nErro ao conectar no Servidor :cry: Reinicie e tente novamente :repeat:', use_aliases=True))
        print(e)
except:
    sys.exit("ERRO: Informe um parâmetro de entrada --> A, B, C ou D.")