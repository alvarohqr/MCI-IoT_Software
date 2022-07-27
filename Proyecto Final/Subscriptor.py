import paho.mqtt.client as mqtt #importa el cliente
import time
import pymongo
from Constantes import Constantes

def on_message(client, userdata, message):
    constantes = Constantes()
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Datos"]
    datosPendientes = mydb["Datos_Pendientes"]

    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    #Procesa el mensaje.
    if(message.topic == constantes.SIGNAL_MOVIMIENTO):
        #Busca el elemento que representa el ultimo mensaje recibido.
        arrayDatosPendientes = datosPendientes.find()
        for x in arrayDatosPendientes:
            if(x["tipo"] == constantes.SIGNAL_MOVIMIENTO):         
                myquery = { "tipo": constantes.SIGNAL_MOVIMIENTO }
                newvalues = { "$set": { "mensaje": message.payload.decode("utf-8") } }
                datosPendientes.update_one(myquery, newvalues)      
                break
    elif(message.topic == constantes.SIGNAL_TEMPERATURA):
        #Busca el elemento que representa el ultimo mensaje recibido.
        arrayDatosPendientes = datosPendientes.find()
        for x in arrayDatosPendientes:
            if(x["tipo"] == constantes.SIGNAL_TEMPERATURA):
                myquery = { "tipo": constantes.SIGNAL_TEMPERATURA }
                newvalues = { "$set": { "mensaje": message.payload.decode("utf-8") } }
                datosPendientes.update_one(myquery, newvalues)          
       
broker_address="127.0.0.1"

print("Crea una nueva instancia")
client = mqtt.Client("Cliente2") #Crea nueva instancia
client.on_message=on_message #Adjunta una funcion al callback

print('Conectando con el servidor " ' + broker_address + ' " .')
client.connect(broker_address) #Conectar al broker.
print('Se ha conectado con exito al broker.')
client.loop_start() #Inicia el loop

print("Subscribirse al topico","ejemplo/sala1")
client.subscribe("ejemplo/sala1")

time.sleep(6000000) # Espera
client.loop_stop() #Termina el loop