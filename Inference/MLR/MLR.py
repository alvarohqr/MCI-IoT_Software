# Sobre los datos de estadísticas de juegos de basketball adjuntos, encontrar los coeficientes que 
# representan la relación entre la altura y el porcentaje de encestes, de efectividad de tiros libres y
# de puntos por juego, así como, los coeficientes de la relación entre porcentaje de encestes y 
# el porcentaje de efectividad de tiros libres y de puntos por juego.


#X1 = Altura en pies, X2 = Peso en libras,  X3 = Porcentaje de efectividad de encestes
#X4 = Porcentaje de efectividad de tiros libres,  X5 = Promedio de puntos por juego

import pymongo
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv("mlr09.csv")
# #Relación de X1 con X3, X4 y X5
# #Relación de X3 con X4 y X5

x = dataset[['X3', 'X4', 'X5']]
y = dataset['X1']

mlr = LinearRegression()  
mlr.fit(x, y)
print("Intercept: ", mlr.intercept_)
print("Coeficiente de X1 con X3, X4 y X5: ",  mlr.coef_) 

x = dataset[['X4', 'X5']]
y = dataset['X3']
mlr = LinearRegression()  
mlr.fit(x, y)
print("Intercept: ", mlr.intercept_)
print("Coeficiente de X3 con X4 y X5: ",  mlr.coef_) 
