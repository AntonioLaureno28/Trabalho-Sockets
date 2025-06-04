from socket import *

#Deve ser substituído pelo endereço do servidor
IP_ADRESS = "192.168.2.22"
port = 55551

#Criação do Socket com endereço IPV4 para realizar comunicação TCP
client = socket(socket.AF_INET, socket.SOCK_STREAM)

#Conexão do cliente com o servidor naquele endereço IP
client.connect(IP_ADRESS, port)
server_response = client.recv(1024).decode('utf-8')

#Esperando a primeira resposta do servidor
if server_response == "O jogo vai começar":
    server_response = client.recv(1024).decode('utf-8')

    #Jogo iniciado 
    if server_response == "Faça sua jogada":
        jogada = input().lower()
        client.sendall(jogada.encode('utf-8'))
        resultado = client.recv(1024).decode('utf-8')
        print(resultado)

#Caso de o jogo ainda não poder ser inicializado
else:
    print(server_response)

#Fecha a conexão com o servidor
client.close()






