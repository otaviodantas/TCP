from socket import *
import re
import sys

serverHost = 'localhost' #aspas vazias significa q o host é o meu pc
serverPort = 12000 
#serverName = "TranslatorServer"

#AF_INET ==> significa o socket usa protocolo IP
#SOCK_STREAM ==> significa que o socket usa o protocolo de trânsfere TCP
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))

#Configuração de quantos clientes o server "ouve"
serverSocket.listen(1)

#printa na tela que o servidor está pronto para ouvir
print ('Servidor pronto')

flagC = True
flagA = True
KeepConnect = False
msg1 = 'CONECTAR: OK'
allistPT = ['um', 'dois', 'três', 'quatro', 'cinco']
allistEN = ['one', 'two', 'three', 'four', 'five']
function = ['CONECTAR', 'ARMAZENAR', 'QUERY', 'SAIR', 'FINALIZAR']

def search(data):
        index = allistPT.index(data)
        result = allistEN[index]
        return result

#loop
while True:
    conect, end = serverSocket.accept()
    print(f'Conexão encontrada: {end}\n')
    
    if conect:
        KeepConnect = True

    while KeepConnect:
        data = conect.recv(1024).decode() #Recebe data enviada pelo cliente
        spr = data.split()
        print(f'Dado recebido: {data}\n')
        flagA = True

        if data  == 'CONECTAR':
            conect.send(msg1.encode()) 
        
        achose = re.match('ARMAZENAR', data)
        cchose = re.match('QUERY', data)
        schose = re.match('SAIR', data)
        fchose = re.match('FINALIZAR', data)

        if achose:
            if allistPT.count(spr[1]) == 1:
                rs = search(spr[1])
                conect.send(rs.encode())
                flagA = False
            
            else:
                allistPT.append(spr[1])
                allistEN.append(spr[2])
                msg2 = 'ARMAZENAR: OK'
                conect.send(msg2.encode())
                flagA = False

        elif cchose:
            msg3 = (str(allistPT) + ' QUERY: OK')
            conect.send(msg3.encode())

        elif schose:
            msg = 'SAIR: OK'
            conect.send(msg.encode())
            KeepConnect = False
            conect.close()

        elif fchose:
            msg = 'FINALIZAR: OK'
            conect.send(msg.encode())
            sys.exit()
        
        elif data in allistPT:
            sch = search(data)
            conect.send(sch.encode())
            flagA = False

        elif function.count(spr[0]) == 0 and flagA:
            msg4 = 'NÃO POSSUO TRADUÇÃO PARA ESSA PALAVRA'
            conect.send(msg4.encode())
            flagA = False

