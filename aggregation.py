#Obtener y restaurar en MongoDB el archivo students.json (adjunto) y realizar los pipelines necesarios para obtener la siguiente información:
    #Calificación promedio de cada alumno.
    #Calificación promedio para cada alumno, sólo de exámenes y tareas.
    #Calificación promedio de todo el grupo sólo de exámenes

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/") #Servidor local
db = client["biblio"]           # Base de datos
coll1 = db["suspenso"]          # Colección "suspenso"
coll2 = db["informatica"]       # Colección "informatica"
x= db.list_collection_names()   # Array de colecciones  

while (True):
    print(""" Qué desea hacer?
    1)Agregar elementos
    2)Eliminar elementos
    3)Ver el listado de las colecciones
    4)Salir""")

    a=input("\nIngrese su opción: ")

    if a == "1":
        coll = input("""
        Ingrese 1 para agregar a la colección """+ x[0] +"""
        Ingrese 2 para agregar a la colección """+ x[1] +""" \n
        """)
        
        nombre = input("Nombre del libro: ")
        autor = input("Autor: ")
        año = input("Año de publicación: ")
        
        if coll == "1":
            #Informatica
            coll2.insert_one({"nombre": nombre, "autor": autor, "año": año})
            print('\nDocumento añadido!\n')           
        elif coll == "2":
            #Suspenso
            coll1.insert_one({"nombre": nombre, "autor": autor, "año": año})
            print('\nDocumento añadido!\n')        
        else:
            print("Opción incorrecta!\n")

    elif a == "2":
        coll = input("""
        Ingrese 1 para eliminar de la colección """+ x[0] +"""
        Ingrese 2 para eliminar de la colección """+ x[1] +""" \n
        """)
        
        nombre = input("Nombre del libro: ")
        
        if coll == "1":
            #Informatica
            coll2.delete_one({"nombre": nombre})
            print('\nDocumento eliminado!\n')           
        elif coll == "2":
            #Suspenso
            coll1.delete_one({"nombre": nombre})
            print('\nDocumento eliminado!\n')      
        else:
            print("Opción incorrecta!\n")

    elif a == "3":
        coll = input("""
        Ingrese 1 para visualizar la colección """+ x[0] +"""
        Ingrese 2 para visualizar la colección """+ x[1] +""" \n
        """)
        if coll == "1":
            print("\nElementos colección informatica: \n")
            for colls in coll2.find():
                print(colls)         
        elif coll == "2":
            print("\nElementos colección suspenso:  \n")
            for colls in coll1.find():
                print(colls)
            print("\n")
        else:
            print("Opción incorrecta!\n")
            
    else:
        break
