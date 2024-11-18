#! /usr/bin/env python3
#
# A lancer en premier
#
# Ce serveur retourne ce qui lui a ete envoye
# (utilisable en TP pour tester scapy & cie)

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('',2222)) # '': toutes les interfaces disponibles
print ("Echo_server : en attente...")
sock.listen(5)
try:
  while True:
    newSocket, address = sock.accept()
    print ("Connected from", address)
    while True:
      receivedData = newSocket.recv(1024)
      if not receivedData: break
      # décommentez ce qui suit pour afficher le message reçu par le serveur :
      print (receivedData)
      newSocket.sendall(receivedData)
    newSocket.close()
    print ("Disconnected from", address)
finally:
  sock.close()
