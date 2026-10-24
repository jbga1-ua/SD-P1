'''Cliente / Monitor): El módulo monitor de la estación de riego que
utiliza la estructura del cliente básico para conectarse a la central e
identificarse.'''
import socket
import sys
import time

HEADER = 64 #indica la longitud del mensaje
SERVER_MONITOR= socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'


def send(msg,conn):
    message = msg.encode(FORMAT) #texto a enviar convertido a bytes
    msg_length = len(message) #cuantos bytes mide

    #rellena con espacios hasta llegar a 64 bytes.
    # Envía primero la cabecera y luego el mensaje.
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    

 
def handle_client(conn, addr):

    conn.settimeout(1)

    try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        
        if msg_length:
            msg_length = int(msg_length) #cuantos bytes mide el mensaje real
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg== "KO":
                print("Estacion averiada")
                send("STATUS#KO# FUGA EXISTENTE",conn)
            if msg == "OK":
                print("Estacion okay")
                send("STATUS#OK# ESTACION OK",conn)
            
    except socket.timeout:
        print("Timeout exception")
        
        

    

def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER_MONITOR}")
    conn_engine, addr = server.accept()

    while True:
        send("PING", conn_engine)
        handle_client(conn_engine, addr)

        time.sleep(1)


#REGISTRO#<ID_ESTACION>#<UBICACION>
#python  WM_WS_M.py Puerto_Engine <IP> Puerto_central WS-04 "River Park"
if  (len(sys.argv) == 6):
    SERVER_CENTRAL = sys.argv[2]
    PORT = int(sys.argv[3])
    ADDR_CENTRAL = (SERVER_CENTRAL, PORT)
    ADDR_MONITOR = (SERVER_MONITOR, int(sys.argv[1]))
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR_CENTRAL)
    print (f"Establecida conexión en [{ADDR_CENTRAL}]")

    msg= f"REGISTRO#{sys.argv[4]}#{sys.argv[5]}"
    
    print("Envio al servidor: ", msg)
    send(msg,client)

    msg_length = client.recv(HEADER).decode(FORMAT)
        
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print(msg)

    client.close()
else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos: <Puerto_Monitor> <ServerIP> <Puerto_Central> <ID_ESTACION> <UBICACION>")
    sys.exit()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR_MONITOR)

print("[STARTING] Servidor inicializándose...")

start()