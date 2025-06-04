from socket import *

#Deve ser substituído pelo endereço do servidor
IP_ADRESS = 'REDACTED'
port = 55551

#Criação do Socket com endereço IPV4 para realizar comunicação TCP
client = socket(AF_INET, SOCK_STREAM)

try:
    #Conexão do cliente com o servidor naquele endereço IP
    client.connect((IP_ADRESS, port))

    while True:
        server_response = client.recv(1024).decode('utf-8')
        print(server_response)
        #Jogo iniciado 
        if server_response == "Faça sua jogada":
            jogada = ""
            jogada = input().lower()
            client.sendall(jogada.encode('utf-8'))
            resultado = client.recv(1024).decode('utf-8')
            print(resultado)
            break

except socket.error as e:
    print(e)
finally:
    #Fecha a conexão com o servidor
    print("Fechando a conexão...")
    input("Pressione Enter para encerrar")
    client.close()






