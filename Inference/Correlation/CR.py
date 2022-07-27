# Se adjunta un archivo tipo csv que contiene datos del clima en Szeged, Hungría, entre el 2006-2016.
# Responder las siguientes preguntas con base en un programa que calcule regresión lineal:
# - ¿Existe una relación entre la humedad y la temperatura?
# - ¿Qué pasa entre la humedad y la temperatura aparente?
# - ¿Se puedes predecir la temperatura aparente dada la humedad? Si es así predecir 20 lecturas de temperatura.
import pymongo
import numpy as np
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["clima"]
coll = db["Clima"]

t = []
h = []

for i in coll.find({"$and":
                    [{"hour": {"$gt": 5, "$lt": 11}},
                     {"day": {"$gt": 0, "$lt": 21}},
                        {"year": {"$eq": 2012}},
                        {"month": {"$eq": 6}}
                     ]}):
    t.append(i['Temperature'])
    h.append(i['Humidity'])

t1 = np.array(t)
t_a1 = np.array(t)
h1 = 100*(np.array(h))

corr1 = np.corrcoef(h1, t1)
#print("Correlación de Pearson entre humedad y temperatura: %.3f\n" %corr1[0][1])

for j in coll.find({"$and":
                    [{"hour": {"$gt": 18, "$lt": 23}},
                     {"day": {"$gt": 0, "$lt": 21}},
                        {"year": {"$eq": 2012}},
                        {"month": {"$eq": 6}}
                     ]}):
    t.append(j['Temperature'])
    h.append(j['Humidity'])

t2 = np.array(t)
t_a2 = np.array(t)
h2 = 100*(np.array(h))
corr2 = np.corrcoef(h2, t2)
if max(corr1[0][1], corr2[0][1]) == corr1[0][1]:
    print("\nCorrelación de Pearson entre humedad y temperatura (5-11 a.m): %.3f\n" %
          corr1[0][1])
    t = t1
    h = h1
else:
    print("\nCorrelación de Pearson entre humedad y temperatura (6-11 p.m): %.3f\n" %
          corr2[0][1])
    t = t2
    h = h2

    model = LinearRegression().fit(h.reshape((-1, 1)), t)
    r_sq = model.score(h.reshape((-1, 1)), t)
    print('coefficient of determination:', r_sq)
    print('intercept:', model.intercept_)
    print('slope:', model.coef_)
    print('\n')
    t = np.array(t).reshape((-1, 1))

    plt.plot(h, model.coef_*h + model.intercept_)

    plt.scatter(h.reshape((-1, 1)), t)
    plt.title('Linear Reggression')
    plt.xlabel("Humidity")
    plt.ylabel("Temperature")
    plt.show()

    # Predicción
    t_pred = model.predict(t.reshape((-1, 1)))
    for i in range(0, 20):
        print('Temperatura predecida', i+1, ': ', t_pred[i])
