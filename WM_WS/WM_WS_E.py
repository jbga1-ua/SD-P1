
import socket
import sys
import threading


HEADER = 64 #indica la longitud del mensaje
FORMAT = 'utf-8'
ESTADO = "OK"


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    #rellena con espacios hasta llegar a 64 bytes.
    # Envía primero la cabecera y luego el mensaje.
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def esperar_tecla():
    global ESTADO
    while True:
        input()
        if ESTADO == "OK":
            ESTADO = "KO"
            print("Simulando averia (KO)")
        else:  
            ESTADO = "OK"
            print("Vulve a OK")
        


# recibe python WM_WS_E <IP><Puerto monito>

if(len(sys.argv)==3):
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR=(SERVER,PORT)
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print(f"Conexion establecida en [{ADDR}]")
    

else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos:  <ServerIP> <Puerto_Monitor>")
    sys.exit()


hilo_tecla=threading.Thread(target=esperar_tecla)
hilo_tecla.start()

try: 
    while True:

        msg_length= client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)

            if msg == "PING":
                print("PING recibido")
                send(ESTADO)
except:
    print("Cayó la conexion")
