from os import X_OK
from flask.wrappers import Response
import pymongo
from flask import Flask, request, jsonify,render_template
from Constantes import Constantes
import statistics
import time
import mimetypes
import jyserver.Flask as jsf
import json
from bson.json_util import dumps

mimetypes.add_type("application/javascript", ".js", True)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Datos"]

datosSinDepurar = mydb["Datos_Sin_Depurar"]
datosConCalidad = mydb["Datos_Con_Calidad"]
datosSinCalidad = mydb["Datos_Sin_Calidad"]
datosPendientes = mydb["Datos_Pendientes"]
datosNotificaciones = mydb["Datos_Notificaciones"]

app = Flask(__name__)
constantes = Constantes()

@app.route('/')
def index():
    return render_template('index.html')

def primerFiltro(datos):
    numSemaforo = datos['numSemaforo']
    temperatura = datos['temperatura']
    cantidadAutos = datos['cantidadAutos']

    if(Constantes.TEMPERATURA[0]>int(temperatura) or Constantes.TEMPERATURA[1]<int(temperatura)):
        return False
    if(Constantes.TRAFICO[0]>int(cantidadAutos) or Constantes.TRAFICO[1]<int(cantidadAutos)):
        return False
    if(Constantes.SEMAFOROS[0]>int(numSemaforo) or Constantes.SEMAFOROS[1]<int(numSemaforo)):
        return False
    return True


@app.route('/cambiarCorreoDestinatario', methods=['POST'])
def cambiarCorreoDestinatario():
    correoDest = request.json['correo']

    myquery = { "tipo": constantes.NOTIFICACION}
    newvalues = { "$set": { "correoDestinatario": correoDest } }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Se modificó el correo del destinatario"

@app.route('/cambiarCorreoRemitente', methods=['POST'])
def cambiarCorreoRemitente():
    correoRemitente = request.json['correo']

    myquery = { "tipo": constantes.NOTIFICACION}
    newvalues = { "$set": { "correoRemitente": correoRemitente } }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Se modificó el correo del remitente"

@app.route('/obtenerDatosNotificaciones', methods=['GET'])
def obtenerDatosNotificaciones():
    array = datosNotificaciones.find()

    for x in array:
        if(x["tipo"] == constantes.NOTIFICACION):
            print(x)
            aux = x["limiteTemperatura"]
            a = aux[0]
            b = aux[1]

            aux_json = {
                "tipo": x['tipo'],
                "limiteMinCapacidad":x['limiteMinCapacidad'],
                "limiteTemperatura":[a,b],
                "correoDestinatario":x["correoDestinatario"],
                "correoRemitente":x["correoRemitente"],
                "password": x["password"],
                "limiteMin":x["correoRemitente"],
                "modo": x["modo"]
            }
            return aux_json

    return {}


@app.route('/cambiarLimiteTemperatura', methods=['POST'])
def cambiarLimiteTemperatura():
    min = request.json['min']
    max = request.json['max']

    myquery = { "tipo": constantes.NOTIFICACION}
    newvalues = { "$set": { "limiteTemperatura": [min, max] } }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Se modificó el limite de la temperatura."




@app.route('/cambiarLimiteMinimaCapacidad', methods=['POST'])
def cambiarLimiteMinimaCapacidad():
    limiteMin = request.json['limiteMin']

    myquery = { "tipo": constantes.NOTIFICACION}
    newvalues = { "$set": { "limiteMin": limiteMin } }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Se modificó el limite de Minima Capacidad"

@app.route('/cambiarContraseña', methods=['POST'])
def cambiarContraseña():
    password = request.json['password']

    myquery = { "tipo": constantes.NOTIFICACION}
    newvalues = { "$set": { "password": password } }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Se modificó la contraseña"



@app.route('/cambiarFormulario', methods=['POST'])
def cambiarFormulario():
    correoDest = request.form['correoDestinatario']
    correoRemitente = request.form['correoRemitente']
    contra = request.form['contra']

    array = datosNotificaciones.find()
    for x in array:
        if(x["tipo"] == constantes.NOTIFICACION):
            myquery = { "tipo": constantes.NOTIFICACION}
            newvalues = { "$set": { "correoDestinatario": correoDest, "correoRemitente":correoRemitente, "password":contra } }

            datosNotificaciones.update_one(myquery, newvalues)


    return "Se ha modificado los valores."


