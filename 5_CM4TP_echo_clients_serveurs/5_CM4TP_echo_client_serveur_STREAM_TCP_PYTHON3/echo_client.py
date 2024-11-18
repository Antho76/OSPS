#! /usr/bin/env python3
#
# A lancer en second

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1',2222))
print ("Connected to server")
data = """Ceci est un message multiligne
a transmettre au serveur
pour le tester."""
for line in data.splitlines():
  s.sendall(bytes(line,'UTF-8'))
  print ("Sent:", line)
  response = s.recv(1024)
  print ("Received", response)
s.close()
