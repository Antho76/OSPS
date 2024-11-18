#! /usr/bin/env python3
# _*_ coding: utf8 _*_
#
# Test des signaux en Python entre deux processus père/fils lancés via fork() avec controle d'erreur
# et utilisation de wait pour que le serveur_secondaire_fils s'exécute avant le serveur_principal_pere
#
# La gestion des signaux n'est ni rigoureuse ni complete, mais suffisante pour un premier test,
# à vous de compléter ;-)
#
# Cf : https://docs.python.org/3/library/signal.html
#
import os, time, signal
import threading

# Le serveur secondaire réagit au signal SIGUSR1
# Normalement pas d'affichage dans un handler --> Juste pour débuggage et supprimer dans votre code définitif
# De même, il ne faut pas envoyer de signaux dans un handler normalement, mais j'accepte si cela peut simplifier votre code
def serveur_secondaire_sigusr1_handler(signum, frame): 
    if signum == signal.SIGUSR1: 
        print('Signal SIGUSR1 recu')

# Le serveur principal réagit au signal SIGUSR2
# Normalement pas d'affichage dans un handler --> Juste pour débuggage et supprimer dans votre code définitif
# De même, il ne faut pas envoyer de signaux dans un handler normalement, mais j'accepte si cela peut simplifier votre code
def serveur_principal_sigusr2_handler(signum, frame): 
    if signum == signal.SIGUSR2: 
        print('Signal SIGUSR2 recu')

def serveur_secondaire_fils():
    print ("Je suis le serveur_secondaire_fils identifie par le pid ",  os.getpid(), " pid de mon serveur_principal_pere ", os.getppid(), "\n")
    signal.signal(signal.SIGUSR1, serveur_secondaire_sigusr1_handler)
    while True: 
         print('Fils en attente de signal...') 
         try:
             # Code du serveur secondaire à placer ici par exemple
             signal.pause()
             os.kill(os.getppid(),signal.SIGUSR2)
         except Exception as e:
             print ('error -->',str(e))
             pass
         print ("Le fils boucle...")
    os._exit(0)
    
def serveur_principal_pere():
    print ("Je suis le serveur_principal_pere identifie par le pid ", os.getpid(), " mon serveur_secondaire_fils a le pid ", newpid, "\n")
    signal.signal(signal.SIGUSR2, serveur_principal_sigusr2_handler)
    while True: 
         print("Pere en attente d'envoi d'un signal...") 
         try:
             # Code du serveur secondaire à placer ici par exemple
             time.sleep(2)
             os.kill(newpid,signal.SIGUSR1)
         except Exception as e:
             print ('error -->',str(e))
             pass
         print ("Le père boucle...")
    
newpid = os.fork()
if newpid < 0:
    print("fork() impossible")
    os.abort()
if newpid == 0:
    serveur_secondaire_fils()
else:
    serveur_principal_pere()
    print ("Debut d'attente du serveur_secondaire_fils dans le processus serveur_principal_pere")
    _, status = os.waitpid(newpid, 0)
    print ("Fin d'attente du serveur_secondaire_fils dans le processus serveur_principal_pere")
    coderetour = os.WEXITSTATUS(status)
    if os.WIFEXITED (status):
        print ("le code de retour de mon serveur_secondaire_fils est : ", coderetour)
