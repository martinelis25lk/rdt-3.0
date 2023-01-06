#servidor_UDP
from multiprocessing import connection
import socket
import struct
import zlib
import zlib
IP = socket.gethostbyname(socket.gethostname())
#IP = '26.168.42.47'
print(IP+'\n')
PORTA = 6000
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
global meu_servidor
meu_servidor = (IP, PORTA)
global nSerie
nSerie = -1


def mandaCliente(pacote,endereco):
    udp.sendto(pacote, endereco)


def checksum_calculator(data):
     checksum = zlib.crc32(data)
     print("O checksum calculado foi: ",checksum)
     return checksum


def checa_checksum(pacoteSerial):
    udp_header = pacoteSerial[:20]
    data = pacoteSerial[20:]
    udp_header = struct.unpack("!IIIII", udp_header)
    correct_checksum = udp_header[3]
    #calcula o checksum pra ver se teve corrompimento
    checksum = checksum_calculator(data)
    #retorna se o pacote está corrompido ou não
    corrompido = correct_checksum != checksum
    return corrompido


def ligaServidor():
    global nSerie
    roteador = (IP,7000)
    ack = bytearray('1','utf-8')#Data
    print("\nNumero de Serie do Ultimo pacote ", nSerie)
    print('estabelecendo conexão...')
    print('esperando mensagem do roteador...\n\n')
    mensagem_recebida, end_cliente = udp.recvfrom(1024) 
    data = mensagem_recebida[20:]
    udp_header = mensagem_recebida[:20]
    udp_header = struct.unpack("!IIIII", udp_header)
    print("recebi = ",data , "do roteador passando ack para ele")
    print("Numero de serie recebido: ",udp_header[4])
    isCorrompido = checa_checksum(mensagem_recebida)
    
    #se o pacote não está corrompido, repassa para roteador->
    if(isCorrompido==False):
        print("pacote chegou intacto ao servidor, mandando ack")
        if(nSerie==udp_header[4]):
            print("pacote duplicado")
        elif(nSerie<=0):
            nSerie=1
            mandaCliente(ack,roteador)
        elif(nSerie>0):
            mandaCliente(ack,roteador)
            nSerie=0
        #mandando o ack
        ligaServidor()
    else:
        print("pacote corrompido")

udp.bind(meu_servidor)
ligaServidor()

