#cliente_udp
from encodings import utf_8
from enum import Flag
from heapq import nsmallest
import socket
import json
import time
from webbrowser import Opera
import zlib
import struct
import threading as th
IP_CLIENTE = socket.gethostbyname(socket.gethostname())
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente = (IP_CLIENTE, 8000)
global pacote
global ack
global Flag
global nSerie
nSerie = -1
flag = 0
ack = -1

#é necessário o ip do servidor, para que o cliente enxergue o servidor
PORTA = 8000

# Function to find the Checksum of Sent Message
def checksum_calculator(data):
     checksum = zlib.crc32(data)
     print("O checksum calculado foi: ",checksum)
     return checksum

def criaPacote(isPerda):
    global nSerie
    start = time.time()
    print('qual mensagem você deseja enviar?, ')
    mensagem = input()
    packet = bytearray(mensagem,'utf-8')#Data
    checksum = checksum_calculator(packet)#checksum
    if(nSerie>0):
        nSerie=0
    else:
        nSerie=1
    if(isPerda):
        a = 1
        #pacote original
        print(packet)
        #criando o novo corrompido
        pacote = packet
        pacote[1] >>= 1
        print(pacote)
    udp_header = struct.pack("!IIIII", PORTA, 7000, len(packet), checksum,nSerie)
    pacoteSerial = udp_header+packet;#cria o pacote com header
    return pacoteSerial

def pacoteDuplicado():
   global flag
   global ack
   global pacote
   pacote1 =  criaPacote(False)
   pacote2 = pacote1
   pacote = pacote1
   
   if(flag==0):
    IP_ROTEADOR = IP_CLIENTE
    endereco_roteador = (IP_ROTEADOR, 7000)

   #recebe mensagem do cliente
   t=th.Timer(10,timer)
   t.start()
   udp.sendto(pacote1, endereco_roteador)
   ack,servidor  = udp.recvfrom(1024)
   print("ack primeiro pacote recebido ", ack)
   ack = -1
   udp.sendto(pacote2, endereco_roteador)
   ack,servidor  = udp.recvfrom(1024)
   print("ack segundo pacote recebido?", ack)

   # print("pacote enviado esperando ack")
   t.cancel()
   menu()


#manda o pacote para o servidor e espera o ack, caso não receba manda de novo
def mandaPacote(isPerda):
    global flag
    global ack
    global pacote
    if(flag==0):
        IP_ROTEADOR = IP_CLIENTE
        endereco_roteador = (IP_ROTEADOR, 7000)

    #recebe mensagem do cliente
    t=th.Timer(10,timer)
    pacote = criaPacote(isPerda)
    udp.sendto(pacote, endereco_roteador)
    t.start()
    ack,servidor  = udp.recvfrom(1024)
    print("ack recebido ", ack)
    t.cancel()
    menu()
    #fim socket

def reenviaPacote(pacote):
    global flag
    global ack
    if(flag==0):
        IP_ROTEADOR = IP_CLIENTE
        endereco_roteador = (IP_ROTEADOR, 7000)

    #recebe mensagem do cliente
    t=th.Timer(10,timer)
    udp.sendto(pacote, endereco_roteador)
    t.start()
    ack,servidor  = udp.recvfrom(1024)
    print("ack recebido ", ack)
    t.cancel()
    menu()

def timer():
    global ack
    global pacote
    if(ack==-1):
        print("Timer estourou, mandando de novo o pacote")
        reenviaPacote(pacote)
    else:
        print("Pacote recebido")
        ack = -1
        menu()

def menu():
    #while(True):
        print("digite a operação que quer executar\n[1]-mandar pacote (sem perda)\n[2]-mandar pacote (com perda)")
        print("[3]-pacote duplicado")
        operacao = int(input())
        if(operacao==1):
            mandaPacote(False)
        elif(operacao==2):
            mandaPacote(True)#com perda
        elif(operacao==3):
            pacoteDuplicado()

udp.bind(cliente)
menu()

