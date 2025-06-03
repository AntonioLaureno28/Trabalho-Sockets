from socket import *
import threading
import time

jogadores = []
jogadas = {}
lock = threading.Lock()

def analise_vencedor(lance_1, lance_2):
    resultado = ""
    if lance_1 == lance_2:
        resultado = "Empate"
    elif (lance_1 == "pedra" and lance_2 == "tesoura") or \
     (lance_1 == "tesoura" and lance_2 == "papel") or \
     (lance_1 == "papel" and lance_2 == "pedra"):
    
        resultado = "Jogador 1 Venceu"
    else:
        resultado = "Jogador 2 Venceu"
    return resultado


def gerenciar_jogadas(conexao, endereco):

    global jogadores, jogadas

    with lock:
        #Verifica se os 2 jogadores estão ocupando a rodada, se tiverem, a conexão é fechada
        if len(jogadores) >= 2:
            conexao.sendall("Jogo lotado.".encode('utf-8'))
            conexao.close()
            return
        else:
            jogadores.append(conexao)
            
    try:

        #Verifica se temos jogadores suficientes para começar a rodada
        if len(jogadores) == 1:
            conexao.sendall("Aguardando outro oponente".encode('utf-8'))
            while len(jogadores) < 2:
                time.sleep(2)
        conexao.sendall("O jogo vai começar".encode('utf-8'))


        jogada = conexao.recv(1024).decode('utf-8')
        with lock:
            jogadas[conexao] = jogada
            
            if len(jogadas) == 2:
                j1_conn, j2_conn = jogadores[0], jogadores[1]
                lance_j1 = jogadas[j1_conn]
                lance_j2 = jogadas[j2_conn]
                result = analise_vencedor(lance_j1, lance_j2)

                if result == "Jogador 1 Venceu":
                    j1_conn.sendall(f"Você Venceu! Você: {lance_j1} ; Oponente: {lance_j2}".encode('utf-8'))
                    j2_conn.sendall(f"Você Perdeu! Você: {lance_j2} ; Oponente: {lance_j1}".encode('utf-8'))
                elif result == "Jogador 2 Venceu":
                    j2_conn.sendall(f"Você Venceu! Você: {lance_j2} ; Oponente: {lance_j1}".encode('utf-8'))
                    j1_conn.sendall(f"Você Perdeu! Você: {lance_j1} ; Oponente: {lance_j2}".encode('utf-8'))
                else:
                    j1_conn.sendall(f"Empate! Você: {lance_j1} ; Oponente: {lance_j2}".encode('utf-8'))
                    j2_conn.sendall(f"Empate! Você: {lance_j2} ; Oponente: {lance_j1}".encode('utf-8'))

                jogadores.clear()
                jogadas.clear()

    except Exception as e:
        print("Ocorreu um erro ao receber a jogada")
    finally:
        print("Operação encerrada.")
        conexao.close()


host = gethostname()
port = 55551

print(host, port)

serv = socket(AF_INET, SOCK_STREAM)
serv.bind((host, port))
serv.listen(2)


while True:
    conexao, endereco = serv.accept()
    thread = threading.Thread(target=gerenciar_jogadas, args=(conexao, endereco))
    thread.start()

