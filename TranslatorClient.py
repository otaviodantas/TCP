from socket import *
import re
import sys

serverHost = 'localhost'
serverPort = 12000    
flagM = True
flagC = False

def conectServer():
    conectS = socket(AF_INET, SOCK_STREAM)
    conectS.connect((serverHost, serverPort))
    conectS.send(op.encode())
    data = conectS.recv(1024).decode() #Recebe data enviada pelo cliente
    print(data)
    return conectS

while True:
    op = input("para iniciar conexão digite: CONECTAR\n")

    if op == 'CONECTAR':
        cc = conectServer()
        flagC = True

    while flagC:
        ch = input("Execute uma ação: \n")
        cc.send(ch.encode())
        data = cc.recv(1024).decode() #Recebe data enviada pelo cliente
        print(data)
        
        if data == 'SAIR: OK':
            cc.close()
            flagC = False
        
        elif data == 'FINALIZAR: OK':
            sys.exit()
