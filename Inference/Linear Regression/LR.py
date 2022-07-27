#Se adjunta un archivo tipo csv que contiene datos del clima en Szeged, Hungría, entre el 2006-2016. 
# Responder las siguientes preguntas con base en un programa que calcule regresión lineal:
#- ¿Existe una relación entre la humedad y la temperatura?
#- ¿Qué pasa entre la humedad y la temperatura aparente?
#- ¿Se puedes predecir la temperatura aparente dada la humedad? Si es así predecir 20 lecturas de temperatura.
import pymongo
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["clima"]
coll = db["Clima"]  

t = []
t_a = []
h = []

for i in coll.find({"$and":
    [{ "hour" : { "$gt":7, "$lt":14}},
    { "day": { "$gt":0, "$lt":21}},
    { "year" : { "$eq": 2015}},
    { "month" : { "$eq": 12}}
    ]}):
    t.append(i['Temperature'])
    t_a.append(i['ApparentTemperature'])
    h.append(i['Humidity'])

t = np.array(t)
t_a = np.array(t) 
h = 100*(np.array(h))

while True:
    print('''
    1) Relación entre humedad y temperatura
    2) Relación entre humedad y temperatura aparente
    3) Salir
    ''') 
    
    a = input("\nSeleccione una opción: ")

    if a == '1':
        model = LinearRegression().fit(h.reshape((-1, 1)),t)
        r_sq = model.score(h.reshape((-1, 1)),t)
        print('coefficient of determination:', r_sq)
        print('intercept:', model.intercept_)
        print('slope:', model.coef_)
        print('\n')
        t = np.array(t).reshape((-1, 1))
        
        plt.plot(h, model.coef_*h + model.intercept_)

        plt.scatter(h.reshape((-1, 1)),t) 
        plt.title('Linear Reggression')
        plt.xlabel("Humidity")
        plt.ylabel("Temperature")
        plt.show()

        #Predicción
        t_pred = model.predict(t.reshape((-1, 1)))
        for i in range(0,20):
            print('Temperatura predecida',i+1,': ',t_pred[i])

    elif a == "2":
        model = LinearRegression().fit(h.reshape((-1, 1)),t_a)
        r_sq = model.score(h.reshape((-1, 1)),t_a)
        print('coefficient of determination:', r_sq)
        print('intercept:', model.intercept_)
        print('slope:', model.coef_)
        print('\n')
        plt.plot(h, model.coef_*h + model.intercept_)
        plt.scatter(h.reshape((-1, 1)),t_a)
        plt.title('Linear Reggression')
        plt.xlabel("Humidity")
        plt.ylabel("Apparent Temperature")
        plt.show()
        ta_pred = model.predict(t_a.reshape((-1, 1)))
        for i in range(0,20):
            print('Temperatura aparente predecida', i+1, ': ', ta_pred[i])

    else:
        break