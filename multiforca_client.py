# coding=UTF-8

import socket
import os
import time


def show_logo():
	print(" _    _   _   _   _     _____   _   _____   ______   _____   ____   _____")
	print("| \  / | | | | | | |   |_   _| | | | ___ | |  __  | |  ___| |  __| |     |")
	print("| _\/_ | | |_| | | |__   | |   | | | ___|  | |__| | |   \_  | |__  |  _  |")
	print("|_|  |_| |_____| |____|  |_|   |_| |_|     |______| |_|\__| |____| |_| |_|")


def flush_input():
	try:
		import sys, termios
		termios.tcflush(sys.stdin, termios.TCIOFLUSH)
	except ImportError:
		import msvcrt
		while msvcrt.kbhit():
			msvcrt.getch()


nome = raw_input("Nome: ")

ip = raw_input("IP: ")
porta = raw_input("Porta: ")
print("Espere enquanto outros jogadores entram e seu mestre escolhe a palavra")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, int(porta)))

time.sleep(0.001)
sock.send(nome)

minhapalavra = sock.recv(1024)

fim = 1;
while(fim):
	os.system("cls")
	show_logo()
	placar = sock.recv(1024)
	if(placar.startswith("fim de jogo")):
		break


	print('\n'+placar)
	time.sleep(0.001)
	sock.send('nada')

	print("Sua palavra: \n")
	for c in minhapalavra:  # printa sua a palavra
		print(c + ' '),

	print ('\n')

		
	ret = sock.recv(1024)
	if(ret == "É a sua vez de jogar: "):
		time.sleep(0.001)
		flush_input()
		sock.send(raw_input("\nEscolha uma letra ou chute a palavra: ").lower())
		minhapalavra = sock.recv(1024)

	else:
		print("\n"+ret)
		
		fimdeturno = sock.recv(1024)

vencedores = []
vencedores = placar.split('|')

if(len(vencedores)== 2):
	print("O jogo acabou, o vencedor foi "+vencedores[1]+".")
elif(len(vencedores) > 2):
	print("O jogo acabou empatado, os vencedores foram:")
	for i in range(1, len(vencedores)):
		print vencedores[i]


sock.close()
