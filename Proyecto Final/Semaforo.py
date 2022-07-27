from Constantes import Constantes
from Cola import Cola
from Automovil import Automovil

class Semaforo():
    
    #Constructor de la clase semaforo.
    def __init__(self,id):
        self.id = id
        self.estado = Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE
        self.tipoTrafico = Constantes.TRAFICO_NULO
        self.autosEnEspera = Cola()
        self.capacidadMaxima = 0
        self.segundosParaCambiarEstado = -1
        self.tiempoEspera = 0
        self.siguienteSemaforo = None
    
    #Metodo para obtener el id
    def getId(self):
        return self.id
    
    def getTipoTrafico(self):
        return self.tipoTrafico 

    def setTipoTrafico(self,tipoTrafico):
        self.tipoTrafico = tipoTrafico 

    #Metodo para obtener el estado
    def getEstado(self):
        return self.estado
    
    def getTiempoEspera(self):
        return self.tiempoEspera

    def setTiempoEspera(self,tiempo):
        self.tiempoEspera = tiempo

    #Metodo para obtener los segundos que faltan para cambiar el estado
    def getSegundosParaCambiarEstado(self):
        return self.segundosParaCambiarEstado
    
    #Metodo para definir los segundos que faltan para cambiar el estado
    def setSegundosParaCambiarEstado(self,segundos):
        self.segundosParaCambiarEstado = segundos
    
    #Metodo para definir el siguiente semaforo
    def setSiguienteSemaforo(self,siguienteSemaforo):
        self.siguienteSemaforo = siguienteSemaforo
    
    #Metodo para obtener el siguiente semaforo
    def getSiguienteSemaforo(self):
        return self.siguienteSemaforo
       

    #Metodo para cambiar la capacidad maxima del semaforo
    def setCapacidadMaxima(self,maxima):
        self.capacidadMaxima = maxima
    
    #Metodo para obtener la capacidad maxima
    def getCapacidadMaxima(self):
        return self.capacidadMaxima
    
    #Metodo para obtener la cantidad de autos en espera    
    def getCantidadAutosEnEspera(self):
        return self.autosEnEspera.getTamaño()
    
    #Metodo para reducir el contador de espera un segundo.
    def reducirSegundosParaCambiarEstado(self):
        self.segundosParaCambiarEstado -= 1
        
    #Metodo para aumentar el tiempo de espera.
    def aumentarTiempoEspera(self):
        self.tiempoEspera += 1

    #Metodo para agregar auto en el semaforo
    def agregarAutoEnEspera(self,auto):
        self.autosEnEspera.encolar(auto)
    
    #Metodo para quitar auto en espera.    
    def quitarAutoEnEspera(self):
        return self.autosEnEspera.desencolar()

    

    #Metodo para cambiar estado del semaforo.
    def cambiarEstado(self):
        if(self.estado == Constantes.ESTADO_SEMAFORO_ROJO):
            self.estado = Constantes.ESTADO_SEMAFORO_VERDE
            return Constantes.ESTADO_SEMAFORO_VERDE
        elif(self.estado == Constantes.ESTADO_SEMAFORO_VERDE):
            self.estado = Constantes.ESTADO_SEMAFORO_AMARILLO
            return Constantes.ESTADO_SEMAFORO_AMARILLO
        elif(self.estado == Constantes.ESTADO_SEMAFORO_AMARILLO):
            self.estado = Constantes.ESTADO_SEMAFORO_ROJO
            return Constantes.ESTADO_SEMAFORO_ROJO
        elif(self.estado == Constantes.ESTADO_SEMAFORO_AMARILLO_INTERMITENTE):
            self.estado = Constantes.ESTADO_SEMAFORO_VERDE
            return Constantes.ESTADO_SEMAFORO_VERDE

    def setEstado(self,estado):
        self.estado = estado

    def cambiarEstadoSemaforo(self,estado):
        if(estado == Constantes.ESTADO_SEMAFORO_VERDE):
            self.setEstado(Constantes.ESTADO_SEMAFORO_VERDE)
        elif(estado == Constantes.ESTADO_SEMAFORO_ROJO):
            self.setEstado(Constantes.ESTADO_SEMAFORO_ROJO)
        elif(estado == Constantes.ESTADO_SEMAFORO_AMARILLO):
            self.setEstado(Constantes.ESTADO_SEMAFORO_AMARILLO)



        