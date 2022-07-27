class Datos:
    def __init__(self, id, idSemaforo,cantidad,temperatura):
        self.id = id
        self.idSemaforo = idSemaforo
        self.cantidad = cantidad
        self.temperatura = temperatura

    def getIdSemaforo(self):
        return self.idSemaforo
    
    def getCantidad(self):
        return self.cantidad

    def getTemperatura(self):
        return self.temperatura