import confluent_kafka  
import sys
import time




#python WM_FO <IP boker><Puerto broker> <ID operario>

if(len(sys.argv)==4):
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    ID_OP=sys.argv[3]
    

else:
    print ("Oops!. Parece que algo falló. Necesito estos argumentos:  <IP broker><Puerto broker> <ID operario>")
    sys.exit()

def enviar_petición(ws_id):
    msg = (f"ACTIVAR#{ws_id}#{ID_OP}")
    print(msg)

try:
    ws_id =1
    while True:
        enviar_petición(ws_id)
        ws_id = ws_id+1
        time.sleep(4)
except KeyboardInterrupt:
    print("\n Programa detenido")
    sys.exit(0)
    