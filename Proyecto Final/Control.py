from Semaforo import Semaforo
from Constantes import Constantes
from Automovil import Automovil
import requests
import json
from random import seed
from random import randint
import smtplib, ssl
import pymongo
import time
from sklearn.linear_model import LinearRegression

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
import matplotlib.pyplot as plt
class Control():

    def __init__(self):      
        #Inicializa el semaforo y establece la capacidad maxima.  
        self.semaforo_1 = Semaforo('1')
        self.semaforo_1.setCapacidadMaxima(5)        
                
        self.semaforo_2 = Semaforo('2')
        self.semaforo_2.setCapacidadMaxima(5)        
        
        self.semaforo_3 = Semaforo('3')
        self.semaforo_3.setCapacidadMaxima(5)        
        
        self.semaforo_4 = Semaforo('4')
        self.semaforo_4.setCapacidadMaxima(5)  
              
        self.semaforo_5 = Semaforo('5')
        self.semaforo_5.setCapacidadMaxima(5)      

        #Establece el siguiente semaforo de los semaforos
        self.semaforo_1.setSiguienteSemaforo(self.semaforo_2)
        self.semaforo_2.setSiguienteSemaforo(self.semaforo_3)
        self.semaforo_3.setSiguienteSemaforo(self.semaforo_4)
        self.semaforo_4.setSiguienteSemaforo(self.semaforo_5)
        self.semaforo_5.setSiguienteSemaforo(self.semaforo_1)

        #Lista de semaforos
        self.listaSemaforos = [self.semaforo_1,self.semaforo_2,self.semaforo_3,self.semaforo_4,self.semaforo_5]
        
        self.constantes = Constantes()

    #Metodo para obtener la cantidad de autos en circulacion        
    def getCantidadAutosEnCirculacion(self):
        respuesta = self.semaforo_1.getCantidadAutosEnEspera() + self.semaforo_2.getCantidadAutosEnEspera() + self.semaforo_3.getCantidadAutosEnEspera() + self.semaforo_4.getCantidadAutosEnEspera() + self.semaforo_5.getCantidadAutosEnEspera()
        return respuesta

    #Metodo para cambiar el estado del semaforo.
    #Parametros
    #numSemaforo - Numero del semaforo a cambiar el estado.
    def cambiarEstadoSemaforo(self,numSemaforo):
        respuesta = ''
        semaforo = self.listaSemaforos[int(numSemaforo)-1]        
        semaforo.setTipoTrafico(Constantes.TRAFICO_CAMBIO_ESTADO)
        estadoActual = semaforo.cambiarEstado()        

        semaforo.setTiempoEspera(0)            
        
    
        if(estadoActual == Constantes.ESTADO_SEMAFORO_VERDE):
            resSemaforo = "verde"
            self.enviarDatos(numSemaforo)
        elif(estadoActual == Constantes.ESTADO_SEMAFORO_ROJO):
            resSemaforo = "rojo"
            self.enviarDatos(numSemaforo)
        else:
            resSemaforo = "amarillo"
        respuesta += 'Se ha cambiado el semaforo # ' + str(numSemaforo) + '  a ' + resSemaforo
        respuesta += self.calcularTiempoSemaforos()
        return respuesta

    #Metodo para agregar un automovil a un semaforo.
    #Parametros
    #inicio - semaforo de inicio del automovil
    #destino - semaforo de destino del automovil
    def agregarAutomovilSemaforo(self,inicio,destino):
        respuesta = ""
        if(self.listaSemaforos[int(inicio)-1].getCapacidadMaxima() > self.listaSemaforos[int(inicio)-1].getCantidadAutosEnEspera()):
            self.listaSemaforos[int(inicio)-1].agregarAutoEnEspera(Automovil(inicio,destino))
            respuesta += self.calcularTiempoSemaforos()
            respuesta += 'Se ha agregado el automovil en el semaforo ' + str(inicio) + ' con destino a ' + str(destino) + " \n"
            
        else:
            respuesta += 'No se ha logrado agregar el automovil en el semaforo ' + str(inicio) + ' con destino a ' + str(destino)       + " \n"


        cantidadAutosSemaforo1 = self.listaSemaforos[int(1)-1].getCantidadAutosEnEspera()
        cantidadAutosSemaforo2 = self.listaSemaforos[int(2)-1].getCantidadAutosEnEspera()
        cantidadAutosSemaforo3 = self.listaSemaforos[int(3)-1].getCantidadAutosEnEspera()
        cantidadAutosSemaforo4 = self.listaSemaforos[int(4)-1].getCantidadAutosEnEspera()
        cantidadAutosSemaforo5 = self.listaSemaforos[int(5)-1].getCantidadAutosEnEspera()

        #Mandar peticion para que sea actualice la pagina.
        datos = {"cantidadAutosSemaforo1":cantidadAutosSemaforo1,"cantidadAutosSemaforo2":cantidadAutosSemaforo2,"cantidadAutosSemaforo3":cantidadAutosSemaforo3,"cantidadAutosSemaforo4":cantidadAutosSemaforo4,"cantidadAutosSemaforo5":cantidadAutosSemaforo5} 
        r1 = requests.post('http://127.0.0.1:9566/actualizarPagina_autos',json = datos)
        print("Actualizar Datos: ",r1.text)

        return respuesta
        
    def depurarDatos(self):
        r1 = requests.get('http://127.0.0.1:9566/depurarDatos')
        print("Depurar Datos: ",r1.text)
        return("Depurar Datos: "+r1.text)

    def sensorTemperatura(self):
        return randint(0, 70)

    def enviarDatos(self,numSemaforo):                       
        cantidadAutos = 0
        for aux in self.listaSemaforos:
            if aux.getId()==numSemaforo:
                cantidadAutos = aux.getCantidadAutosEnEspera()

        datos = {"numSemaforo": numSemaforo, "cantidadAutos": cantidadAutos} 
        r1 = requests.post('http://127.0.0.1:9566/datos', json = datos)
        print("Enviar Datos: ",r1.text)

    #Metodo para monitorear el estado de los semaforos
    def monitorear(self):
        respuesta = ''
        
        for a in self.listaSemaforos:
            if(a.getEstado() == Constantes.ESTADO_SEMAFORO_VERDE):
                respuesta += "Estado Semaforo " + a.getId() +": Verde \n"
            elif(a.getEstado() == Constantes.ESTADO_SEMAFORO_ROJO):
                respuesta += "Estado Semaforo " + a.getId() + ": Rojo   \n"
            elif(a.getEstado() == Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE or a.getEstado() == Constantes.ESTADO_SEMAFORO_AMARILLO):
                respuesta += "Estado Semaforo " + a.getId() + ": Amarillo   \n"
            else:
                respuesta += "Error en el estado del semaforo " + a.getId() + "\n"

            respuesta += "Cantidad Autos: " + str(a.getCantidadAutosEnEspera())+ "\n"
            if(a.getTipoTrafico() == Constantes.TRAFICO_NULO):
                respuesta += "Tipo de trafico: Nulo \n"
            elif(a.getTipoTrafico() == Constantes.TRAFICO_POCO):
                respuesta += "Tipo de trafico: Poco \n"
            elif(a.getTipoTrafico() == Constantes.TRAFICO_NORMAL):
                respuesta += "Tipo de trafico: Normal \n"
            elif(a.getTipoTrafico() == Constantes.TRAFICO_MUCHO):
                respuesta += "Tipo de trafico: Mucho \n"
            elif(a.getTipoTrafico() == Constantes.TRAFICO_CONGESTIONAMIENTO):
                respuesta += "Tipo de trafico: Congestionamiento \n"
            #En caso de que el semaforo se encuentre en intermitente
            if(a.getSegundosParaCambiarEstado() == -1):
                respuesta += "Semaforo " + a.getId() + " en Intermitente \n"
            else:
                respuesta += "Semaforo " + a.getId() + " Tiempo para cambiar estado: " + str(a.getSegundosParaCambiarEstado()) + "\n"
            respuesta += '---------------------------------------- \n'
        
        return respuesta
    
    def procesarCambioEstadoSemaforo(self,estado,a):
        respuesta=""
        if(estado == Constantes.ESTADO_SEMAFORO_VERDE):
            respuesta += 'Se ha cambiado el estado del semaforo ' + a.getId() + ' a verde. \n'
            self.enviarDatos(a.getId())
        elif(estado == Constantes.ESTADO_SEMAFORO_ROJO):
            respuesta += 'Se ha cambiado el estado del semaforo ' + a.getId() + ' a rojo.  \n'
            self.enviarDatos(a.getId())
        else:
            respuesta += 'Se ha cambiado el estado del semaforo ' + a.getId() + ' a amarillo.  \n'         
        return respuesta

    def calcularTiempoSemaforos(self):
        respuesta = ""
        for a in self.listaSemaforos:
            porcentajeCantidadAutomoviles = a.getCantidadAutosEnEspera()/a.getCapacidadMaxima()    
            
            valorRojo = 0
            valorVerde = 0
            valorAmarrilo = 0
            valorTipoTrafico = None

            if(porcentajeCantidadAutomoviles == Constantes.TRAFICO_CONGESTIONAMIENTO):
                valorRojo = 5
                valorVerde = 8
                valorAmarrilo = 1
                valorTipoTrafico =  Constantes.TRAFICO_CONGESTIONAMIENTO
            elif(porcentajeCantidadAutomoviles >= Constantes.TRAFICO_MUCHO[0] and porcentajeCantidadAutomoviles < Constantes.TRAFICO_MUCHO[1]):
                valorRojo = 3
                valorVerde = 5
                valorAmarrilo = 1
                valorTipoTrafico =  Constantes.TRAFICO_MUCHO
            elif(porcentajeCantidadAutomoviles >= Constantes.TRAFICO_NORMAL[0] and porcentajeCantidadAutomoviles < Constantes.TRAFICO_NORMAL[1]):
                valorRojo = 3
                valorVerde = 3
                valorAmarrilo = 1
                valorTipoTrafico =  Constantes.TRAFICO_NORMAL
            elif(porcentajeCantidadAutomoviles > Constantes.TRAFICO_POCO[0] and porcentajeCantidadAutomoviles < Constantes.TRAFICO_POCO[1]):
                valorRojo = 1
                valorVerde = 1
                valorAmarrilo = 1
                valorTipoTrafico =  Constantes.TRAFICO_POCO
            elif(porcentajeCantidadAutomoviles == Constantes.TRAFICO_NULO):
                valorAmarrilo = -1
                valorTipoTrafico =  Constantes.TRAFICO_NULO

            #En caso de que sea un tipo de trafico diferente (nulo,poco,....)
            if(a.getTipoTrafico() != valorTipoTrafico):
                if(a.getEstado() == Constantes.ESTADO_SEMAFORO_ROJO):      
                    if(valorTipoTrafico == Constantes.TRAFICO_NULO):
                        a.setSegundosParaCambiarEstado(-1)
                        a.setEstado(Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE)
                    #Si el nuevo tiempo cambia a un valor negativo debe cambiar al siguiente estado
                    elif(valorRojo - a.getTiempoEspera() <= 0):
                        respuesta += self.procesarCambioEstadoSemaforo(a.cambiarEstado(),a)
                        a.setTiempoEspera(0)                    
                    a.setSegundosParaCambiarEstado(valorRojo - a.getTiempoEspera())
                elif(a.getEstado() == Constantes.ESTADO_SEMAFORO_VERDE):          
                    if(valorTipoTrafico == Constantes.TRAFICO_NULO):
                        a.setSegundosParaCambiarEstado(-1)
                        a.setEstado(Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE)
                    #Si el nuevo tiempo cambia a un valor negativo debe cambiar al siguiente estado
                    elif(valorVerde - a.getTiempoEspera() <= 0):
                        respuesta += self.procesarCambioEstadoSemaforo(a.cambiarEstado(),a)
                        a.setTiempoEspera(0)     
                    a.setSegundosParaCambiarEstado(valorVerde - a.getTiempoEspera())
                elif(a.getEstado() == Constantes.ESTADO_SEMAFORO_AMARILLO):
                    #En caso de que el semaforo se encuentre en otro tipo de trafico distinto
                    #al nulo y se deba cambiar a intermitente.
                    if(valorTipoTrafico == Constantes.TRAFICO_NULO):                        
                        a.setSegundosParaCambiarEstado(-1)
                        a.setEstado(Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE)
                    #en caso de que se encuentre en amarillo pero no en intermitente (trafico nulo)
                    else:
                        #Si el nuevo tiempo cambia a un valor negativo debe cambiar al siguiente estado                        
                        if(valorAmarrilo - a.getTiempoEspera() <= 0):
                            respuesta += self.procesarCambioEstadoSemaforo(a.cambiarEstado(),a)
                            a.setTiempoEspera(0)                        
                        a.setSegundosParaCambiarEstado(valorAmarrilo - a.getTiempoEspera())
                elif(a.getEstado() == Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE):
                        respuesta += self.procesarCambioEstadoSemaforo(a.cambiarEstado(),a) 
                        a.setTiempoEspera(0)    
                        a.setSegundosParaCambiarEstado(valorVerde - a.getTiempoEspera())
                a.setTipoTrafico(valorTipoTrafico) 

        return respuesta
        
    #Metodo para mover un turno.    
    def moverUnTurno(self):
        respuesta = ''       
        
        for a in self.listaSemaforos:   
            calcularTiempoSemaforos = False               
            #Si ya debe cambiar el estado del semaforo
            if(a.getSegundosParaCambiarEstado() == 0):                 
                estado = a.cambiarEstado()
                calcularTiempoSemaforos = True
                if(estado == Constantes.ESTADO_SEMAFORO_VERDE):
                    respuesta += 'Se ha cambiado el estado del semaforo ' + a.getId() + ' a verde. \n'
                    self.enviarDatos(a.getId())
                elif(estado == Constantes.ESTADO_SEMAFORO_ROJO):
                    respuesta += 'Se ha cambiado el estado del semaforo ' + a.getId() + ' a rojo.  \n'
                    self.enviarDatos(a.getId())
                else:
                    respuesta += 'Se ha cambiado el estado del semaforo ' + a.getId() + ' a amarillo.  \n'               
            aux=""      

            

            (aux,calcularTiempoSemaforos) = self.moverAuto(a,calcularTiempoSemaforos)
            respuesta += aux
            if(a.getEstado() != Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE):
                a.reducirSegundosParaCambiarEstado()
                a.aumentarTiempoEspera()
        
            if(calcularTiempoSemaforos):
                respuesta += self.calcularTiempoSemaforos()
        respuesta += 'Se ha movido con exito un segundo.  \n'

        return respuesta



    #Metodo interno para mover un auto.
    #Parametros
    #a - auto a mover.
    #respuesta - respuesta que se ira agregando para regresar.
    #calcularTiempoSemaforos - en caso de que se tenga que calcular el tiempo de los semaforos.
    def moverAuto(self,a,calcularTiempoSemaforos):
        respuesta = ""
        if(a.getEstado() == Constantes.ESTADO_SEMAFORO_VERDE):            
            #En caso de congestion
            if(a.getSiguienteSemaforo().getCantidadAutosEnEspera() == a.getSiguienteSemaforo().getCapacidadMaxima()):
                respuesta += Constantes.MENSAJE_CONGESTION + ' en el semaforo '+ a.getId()  + ' \n'                
                return respuesta
            #Cuando el semaforo tenga automoviles en espera, se mueve un auto.
            elif(a.getCantidadAutosEnEspera() !=0):            
                autoAux = a.quitarAutoEnEspera() 
                
                #Se espera la señal del sensor de movimiento.
                #Revisa que el elemento de señal de movimiento este vacio.
                constantes = Constantes()
                myclient = pymongo.MongoClient("mongodb://localhost:27017/")
                mydb = myclient["Datos"]
                datosPendientes = mydb["Datos_Pendientes"]

                #Busca el elemento que representa el ultimo mensaje recibido.
                arrayDatosPendientes = datosPendientes.find()
                                
                myquery = { "tipo": constantes.SIGNAL_MOVIMIENTO }
                newvalues = { "$set": { "mensaje": "" } }

                datosPendientes.update_one(myquery, newvalues)

                r3 = requests.get('http://127.0.0.1:9566/esperarSeñalMovimiento')
                print("prueba")
                cantidadAutosSemaforo1 = self.listaSemaforos[int(1)-1].getCantidadAutosEnEspera()
                cantidadAutosSemaforo2 = self.listaSemaforos[int(2)-1].getCantidadAutosEnEspera()
                cantidadAutosSemaforo3 = self.listaSemaforos[int(3)-1].getCantidadAutosEnEspera()
                cantidadAutosSemaforo4 = self.listaSemaforos[int(4)-1].getCantidadAutosEnEspera()
                cantidadAutosSemaforo5 = self.listaSemaforos[int(5)-1].getCantidadAutosEnEspera()

                #Mandar peticion para que sea actualice la pagina.
                datos = {"cantidadAutosSemaforo1":cantidadAutosSemaforo1,"cantidadAutosSemaforo2":cantidadAutosSemaforo2,"cantidadAutosSemaforo3":cantidadAutosSemaforo3,"cantidadAutosSemaforo4":cantidadAutosSemaforo4,"cantidadAutosSemaforo5":cantidadAutosSemaforo5} 
                r1 = requests.post('http://127.0.0.1:9566/actualizarPagina_autos',json = datos)
                print("Actualizar Datos: ",r1.text)

                #Revisar que no se excedan los coches.
                r1 = requests.get('http://127.0.0.1:9566/obtenerDatosNotificaciones').json()   
                limite = r1["limiteMinCapacidad"]
                if((100-(cantidadAutosSemaforo1/self.listaSemaforos[int(1)-1].getCapacidadMaxima()))*100 < limite or (100-(cantidadAutosSemaforo2/self.listaSemaforos[int(2)-1].getCapacidadMaxima()))*100 < limite or (100-(cantidadAutosSemaforo3/self.listaSemaforos[int(3)-1].getCapacidadMaxima()))*100 < limite or (100-(cantidadAutosSemaforo4/self.listaSemaforos[int(4)-1].getCapacidadMaxima()))*100 < limite or (100-(cantidadAutosSemaforo5/self.listaSemaforos[int(5)-1].getCapacidadMaxima()))*100 < limite):
                    self.notificar("Mensaje de Prueba","Se ha excedido el limite minimo de autos por semaforo")

                #En caso de llegar a su destino.
                if(autoAux.getDestino() == a.getSiguienteSemaforo().getId()):
                    respuesta += 'El auto con inicio en el semaforo ' + str(autoAux.getInicio()) + ' ha llegado al semaforo '+autoAux.getDestino()+'.  \n'
                else:
                    a.getSiguienteSemaforo().agregarAutoEnEspera(autoAux)     
                    respuesta += 'El auto con inicio en el semaforo ' + str(autoAux.getInicio()) + ' ha llegado al semaforo '+a.getSiguienteSemaforo().getId()+'.  \n'                               
                
                calcularTiempoSemaforos=True

        return (respuesta,calcularTiempoSemaforos)
    
    def notificarCorreo(self):
        port = 465  # For SSL

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(Constantes.SENDER_EMAIL, Constantes.contraEmail)
            server.sendmail(Constantes.SENDER_EMAIL, Constantes.RECEIVER_EMAIL, Constantes.MESSAGE)

        return "Se ha enviado el correo con exito"

    def cambiarCorreoDestinatario(self,correo):
        datos = {"correo":correo}
        r1 = requests.post('http://127.0.0.1:9566/cambiarCorreoDestinatario', json = datos)
        return "Se ha cambiado con exito el correo del destinatario."

    def cambiarLimiteMinimaCapacidad(self,limiteMin):
        datos = {"limiteMin":limiteMin}
        r1 = requests.post('http://127.0.0.1:9566/cambiarLimiteMinimaCapacidad', json = datos)
        return "Se ha cambiado con exito el Limite Minima Capacidad."


    def cambiarLimiteTemperatura(self,min,max):
        datos = {"min":min,"max":max}
        r1 = requests.post('http://127.0.0.1:9566/cambiarLimiteTemperatura', json = datos)
        return "Se ha cambiado con exito el Limite de temperatura."

    def cambiarCorreoRemitente(self,correo):
        datos = {"correo":correo}
        r1 = requests.post('http://127.0.0.1:9566/cambiarCorreoRemitente', json = datos)
        return "Se ha cambiado con exito el correo del remitente."

    def cambiarContraseña(self,password):
        datos = {"password":password}
        r1 = requests.post('http://127.0.0.1:9566/cambiarContraseña', json = datos)
        return "Se ha cambiado con exito la contraseña."

    
    def cambiarMedioNotificacion(self,medioNotificacion):
        datos = {"medioNotificacion":medioNotificacion}
        r1 = requests.post('http://127.0.0.1:9566/cambiarMedioNotificacion', json = datos)
        return "Se ha cambiado con exito el medio de comunicacion."

    def analisisInferencia(self):
        r1 = requests.get('http://127.0.0.1:9566/analisisInferencia') 
        aux_json = json.loads(r1.text)
        respuesta = ""

        temperatura_Array = []
        cantidad_Autos_Array = []
        
        for aux in aux_json:
            elemento = aux_json[aux]
            temperatura = elemento["temperatura"]
            cantidad_Autos = elemento["cantidadAutos"]
            temperatura_Array.append(int(temperatura))
            cantidad_Autos_Array.append(int(cantidad_Autos))


        temperatura_Array = np.array(temperatura_Array)
        cantidad_Autos_Array = np.array(cantidad_Autos_Array)


        model = LinearRegression().fit(cantidad_Autos_Array.reshape((-1, 1)),temperatura_Array)
        r_sq = model.score(cantidad_Autos_Array.reshape((-1, 1)),temperatura_Array)
        print('coefficient of determination:', r_sq)
        respuesta += 'coefficient of determination:'+ str(r_sq)+"\n"

        print('intercept:', model.intercept_)
        respuesta += 'intercept:'+ str( model.intercept_)+"\n"
        print('slope:', model.coef_)
        respuesta += 'slope:'+str( model.coef_)+'\n'+'\n'
        print('\n')
        temperatura_Array = np.array(temperatura_Array).reshape((-1, 1))
        
        
        plt.plot(cantidad_Autos_Array, model.coef_*cantidad_Autos_Array + model.intercept_)

        plt.scatter(cantidad_Autos_Array.reshape((-1, 1)),temperatura_Array) 
        plt.title('Linear Reggression')
        plt.xlabel("Cantidad Autos")
        plt.ylabel("Temperature")
        plt.show()

        #Predicción
        t_pred = model.predict(temperatura_Array.reshape((-1, 1)))
        #for i in range(0,20):
            #if(i<t_pred.size):
                #print('Temperatura predecida',i+1,': ',t_pred[i])
                #respuesta += 'Temperatura predecida'+str(i+1)+': '+str(t_pred[i])+"\n"
        return respuesta


    def notificar(self,titulo,contenido):

        r1 = requests.get('http://127.0.0.1:9566/obtenerDatosNotificaciones').json()   
        print(r1)
        if(r1["modo"] == Constantes.MODO_CORREO):
            mail_content = contenido
            
            #The mail addresses and password
            r1
            #sender_address = "proyecto.iot.itson@gmail.com"
            sender_address = r1["correoRemitente"]
            #sender_pass = "estaes1contrasena"
            sender_pass = r1["password"]
            #receiver_address = 'jesusgnzlez16@gmail.com'
            receiver_address = r1["correoDestinatario"]
            #Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = titulo   #The subject line
            #The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, sender_pass) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print('Mail Enviado')
            return "Se ha enviado el correo electronico"
        elif(r1["modo"] == Constantes.MODO_TELEGRAM):
            message=contenido

            #Telegram code
            base_url='https://api.telegram.org/bot1977688109:AAHoiJ3793UPn3DRdy_vXEu05DaqZG7eTKQ/sendMessage?chat_id=-537494671&text="{}"'.format(message)
            requests.get(base_url)
            print('Telegram Sent')
            return "Se ha enviado el mensaje a Telegram"
            #######################
        elif(r1["modo"] == Constantes.MODO_SLACK):          
            message=contenido
            #SLACK code
            payload='{"text":"%s"}' % message
            response = requests.post('https://hooks.slack.com/services/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', 
            data=payload)

            print (response.text)
            print("slack sent")
            return "Se ha enviado el mensaje a slack"