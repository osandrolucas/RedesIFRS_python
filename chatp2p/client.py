import socket
import sys
import time
from emoji import emojize

s = socket.socket()
host = str.upper(input('Por favor, insira o nome do servidor para se conectar: '))
# print(host) #testing upper
port = 5000
try:
    print(emojize('Tentando se conectar ao servidor :clock12: :clock2: :clock3: :clock4: :clock5: ...', use_aliases=True))
    s.connect((host, port))
    print('Sucesso! Você entrou no Chat P2P através do servidor "{}" na porta "{}".'.format(host, port))
    print(emojize('Status da conexão: :on:', use_aliases=True))
    print(emojize('\nAguardando uma mensagem do Servidor...  :clock12: :clock2: :clock3: :clock4: :clock5: ...',use_aliases=True))
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
        print('Mensagem enviada com sucesso...')
        print(emojize('\nAguardando uma mensagem do Servidor...  :clock12: :clock2: :clock3: :clock4: :clock5: ...',use_aliases=True))
        print('')
except Exception as e:
    print(emojize('\nErro ao conectar no Servidor :cry: Reinicie e tente novamente :repeat:', use_aliases=True))
    print(e)
