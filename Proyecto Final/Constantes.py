class Constantes():
    #Limites
    #Limite de temperaturas
    TEMPERATURA = [-10, 70]
    #Limite de trafico
    #Nota: No puede ser en flotante.
    TRAFICO = [0, 100]
    SEMAFOROS = [1, 5]


    #Tipos de trafico
    TRAFICO_NULO = 0
    TRAFICO_POCO = [0 , .3333]
    TRAFICO_NORMAL = [.3333,.6666]
    TRAFICO_MUCHO = [.6666 , 1.00]
    TRAFICO_CONGESTIONAMIENTO = 1.00
    TRAFICO_CAMBIO_ESTADO = 999

    #Estados posibles en un semaforo
    ESTADO_SEMAFORO_ROJO    = 0
    ESTADO_SEMAFORO_AMARILLO = 1
    #ESTADO_SEMAFORO_AMARILLO_A_ROJO   = 1
    #ESTADO_SEMAFORO_AMARILLO_A_VERDE = 2
    ESTADO_SEMAFORO_AMARILLO_INTERMITENTE = 2
    ESTADO_SEMAFORO_VERDE   = 3

    #Mensaje de congestion.
    MENSAJE_CONGESTION = 'Ha ocurrido una congestion'

    
    contraEmail= "SistemasITSON99"

    SENDER_EMAIL = "sistemasitson@gmail.com"
    RECEIVER_EMAIL = "carlosramongalindolopez@gmail.com"

    MESSAGE = """\
Subject: Hi there

This message is sent from Python."""

    SIGNAL_TEMPERATURA = "SIGNAL_TEMPERATURA"
    SIGNAL_MOVIMIENTO = "SIGNAL_MOVIMIENTO"

    NOTIFICACION_AUTOS = "NOTIFICACION_AUTOS"
    NOTIFICACION_TEMPERATURA = "NOTIFICACION_TEMPERATURA"
    NOTIFICACION = "NOTIFICACION"

    NOTIFICACION_ACTUALIZAR_SI = "SI"
    NOTIFICACION_ACTUALIZAR_NO = "NO"

    MODO_CORREO = "MODO_CORREO"
    MODO_SLACK = "MODO_SLACK"
    MODO_TELEGRAM = "MODO_TELEGRAM"
