#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# A lancer en premier
#
# Ce serveur retourne ce qui lui a ete envoye
# (utilisable en TP pour tester scapy & cie)

import socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#mySocket.bind(('',2222)) # '': toutes les interfaces disponibles
mySocket.bind(('',2222))
print ("Echo_server : en attente...")
try:
  while True:
    msgClientraw, addr = mySocket.recvfrom(1024)
    print ("Connected from", addr)
    print (msgClientraw)
    mySocket.sendto(msgClientraw, addr)
finally:
  mySocket.close()
  del mySocket
