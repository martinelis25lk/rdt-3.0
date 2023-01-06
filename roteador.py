import json
from sys import flags
import threading
import socket 
import zlib
import struct
IP =  socket.gethostbyname(socket.gethostname())
#IP = '26.168.42.47'
PORTA = 7000
global udp
global flag
flag = 0
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
roteador_endereco = (IP,PORTA)
def checksum_calculator(data):
     checksum = zlib.crc32(data)
     print("O checksum calculado foi: ",checksum)
     return checksum


def checa_checksum(pacoteSerial):
    udp_header = pacoteSerial[:20]
    data = pacoteSerial[20:]
    udp_header = struct.unpack("!IIIII", udp_header)
    correct_checksum = udp_header[3]

    print("Sequence number: ",udp_header[4],"\n")
    print("Checksum recebido no header: ",udp_header[3],"\n")
    #calcula o checksum pra ver se teve corrompimento
    checksum = checksum_calculator(data)
    #retorna se o pacote está corrompido ou não
    corrompido = correct_checksum != checksum
    return corrompido

def retransmitepacote():
    print('conexão iniciada')
    while True:
        #abrea conexão do roteador
        if(flag==0):
            
            print('bind deu certo, esperando pacote')

        #espera pacote do cliente
        pacoteSerial, endereco = udp.recvfrom(1024)
        print("recebeu o pacote")
    

        #calcula o checksum e determina se o pacote foi corrompido
        isCorrompido = checa_checksum(pacoteSerial)
        #se o pacote não está corrompido, repassa para o servidor
        if(isCorrompido==False):
            print("pacote chegou intacto ao roteador, repassando ao servidor")
            print(pacoteSerial[20:])
            endereco_servidor = (IP,6000)
            endereco_cliente = (IP,8000)
            #Data
            mandaServidor(pacoteSerial,endereco_servidor)
            #manda o ack para o cliente
            ack, endereco = udp.recvfrom(1024)
            mandaCliente(ack,endereco_cliente)
            retransmitepacote()
        else:
            print("pacote corrompido")

      
    
def mandaCliente(pacote,endereco):
    udp.sendto(pacote, endereco)


def mandaServidor(pacoteSerial,endereco):
    #manda a mensagem para o servidor
    HOST_ENVIA =  socket.gethostbyname(socket.gethostname())
    ENVIA_PARA_PORTA = 6000
    destino = (HOST_ENVIA, ENVIA_PARA_PORTA)
    udp.sendto(pacoteSerial, destino)
    #espera pelo ack
    print("ack recebido, repassando para o cliente")
    #manda o ack para o cliente
    #endereco_cliente = (HOST_ENVIA, 8000)
    #ack, end_servidor = udp.recvfrom(1024) 
    #mandaCliente(ack,endereco_cliente)

udp.bind(roteador_endereco)
retransmitepacote()