@app.route('/determinarActualizacion')
def determinarActualizacion():    
    respuesta = {}
    arreglo = datosNotificaciones.find()
    for x in arreglo:
        if(x["tipo"] == constantes.NOTIFICACION_AUTOS):
            if(x["actualizar"] == constantes.NOTIFICACION_ACTUALIZAR_SI):
                respuesta["NOTIFICACION_AUTOS"] = x
                myquery = { "tipo": constantes.NOTIFICACION_AUTOS}
                newvalues = { "$set": { "actualizar": constantes.NOTIFICACION_ACTUALIZAR_NO} }
                datosNotificaciones.update_one(myquery, newvalues)
        elif(x["tipo"] == constantes.NOTIFICACION_TEMPERATURA):
            if(x["actualizar"] == constantes.NOTIFICACION_ACTUALIZAR_SI):
                respuesta["NOTIFICACION_TEMPERATURA"] = x
                myquery = { "tipo": constantes.NOTIFICACION_TEMPERATURA}
                newvalues = { "$set": { "actualizar": constantes.NOTIFICACION_ACTUALIZAR_NO} }
                datosNotificaciones.update_one(myquery, newvalues)
    
    return parse_json(respuesta)

@app.route('/configuracion')
def configuracion():
    return render_template('opciones.html')

@app.route('/esperarSeñalMovimiento', methods=['get'])
def esperarSeñalMovimiento():
    noSeRecibio = True    
    while(noSeRecibio):
        arrayDatosPendientes = datosPendientes.find()
        print("Se esperaran 5 segundos para recibir la señal de movimiento.")
        time.sleep(1)
        for x in arrayDatosPendientes:
            if(x["tipo"] == constantes.SIGNAL_MOVIMIENTO and x["mensaje"] != ""):
                noSeRecibio = False
                print("Se recibio la señal de movimiento")
                break
    return "Se ha recibido la señal de movimiento."

    

@app.route('/actualizarPagina_autos', methods=['Post'])
def actualizarPagina_autos():
    cantidadAutosSemaforo1 = request.json['cantidadAutosSemaforo1']
    cantidadAutosSemaforo2 = request.json['cantidadAutosSemaforo2']
    cantidadAutosSemaforo3 = request.json['cantidadAutosSemaforo3']
    cantidadAutosSemaforo4 = request.json['cantidadAutosSemaforo4']
    cantidadAutosSemaforo5 = request.json['cantidadAutosSemaforo5']
   
    myquery = { "tipo": constantes.NOTIFICACION_AUTOS}
    newvalues = { "$set": { "actualizar": constantes.NOTIFICACION_ACTUALIZAR_SI,"cantidadAutosSemaforo1":cantidadAutosSemaforo1,"cantidadAutosSemaforo2":cantidadAutosSemaforo2,"cantidadAutosSemaforo3":cantidadAutosSemaforo3,"cantidadAutosSemaforo4":cantidadAutosSemaforo4,"cantidadAutosSemaforo5":cantidadAutosSemaforo5 } }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Los Datos se han actualizado en la BD"

@app.route('/analisisInferencia', methods=['GET'])
def analisisInferencia():
    a = datosConCalidad.find()
    aux_json = {}

        
    #Crear json
    for aux in a:
        {"_id":aux["_id"],"temperatura":aux["temperatura"],"cantidadAutos":aux["cantidadAutos"]}
        id = aux["_id"]
        aux_json[str(id)]={"temperatura":aux["temperatura"],"cantidadAutos":aux["cantidadAutos"]}

    return aux_json



@app.route('/cambiarMedioNotificacion', methods=['Post'])
def cambiarMedioNotificacion():
    medioNotificacion = request.json["medioNotificacion"]
    myquery = { "tipo": constantes.NOTIFICACION}
    newvalues = { "$set": { "modo": medioNotificacion} }

    datosNotificaciones.update_one(myquery, newvalues)
    return "Se ha actualizado el medio de notificacion."


