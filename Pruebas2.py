import os
import time
import json
import threading
import time
import json
import time
import re
import os
import emoji  #se instala la libreria
import unidecode #se instala la libreria
import tweepy
import aceso


numTendencia = [0,1,2,3,4,5,7,8,9]
passwor="pTxq2nEit9Ce2nVBmumD9FQfsw6ytcYcWHCVwoJsKoZueQcOqhKYrWm5yCbjwPHwFiSmCA5eqcQZYYEoOKbtAQ=="


username="/dbs/tendencias/colls/tendencia"+str(numTendencia[2])+""
username2="/dbs/tendencias/colls/tendencia0"
password=passwor
# print (username)
# print (username2)
# print (passwor)
# print (password)

numTendencia = [0,1,2,3,4,5,7,8,9]
    
def ObtenerTodosLosNombres():
    try:
            ruta='DataLimpiezaTexto'
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+e)
        
def ObtenerYaHechos():
    try:
            ruta='C:\Python\PT2Final\DataBase'
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+e)
        
def PrimeraLectura(archivo):
    rutautil="C:\Python\PT2Final\DataBase"
    NomArchivo=rutautil+'\\'+archivo
    global data
    try:
        with open(NomArchivo, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("No se encontro archivo JSON " + e)     
    finally:
        return data
        
def TopTemas ():
    Tendencia = ObtenerTodosLosNombres()
    Tende =[]
    Final = []
    for tema in Tendencia:
        contador = 0
        datas = PrimeraLectura(tema)
        for tuit in datas['tuits']:
            contador+=1
        print ("El archivo es: "+ tema + "Tiene " +str(contador)+ " tuits")
        Tende.append((tema,contador))
            
    pels_sorted = sorted(Tende, reverse=True, key=lambda tupla: tupla[1])
    top_10 = pels_sorted[:10]
    for n in top_10:
        Final.append(n[0])

    return Final

#archivos = TopTemas()
#print (archivos)



def hola_mundo (nombre):
    time.sleep(5)
    print ("Hola Mundo 1 "+ nombre)

 
def hola_mundo2 (nombre):
    time.sleep(8)
    print ("Hola Mundo 2 "+ nombre)
    

def hola_mundo3 (nombre):
    time.sleep(1)
    print ("Hola Mundo 3 "+ nombre)
    
    
def quitar (uno, dos):
    final = uno
    for n in final:
        if (n in dos):
            uno.remove(n)
    return uno
    

if __name__ == '__main__':
    # threa = threading.Thread(target = hola_mundo, args=("Codi",))
    # threa2 = threading.Thread(target = hola_mundo2, args=("Arturo",))
    # threa3 = threading.Thread(target = hola_mundo3, args=("Hector",))
    
    # threa.start()
    # threa2.start()
    # threa3.start()
    # threa2.join()
    # threa3.join()
    # threa.join()
    #archivos= TopTemas()
    #print(archivos)
    #time.sleep(5)
    
    #api = aceso.cargar_API()
    
    
    # user = {
    #             "user_id": 1500509482853580800,
    #             "name": "\u10e6\u200cLia Gail Martinez lopez \u10e6",
    #             "screen_name": "Pommo38",
    #             "followers_count": 0
    #         }
    # tema = "Cerocahui.json"
    # dataJSON=PrimeraLectura(tema)
    # temas = TopTemas()
    # hechos = ObtenerYaHechos()
    # print("Temas")
    # print(temas)
    # print("hechos")
    # print(hechos)
    # fn = quitar(temas,hechos)
    # print("Esto quedo....")
    # print(fn)
    
    #time.sleep(10)
    
    #relacion = api.show_friendship(source_id = 998066378803380225 , target_id = 93922911 )
    #print (relacion)
    #relacion2 = api.show_friendship(source_screen_name = 'JorgeLejarazo' , target_id = 93922911 )
    #print (relacion2)
    #time.sleep(5)
    # print (user)
    
    # Nconsulta = 150
    # turno = 1

    # lista = list(range(1,30000))
    # print (consulta)
    # time.sleep(5)
    # for n in lista:
    #     if (Nconsulta >= 150):
    #                 if (turno <=14):
    #                     turno +=1
    #                     print (turno)
    #                 else:
    #                     turno = 1
    #                     print (turno)
    #                 print ("Consulta --->" + str(Nconsulta))
    #                 time.sleep(1)
                    
    
    # relac = {}
    # relac = {
    #         'idTuit' : "preuba",
    #         'idApunta' : "prueba",
    #         'following' : "prueba",
    #         'followed_by': "prueba"        
    #     }
    
    for tuit in dataJSON['tuits']:
        #print(tuit)
        
        print(tuit['relacion'])
        try:
            if (tuit['relacion']['idTuit'] != "original"):
                print("si es diferente")
                if (tuit['relacion']['idTuit'] != "error"):
                    if (tuit['relacion']['following'] == True):
                        print("El lo sigue")
                    if (tuit['relacion']['followed_by'] == True):
                        print("Lo siguen a el")
                        time.sleep(5)
            else:
                print("Es igual")
                #time.sleep(2)
        except Exception:
            print("Error: ")
        #print (tuit)
    time.sleep(15)

    print ("Hola Mundo desde el hilo principal")
    lista = list(range(1,15))
    print(lista)
    turno = 1
    
    for n in lista:
     if n <= 12:
         print("entro " + str(n))
     else:
         print("no entro")     
    