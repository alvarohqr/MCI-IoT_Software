from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room,emit
from Control import Control
from Constantes import Constantes
import json

app = Flask(__name__)
app.config['DEBUG'] = True
socketio = SocketIO(app)
control = Control()

constantes = Constantes()

#Lista de usuarios en linea.
users = []


@socketio.on('cambiarCorreoDestinatario')
def cambiarCorreoDestinatario(datos):    
    #Lo convierte en json
    correo = datos.decode('unicode_escape')    
    print('Peticion para agregar auto de: ' ,request.sid)    
    respuesta = control.cambiarCorreoDestinatario(correo)

    #Manda la respuesta al cliente.
    emit('cambiarCorreoDestinatario',respuesta.encode(),room=request.sid)


@socketio.on('cambiarLimiteMinimaCapacidad')
def cambiarLimiteMinimaCapacidad(datos):  
    limiteMin = datos.decode('unicode_escape')    
    print('Peticion para cambiar Limite Minima Capacidad de: ' ,request.sid)    
    respuesta = control.cambiarLimiteMinimaCapacidad(limiteMin)

    #Manda la respuesta al cliente.
    emit('cambiarLimiteMinimaCapacidad',respuesta.encode(),room=request.sid)

@socketio.on('cambiarMedioNotificacion')
def cambiarMedioNotificacion(datos):  
    medioNotificacion = datos.decode('unicode_escape')    
    print('Peticion para cambiar Medio de Notificacion de: ' ,request.sid)    
    respuesta = control.cambiarMedioNotificacion(medioNotificacion)

    #Manda la respuesta al cliente.
    emit('cambiarLimiteMinimaCapacidad',respuesta.encode(),room=request.sid)
@socketio.on('cambiarLimiteTemperatura')
def cambiarLimiteTemperatura(datos):  
    aux_json =datos
    min = aux_json["min"]
    max = aux_json["max"]

    print("Min: ",min)
    print("Max: ",max)
    print('Peticion para cambiar Limite Temperatura de: ' ,request.sid)    
    respuesta = control.cambiarLimiteTemperatura(min,max)

    #Manda la respuesta al cliente.
    emit('cambiarLimiteTemperatura',respuesta.encode(),room=request.sid)


@socketio.on('cambiarContraseña')
def cambiarContraseña(datos):  
    password = datos.decode('unicode_escape')    
    print('Peticion para cambiar la contraseña de: ' ,request.sid)    
    respuesta = control.cambiarContraseña(password)

    #Manda la respuesta al cliente.
    emit('cambiarContraseña',respuesta.encode(),room=request.sid)


@socketio.on('obtenerDatosNotificaciones')
def obtenerDatosNotificaciones():  
    print('Peticion para obtener los datos de las notificaciones de: ' ,request.sid)    
    respuesta = control.obtenerDatosNotificaciones()

    #Manda la respuesta al cliente.
    emit('obtenerDatosNotificaciones',respuestaroom=request.sid)

@socketio.on('cambiarCorreoRemitente')
def cambiarCorreoRemitente(datos):    
    #Lo convierte en json
    correo = datos.decode('unicode_escape')    
    print('Peticion para cambiar Correo Remitente de: ' ,request.sid)    
    respuesta = control.cambiarCorreoRemitente(correo)

    #Manda la respuesta al cliente.
    emit('cambiarCorreoRemitente',respuesta.encode(),room=request.sid)

@socketio.on('agregarAuto')
def agregarAuto(string):    
    #Lo convierte en json
    datos = json.loads(string.decode('unicode_escape'))
    
    inicio =  datos['inicio']
    destino =  datos['destino']
    
    print('Peticion para agregar auto de: ' ,request.sid)    
    respuesta = control.agregarAutomovilSemaforo(inicio,destino)
    
    #Manda la respuesta al cliente.
    emit('agregarAuto',respuesta.encode(),room=request.sid)
    
@socketio.on('depurarDatos')
def depurarDatos():
    print('Peticion de depurar datos de: ' ,request.sid)    
    respuesta = control.depurarDatos()
    emit("depurarDatos",respuesta.encode(),room=request.sid)

@socketio.on('analisisInferencia')
def analisisInferencia():
    print('Peticion de analisis de Inferencia de: ' ,request.sid)    
    respuesta = control.analisisInferencia()
    emit("analisisInferencia",respuesta.encode(),room=request.sid)

@socketio.on('notificar')
def notificar(string):
    print('Peticion de notificar de: ' ,request.sid)    

    datos = string
    titulo = datos["titulo"]
    contenido = datos["contenido"]

    respuesta = control.notificar(titulo,contenido)
    emit("notificar",respuesta.encode(),room=request.sid)


@socketio.on('correrTiempo')
def correrTiempo():    
    print('Peticion de correr tiempo de: ' ,request.sid)    
    respuesta = control.moverUnTurno()
    print(users)
    for a in users:        
        print(a)
        #Manda la respuesta al cliente.
        emit('correrTiempo',respuesta.encode(),room=a)
    
@socketio.on('login')
def login():
    print(users)
    try:
        if(users == []):
            emit('login',("Se conecto el usuario: "+request.sid).encode(), room=request.sid)
            users.append(request.sid)
        else:
            users.index(request.sid) 
            emit('login',("Se conecto el usuario: "+request.sid).encode(), room=request.sid)
            users.append(request.sid)
    except ValueError:
        print("Ya se encuentra logeado el usuario")
        
@socketio.on('cambiarEstadoSemaforo')
def cambiarEstadoSemaforo(datos):
    semaforo = datos.decode('unicode_escape')    
    print('Peticion de cambio de estado de semaforo de: ' ,request.sid)    
    respuesta = control.cambiarEstadoSemaforo(semaforo)
    for a in users:
        #Manda la respuesta al cliente.
        emit('cambiarEstadoSemaforo',respuesta.encode(),room=a)
    

@socketio.on('monitorear')
def monitorear():
    print('Peticion de monitoreo de: ' ,request.sid)    
    #Regresa el estado de los semaforos.
    respuesta = control.monitorear()
    #Manda la respuesta al cliente.
    emit('monitorear',respuesta.encode(),room=request.sid)
    
@socketio.on('join')
def on_join(data):    
    room = data['room']  
    
    
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    print("Se desconectó el usuario: ", request.sid)
    users.remove(request.sid)
    leave_room(room)

if __name__ == '__main__':
    socketio.run(app)