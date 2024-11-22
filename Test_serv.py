import multiprocessing
import time
import os

def server(shared_value, fifo_path, event, sdfifo):
    print(f"Server process ID: {os.getpid()}")

    #Ouverture du tube
    with open(fifo_path,'r') as fifo:
        while True:

            #lecture du tube
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

            with open(sdfifo,'w') as fifo2:
                fifo2.write("done")
                fifo.flush()
            
            print(f"Server updated shared value to: {shared_value.value}")
            event.set()

def dispatcher():
    try:
        nombre = int(input("Entrez un nombre\n"))
        print(f"Vous avez entré le nombre : {nombre}")

    except ValueError:

        print("Ce n'est pas un nombre entier valide.")
    
    # Créer un tube 
    fifo_path = 'dsfifo'
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)
    
    sdfifo = 'sdfifo'
    if not os.path.exists(sdfifo):
        os.mkfifo(sdfifo)

    # Créer un segment de mémoire partagée
    shared_value = multiprocessing.Value('i', nombre)  # 'i' pour un entier

    #Créer Event
    event = multiprocessing.Event()

    # Créer le processus serveur
    server_process = multiprocessing.Process(target=server, args=(shared_value,fifo_path,event,sdfifo))
    
    # Démarrer le serveur
    server_process.start()
    

    event.clear()

    with open(fifo_path, 'w') as fifo:

        fifo.write(f"HALF")
        fifo.flush()

    with open(sdfifo,'r') as fifo2:
        data=None
        while not data:
            data = fifo2.read()
            print("Waiting for server response")

    # Attendre que le serveur se termine
    server_process.join()
    
    print(f"Final shared value: {shared_value.value}")

    #Nettoyage tube
    os.remove(fifo_path)

if __name__ == "__main__":
    dispatcher()