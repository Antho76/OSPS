import multiprocessing
import time
import os
import threading

serv_pid = 0
disp_pid = 0 

def server(shared_value, fifo_path, sdfifo):
    global serv_pid
    serv_pid = os.getpid()
    print(f"Server process ID: {serv_pid}")
    
    # Ouverture du tube
    with open(fifo_path, 'r') as fifo:
        while True:
            last_serv_activity.value = int(time.time())  # Mettre à jour l'activité du serveur
            
            # Lecture du tube
            data = fifo.read()
            if not data:
                print("Server breaking")
                break
            
            print(f"Serveur received data : {data.strip()}")

            match data.strip():
                case "SUM":
                    shared_value.value = shared_value.value + 1
                case "HALF":
                    shared_value.value = shared_value.value // 2

            with open(sdfifo, 'w') as fifo2:
                fifo2.write("done")
                fifo2.flush()
            
            print(f"Server updated shared value to: {shared_value.value}")

def watchdog():
    print("Watchdog launched")
    print("Launching dispatcher....")
    try:
        dispatcher()
    except:
        print("")
    finally:
        print("Launched !")
    
    global serv_pid
    global disp_pid

    while True:
        
        time.sleep(2)
        current_time = int(time.time())
        #print(current_time, last_serv_activity.value)
        if current_time - last_serv_activity.value > 10:
            print("Serveur inactif depuis 10 sec, arrêt du serveur.")
            os.kill(serv_pid, 9)  # Terminer le processus serveur
            break  # Sortir de la boucle watchdog si le serveur est arrêté
            
        if current_time - last_disp_activity.value > 10:
            print("Dispatcher inactif depuis 10 sec, arrêt du dispatcher.")
            os.kill(disp_pid, 9)  # Terminer le processus dispatcher
            break  # Sortir de la boucle watchdog si le dispatcher est arrêté

def dispatcher():
    global disp_pid
    disp_pid = os.getpid()

    try:
        nombre = int(input("Entrez un nombre\n"))
        print(f"Vous avez entré le nombre : {nombre}")

    except ValueError:
        print("Ce n'est pas un nombre entier valide.")
        nombre = 0

    # Créer un tube 
    fifo_path = 'dsfifo'
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)
    
    sdfifo = 'sdfifo'
    if not os.path.exists(sdfifo):
        os.mkfifo(sdfifo)

    # Créer un segment de mémoire partagée
    shared_value = multiprocessing.Value('i', nombre)  # 'i' pour un entier

    # Créer le processus serveur
    server_process = multiprocessing.Process(target=server, args=(shared_value, fifo_path, sdfifo))
    
    # Démarrer le serveur
    server_process.start()
    

    last_disp_activity.value = int(time.time())

    with open(fifo_path, 'w') as fifo:
        fifo.write(f"SUM")
        fifo.flush()

    with open(sdfifo, 'r') as fifo2:
        data = None
        while not data:
            data = fifo2.read()
            print("Waiting for server response")

    # Attendre que le serveur se termine
    server_process.join()
    
    print(f"Final shared value: {shared_value.value}")

    # Nettoyage tube
    os.remove(fifo_path)
    os.remove(sdfifo)

if __name__ == "__main__":

    #Init variables
    last_disp_activity = multiprocessing.Value('i',int(time.time()))
    last_serv_activity = multiprocessing.Value('i',last_disp_activity.value)

    # Démarrer le watchdog
    watchdog_thread = threading.Thread(target=watchdog)
    watchdog_thread.daemon = True
    watchdog_thread.start()

    while True:
        dispatcher()
