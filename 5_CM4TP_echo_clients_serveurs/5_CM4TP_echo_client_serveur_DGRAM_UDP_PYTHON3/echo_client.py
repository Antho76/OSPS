#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# A lancer en second
#
import socket

HOST = '127.0.0.1'
PORT = 2222
server = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print ("Sending to server")
data = """Ceci est un message multiligne
a transmettre au serveur
pour le tester."""
for line in data.splitlines():
  s.sendto(bytes(line,'UTF-8'), server)
  print ("Sent:", line)
  response = s.recv(1024)
  print ("Received", response)
s.close()
