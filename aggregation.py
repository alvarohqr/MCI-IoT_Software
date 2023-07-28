#Alvaro Humberto Quiñonez Rodriguez 
#Ejercicio de consultas de agregación

from pymongo import MongoClient
import pprint #pretty print
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["mci"]
Collection = db["students"]

# Descomentar las siguientes lineas antes de ejecutar el programa
# y volver a comentarlas para evitar id duplicados 
#students=[]
#for line in open('students.json','r'):
#    students.append(json.loads(line))
#Collection.insert_many(students)

while(True):
	print(""" Qué desea conocer?
    1)Calificación promedio de cada alumno (examen, quiz y tareas).
    2)Calificación promedio para cada alumno, sólo de exámenes y tareas.
    3)Calificación promedio de todo el grupo sólo de exámenes
    4)Salir""")

	a=input("\nIngrese su opción: ")

	if a == "1":
		pipeline = [
			{"$unwind":  "$scores"},
			{"$group":
				{
					"_id": "$_id",
					"avgscore": { "$avg": "$scores.score" }
				}
			},
			{
				"$sort":{"_id": 1}
			}
			]
		pprint.pprint(list(db.students.aggregate(pipeline)))
		print("\n")	
		
	elif a == "2":
		pipeline = [

			{"$unwind": "$scores"},
			{
				"$group": {"_id": "$_id",
				"avgscore": {
					"$avg": {
					"$cond": [
						{"$or": [{"$eq": ["$scores.type", "exam"]}, {"$eq": [ "$scores.type","homework"]}]},
						{"$multiply": ["$scores.score",{"$divide": [3,2 ]}] # se multiplica por 3/2 ya que se toman
						#las 3 calificacioes
						}, 0 #si no se cumple avgscore toma el valor de 0
					]
					}
				}
				}
			},

			{"$sort":{"_id": 1}}
			]
		pprint.pprint(list(db.students.aggregate(pipeline)))	
		print("\n")	

	elif a == "3":
		pipeline = [
			{"$unwind": "$scores"},	
			{"$group": {"_id": "null",
				"avgscore": {
					"$avg": {
						"$cond": [
						{"$eq": [ "$scores.type","exam"]},
						{"$multiply": [
							"$scores.score",{"$divide":[600,200]}
					]
						},0 #si no se cumple avgscore toma el valor de 0
					]
					}
				}
				}
			} 
		]
		pprint.pprint(list(db.students.aggregate(pipeline)))
		print("\n")	
	
	else:		
		break