@app.route('/datos', methods=['Post'])
def datos():    
    
        
    myquery = { "tipo": constantes.SIGNAL_TEMPERATURA}
    newvalues = { "$set": { "mensaje": "" } }

    datosPendientes.update_one(myquery, newvalues)

    noSeRecibio = True
    temperatura = ""
    while(noSeRecibio):
        #Busca el elemento que representa el ultimo mensaje recibido.
        arrayDatosPendientes = datosPendientes.find()
        print("Se esperaran 5 segundos para recibir la señal de temperatura.")
        time.sleep(1)

        arrayDatosPendientes = datosPendientes.find()
        for x in arrayDatosPendientes:
            if(x["tipo"] == constantes.SIGNAL_TEMPERATURA and x["mensaje"] != ""):
                noSeRecibio = False
                print("Se recibio la señal de temperatura")
                temperatura = x["mensaje"]
                break


    numSemaforo = request.json['numSemaforo']
    cantidadAutos = request.json['cantidadAutos']    
    json = {"numSemaforo":numSemaforo,"temperatura": temperatura, "cantidadAutos": cantidadAutos} 

    print("numSemaforo: ", numSemaforo)
    print("temperatura: ", temperatura)
    print("cantidadAutos: ", cantidadAutos)

    #Se debe cambiar
    if(primerFiltro(json)):
                
        r1 = obtenerDatosNotificaciones()

        auxArray = r1["limiteTemperatura"]
        limiteInferior = int(auxArray[0])
        limiteSuperior = int(auxArray[1])
        temperatura = int(temperatura)

        if(limiteInferior<temperatura and limiteSuperior>temperatura):
            datosSinDepurar.insert_one(json)
            print("Dato Agregado a la BD exitosamente")
            #Se actualiza la pagina.
            myquery = { "tipo": constantes.NOTIFICACION_TEMPERATURA}
            newvalues = { "$set": { "actualizar": constantes.NOTIFICACION_ACTUALIZAR_SI,"temperaturaSemaforo"+str(numSemaforo):temperatura } }

            datosNotificaciones.update_one(myquery, newvalues)
            return "Dato Agregado a la BD exitosamente"
        else:
            print("Los Datos a agregar no han pasado el segundo filtro")
            return "Los Datos a agregar no han pasado el segundo filtro"
    else:
        print("Los Datos a agregar no han pasado el primer filtro")
        return "Los Datos a agregar no han pasado el primer filtro"
    
@app.route('/depurarDatos', methods=['Get'])
def depurarDatos():
    arrayDatosSinDepurar = datosSinDepurar.find()
    arrayTemperaturaDatosSinDepurar = []
    arrayAutosDatosSinDepurar = []    

    for a in arrayDatosSinDepurar:
        arrayTemperaturaDatosSinDepurar.append(int(a["temperatura"]))
        arrayAutosDatosSinDepurar.append(int(a["cantidadAutos"]))


    desviacionEstandarTemperatura = statistics.stdev(arrayTemperaturaDatosSinDepurar)
    desviacionEstandarAutos = statistics.stdev(arrayAutosDatosSinDepurar)

    print("desviacionEstandarTemperatura = ", desviacionEstandarTemperatura)
    print("desviacionEstandarAutos = ",desviacionEstandarAutos)

    mediaTemperatura = statistics.mean(arrayTemperaturaDatosSinDepurar)
    mediaAutos = statistics.mean(arrayAutosDatosSinDepurar)

    print("mediaTemperatura",mediaTemperatura)
    print("mediaAutos",mediaAutos)

    arrayDatosSinDepurar = datosSinDepurar.find()
    for x in arrayDatosSinDepurar:
        #Si el valor se encuentra por debajo/arriba de la media menos/mas una desviacion estandar, entonces no se encuentra en el 68.0% de valores
        if((mediaTemperatura - desviacionEstandarTemperatura) > int(x["temperatura"]) or (mediaTemperatura+desviacionEstandarTemperatura) < int(x["temperatura"])):
            print("Dato sin calidad: ",x)
            datosSinCalidad.insert_one(x)            
        elif((mediaAutos - desviacionEstandarAutos) > int(x["cantidadAutos"]) or (mediaAutos+desviacionEstandarAutos < int(x["cantidadAutos"]))):
            datosSinCalidad.insert_one(x)
            print("Dato sin calidad: ",x)
        else:
            print("Dato con calidad: ",x)
            datosConCalidad.insert_one(x)
        datosSinDepurar.delete_one(x)

    #Manda notificacion a la pagina web para actualizarse.


    return "Los Datos se han depurado"

def parse_json(data):
    return json.loads(dumps(data))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9566,debug=True)
    