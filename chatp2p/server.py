import socket
import sys
import time
from emoji import emojize

##End of imports##

### init ###

s = socket.socket()
host = str.upper(socket.gethostname())
port = 5000
print('INFORMAÇÃO: O servidor será iniciado no Host {} através da porta {}.'.format(host, port))
s.bind((host,port))
print(emojize('\nLigação do servidor ao host e porta realizada com sucesso! :satisfied:', use_aliases=True))
print(emojize('Aguardando conexões :clock12: :clock2: :clock3: :clock4: :clock5: ...', use_aliases=True))
print("")

try:
    s.listen(1)
    conn, addr = s.accept()
    n = str(conn.getsockname())
    ns = n.split()
    print('{} Se conectou ao Chat P2P!'.format(ns[0]))
    print(emojize('Status da conexão: :on:', use_aliases=True))
    print('')
    while 1: #True
        #Enviando
        print('Escreva uma mensagem para o Cliente...')
        message = input(str('>> '))
        message = message.encode()
        conn.send(message)
        print('Mensagem enviada com sucesso...')
        print('')
        # Recebendo
        print(emojize('\nAguardando uma mensagem do Cliente...  :clock12: :clock2: :clock3: :clock4: :clock5: ...',use_aliases=True))
        msg_entrada = conn.recv(1024)
        msg_entrada = msg_entrada.decode()
        print('Cliente: ', msg_entrada)
        print('')
except Exception as e:
    print('Erro: ', e)
