# coding=UTF-8
import os
import socket
import time

#CLASSE JOGADOR
class jogador():
    def __init__(self, nome, conn, addr):
        self.nome = nome
        self.conn = conn
        self.addr = addr
        self.pontos = 0
        self.palavra = ''

#LIDANDO COM A SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('', 5001))
print((sock.getsockname())[1])
sock.listen(1)

num_jogadores = int(raw_input("Quantidade de jogadores: "))

lista_jogadores = []
lista_vencedores = []


def checarpontos(i):
    if(lista_jogadores[i].pontos <= 0):
        lista_jogadores.pop(i)

#ESPERANDO OS JOGADORES ENTRAREM NO JOGO
for i in range(num_jogadores):
    conn, addr = sock.accept()
    nome = conn.recv(1024)
    lista_jogadores.append(jogador(nome, conn, addr))
    print(lista_jogadores[i].nome + " se conectou.")

palavra = raw_input("Escolha a palavra: ")

#SETANDO AS CONFIGURAÇÕES DE CADA JOGADOR
branco = ''
for i in range(len(palavra)):
    branco+='_'

for i in range(num_jogadores):
    lista_jogadores[i].palavra = branco
    lista_jogadores[i].pontos = 6;


#JOGO DE VERDADE

for j in range(num_jogadores):
    time.sleep(0.001)
    lista_jogadores[j].conn.send(branco)  # MANDANDO O BRANCO

fim = 1
os.system("cls")

while(fim):
    for i in range(num_jogadores):
        placar ="Placar: \n"
        for jog in range(num_jogadores): #MONTANDO O PLACAR
            placar+= lista_jogadores[jog].nome + '\t' + str(lista_jogadores[jog].pontos) + '\n'

        print(placar)

        for j in range(num_jogadores):
            time.sleep(0.001)
            lista_jogadores[j].conn.send(placar) #MANDANDO O PLACAR PARA TODOS OS JOGADORES
            nada = lista_jogadores[j].conn.recv(1024)
            if(j != i):
                time.sleep(0.001)
                lista_jogadores[j].conn.send(lista_jogadores[i].nome + " está jogando.") #MANDANDO PARA OS JOGADORES QUEM ESTÁ JOGANDO

        print(lista_jogadores[i].nome + " está jogando.")

        time.sleep(0.001)
        lista_jogadores[i].conn.send("É a sua vez de jogar: ") #MANDANDO PARA O JOGADOR QUE É SUA VEZ DE JOGAR
        ret = lista_jogadores[i].conn.recv(1024)
        if(len(ret) == 1):
            perdepontos = 1
            novapalavra = ''
            for c in range(len(palavra)):
                if(palavra[c] == ret):
                    perdepontos = 0
                    novapalavra += ret
                else:
                    novapalavra += lista_jogadores[i].palavra[c]


            lista_jogadores[i].palavra = novapalavra
            lista_jogadores[i].pontos -= perdepontos
            time.sleep(0.001)
            lista_jogadores[i].conn.send(lista_jogadores[i].palavra)
            checarpontos(i)
        else:
            perdepontos = 2
            if(palavra == ret):
                fim = 0
                lista_jogadores[i].palavra = palavra
                lista_vencedores.append(lista_jogadores[i])
                perdepontos = 0
            lista_jogadores[i].pontos -= perdepontos
            time.sleep(0.001)
            lista_jogadores[i].conn.send(lista_jogadores[i].palavra)
            checarpontos(i)

        for j in range(num_jogadores):
            if(j != i):
                time.sleep(0.001)
                lista_jogadores[j].conn.send("Fim de turno") #MANDANDO PARA OS JOGADORES QUE ESTAVAM ESPERANDO QUE O TURNO ACABOU


#Determinar um o vencedor
maior = max(i.pontos for i in lista_vencedores)
vencedor = ''

for i in range(len(lista_vencedores)):
    if(lista_vencedores[i].pontos == maior):
        vencedor += '|' + lista_vencedores[i].nome


#Mandando o sinal que o jogo acabou
for i in range(num_jogadores):
    lista_jogadores[i].conn.send("fim de jogo"+vencedor)

sock.close()
