'''(Servidor): Aplicación centralizada que hereda la lógica del
servidor concurrente con hilos (Threads), quedando a la escucha en un puerto
para aceptar las conexiones simultáneas de múltiples estaciones.'''
import socket 
import threading


HEADER = 64 #indica la longitud del mensaje
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

'''Esta función se ejecuta en un hilo nuevo por cada estación que se conecta. 
conn es el socket específico de esa conexión; addr es la IP/puerto de quien llama 
(no se usa dentro, pero se recibe por si hiciera falta).
def handle_client(conn, addr)'''

def handle_client(conn, addr):
   
    msg_length = conn.recv(HEADER).decode(FORMAT)
    
    if msg_length:
        msg_length = int(msg_length) #cuantos bytes mide el mensaje real
        msg = conn.recv(msg_length).decode(FORMAT)
        campos = msg.split("#")
        #lo que recibe el servidor tiene tres parametros, el primero es "REGISTRO" y los dso siguientes existen
        if len(campos) ==3 and campos[0]=="REGISTRO" and campos[1] and campos[2]:
            print(f"{campos[1]}#{campos[2]}")
            send("STATUS#OK#Estacion registrada correctamente",conn)
        else:
            send("STATUS#ERROR",conn)

    conn.close()
    
def send(msg,conn):
    message = msg.encode(FORMAT) #texto a enviar convertido a bytes
    msg_length = len(message) #cuantos bytes mide

    #rellena con espacios hasta llegar a 64 bytes.
    # Envía primero la cabecera y luego el mensaje.
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def start():
    server.listen()
    print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    #programa ya es un hilo vivo asi que se le resta 1
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
            
        

######################### MAIN ##########################


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[STARTING] Servidor inicializándose...")

start()
