import pymysql
import paho.mqtt.client as mqtt
import time

#se notifica la conexión al broker
def on_connect(client,userdata,flags,rc):
    print("Conectado - Código de resultado: " + str(rc))
    client.subscribe("topico/#")
    
#el callback cuando se recibe un mensaje
def on_message(client,userdata,msg):
    now = time.strftime('%Y-%m-%d %H-%M-%S')
    print(msg.topic+":"+str(msg.payload.decode("utf-8")))
    

client = mqtt.Client()
client.on_connect=on_connect
client.on_message = on_message
client.connect('localhost')
client.loop_forever()
