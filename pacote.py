from datetime import datetime
from socket import *
import json 


addrD = ""#porta destino
addrS = ""#porta origim

s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)




data = 'data de teste'
addr = 4711    # arbitrary source port
dport = 45134   # arbitrary destination port
length = 8+len(data);
checksum = 0

pacote = {
    "data": "data de teste",
    "addr_origem": 7000, #porta de origem,
    "addr_destino": 6000, #porta de destino
    "lenght": length,
    "checksum" : 13,
    "numSerie" : 1
}

pacoteSerial = json.dumps(pacote);
#udp_header = struct.pack('!HHHH', sport, dport, length, checksum)
s.sendto(bytes(pacoteSerial),json, ('', 0));


