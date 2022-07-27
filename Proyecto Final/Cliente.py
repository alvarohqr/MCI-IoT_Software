import socketio
from Constantes import Constantes
import winsound

sio = socketio.Client()
constantes = Constantes()



#Metodo para desplegar el menu principal
def menu():
    import json
    print('----------------Menu Proyecto-----------------')
    print('1.Monitoriar Mapa')
    print('2.Agregar Auto en Semaforo')
    print('3.Cambiar Estado Semaforo')
    print('4.Depurar Datos')
    print('5.Correr Tiempo')
    print('6.Notificar')
    print("7.Configuraciones.")
    print('8.Análisis de inferencia')
    print('9.Cerrar Aplicacion')
    respuesta = input()
    
    #Si es escoge monitorear
    if(respuesta == "1"):
        sio.emit('monitorear')
    
    #Si es escoge Agregar auto en semaforo    
    elif(respuesta == "2"):
        semaforoInicio = input('Semaforo Inicio: ')
        semaforoDestino = input('Semaforo Destino: ')
                
        a = {
            'inicio': semaforoInicio,
            'destino': semaforoDestino
            }
                
        sio.emit('agregarAuto', json.dumps(a).encode())
    
    #Si es escoge Cambiar Estado Semaforo
    elif(respuesta == "3"):    
        numSemaforo = input("# de Semaforo a cambiar de estado: ")        
        sio.emit('cambiarEstadoSemaforo',numSemaforo.encode())
    elif(respuesta == "4"):
        sio.emit('depurarDatos')
    #Si es escoge Correr Tiempo
    elif(respuesta == "5"):
        sio.emit('correrTiempo')
    elif(respuesta == "6"):
        aux_json = {"titulo":"Notificación arbitraria","contenido":"Este es un correo de prueba."}
        sio.emit('notificar',aux_json)
    elif(respuesta == "7"):
        respuesta = ""
        print("1.Cambiar Correo destinatario.")
        print("2.Cambiar Correo remitente.")
        print("3.Cambiar Contraseña.")
        print("4.Cambiar Limite Minima Capacidad.")
        print("5.Cambiar Limite Temperatura.")
        print("6.Cambiar Medio de notificacion.")
        respuesta = input()
        if(respuesta == "1"):
            nuevoCorreo = input("Nuevo correo destinatario: ")
            sio.emit('cambiarCorreoDestinatario',nuevoCorreo.encode())
        elif(respuesta == "2"):
            nuevoCorreo = input("Nuevo correo remitente: ")
            sio.emit('cambiarCorreoRemitente',nuevoCorreo.encode())
        elif(respuesta == "3"):
            password = input("Nueva Contraseña: ")
            sio.emit('cambiarContraseña',password.encode())
        elif(respuesta == "4"):
            minTemp = input("Nueva Minima Capacidad: ")
            sio.emit('cambiarLimiteMinimaCapacidad',minTemp.encode())
        elif(respuesta == "5"):            
            min = input("Limite minimo: ")
            max = input("Limite maximo: ")
            aux_json = {"min":min,"max":max}
            sio.emit('cambiarLimiteTemperatura',aux_json)
        elif(respuesta == "6"):                
            print("1.Correo Electronico")
            print("2.Telegram")
            print("3.Slack")
            medioNotificacion = input("")

            if(medioNotificacion == "1"):
                respuesta = Constantes.MODO_CORREO
            elif(medioNotificacion == "2"):
                respuesta = Constantes.MODO_TELEGRAM
            elif(medioNotificacion == "3"):
                respuesta = Constantes.MODO_SLACK

            sio.emit('cambiarMedioNotificacion',respuesta.encode())
    elif(respuesta == "8"):
        sio.emit('analisisInferencia')
        return
    #Si es escoge terminar la aplicacion.
    elif(respuesta == "9"):
        return
    else:
        menu()

def hacer_Ruido():
    dur = 1000
    freq = 440
    #winsound.Beep(frequency=freq,duration=dur)

@sio.event
def connect():
    print("Conectado al servidor")
    sio.emit('login')    

@sio.on('login')
def login(data):
    print(data.decode('unicode_escape'))
    menu()
    
@sio.event
def disconnect():
    print("Desconectado")



@sio.on('obtenerDatosNotificaciones')
def obtenerDatosNotificaciones(data):
    print(data)
    hacer_Ruido()
    menu()

@sio.on('analisisInferencia')
def obtenerDatosNotificaciones(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()


@sio.on('cambiarCorreoRemitente')
def cambiarCorreoRemitente(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()
    
@sio.on('cambiarCorreoDestinatario')
def cambiarCorreoDestinatario(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('cambiarLimiteMinimaCapacidad')
def cambiarLimiteMinimaCapacidad(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('cambiarLimiteTemperatura')
def cambiarLimiteTemperatura(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('cambiarMedioNotificacion')
def cambiarMedioNotificacion(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('cambiarContraseña')
def cambiarContraseña(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()
@sio.on('agregarAuto')
def agregarAuto(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('notificarCorreo')
def notificarCorreo(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()


@sio.on('cambiarEstadoSemaforo')
def cambiarEstadoSemaforo(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('monitorear')
def monitorear(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('correrTiempo')
def correrTiempo(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

@sio.on('depurarDatos')
def correrTiempo(data):
    print(data.decode('unicode_escape'))
    hacer_Ruido()
    menu()

sio.connect('http://127.0.0.1:5000')