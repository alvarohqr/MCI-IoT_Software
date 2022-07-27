import pymysql
import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect('localhost')#conexión al broker (localhost)
try:
    while True:
        #publish(topic, payload=None, qos=0, retain=False)
        topico = client.publish("topico", input("Mensaje: "))

except KeyboardInterrupt:
    client.disconnect()
