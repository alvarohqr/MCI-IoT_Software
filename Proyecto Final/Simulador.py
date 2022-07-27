import pymongo
from Constantes import Constantes

constantes = Constantes()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Datos"]

datosPendientes = mydb["Datos_Pendientes"]
datosNotificaciones = mydb["Datos_Notificaciones"]

while(True):
    print("1.Notificacion Temperatura")
    print("2.Notificacion Disponibilidad")
    print("3.Sensor Temperatura")
    print("4.Sensor Movimiento")

    respuesta = input()

    if(respuesta=="1"):
        arreglo = datosNotificaciones.find()
        for x in arreglo:            
            if(x["tipo"] == constantes.NOTIFICACION_TEMPERATURA):
                myquery = { "tipo": constantes.NOTIFICACION_TEMPERATURA}
                newvalues = { "$set": { "actualizar": constantes.NOTIFICACION_ACTUALIZAR_SI} }
                datosNotificaciones.update_one(myquery, newvalues)
    elif(respuesta=="2"):                     
        arreglo = datosNotificaciones.find()
        for x in arreglo:            
            if(x["tipo"] == constantes.NOTIFICACION_AUTOS):
                myquery = { "tipo": constantes.NOTIFICACION_AUTOS}
                newvalues = { "$set": { "actualizar": constantes.NOTIFICACION_ACTUALIZAR_SI} }
                datosNotificaciones.update_one(myquery, newvalues)
    elif(respuesta=="3"):                     
        arreglo = datosPendientes.find()
        for x in arreglo:            
            if(x["tipo"] == constantes.SIGNAL_TEMPERATURA):
                myquery = { "tipo": constantes.SIGNAL_TEMPERATURA}
                newvalues = { "$set": { "mensaje": input("Temperatura: ")} }                
                datosPendientes.update_one(myquery, newvalues)
    elif(respuesta=="4"):                     
        arreglo = datosPendientes.find()
        for x in arreglo:            
            if(x["tipo"] == constantes.SIGNAL_MOVIMIENTO):
                myquery = { "tipo": constantes.SIGNAL_MOVIMIENTO}
                newvalues = { "$set": { "mensaje": constantes.NOTIFICACION_ACTUALIZAR_SI} }
                datosPendientes.update_one(myquery, newvalues)
    else:
        continue