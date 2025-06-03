from socket import *

host = gethostname()
port = 55551

print(host, port)

serv = socket(AF_INET, SOCK_STREAM)
serv.bind((host, port))
serv.listen(1)


print(f"Servidor iniciado em {host}:{port}. Esperando por um oponente.")

conn, addr = serv.accept()
print(f'Oponente conectado em {addr}')

jogada_1 = ""
while jogada_1 not in ["pedra", "papel", "tesoura"]:
    jogada_1 = input("Escolha sua jogada, jogador 1")

jogada_2 = conn.recv(1024).decode('utf-8') #Recebe as informações do cliente

print(f'jogador 2 escolheu: {jogada_2}')

resultado = ""
if jogada_1 == jogada_2:
    resultado = "Empate"
elif (jogada_1 == "pedra" and jogada_2 == "tesoura") or \
     (jogada_1 == "tesoura" and jogada_2 == "papel") or \
     (jogada_1 == "papel" and jogada_2 == "pedra"):
    
    resultado = "Jogador 1 Venceu"
else:
    resultado = "Jogador 2 Venceu"

print(resultado)
conn.sendall(resultado.encode('utf-8')) #Envia o resultado para o cliente

conn.close()
serv.close()
print("Conexão fechada.")



