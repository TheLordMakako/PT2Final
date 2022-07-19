from black import main
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
import asyncio
import json
import time
import re
import os
from datetime import datetime
import aceso2

Nconsulta = 0
api = aceso2.cargar_API()

def solicitaAPI(turno):
    print ("Se cambia de API turno --> " + str(turno))
    if (turno == 1):
        api2 = aceso2.cargar_API()
    elif (turno == 2):
        api2 = aceso2.cargar_API2()
    elif (turno == 3):
        api2 = aceso2.cargar_API3()
    elif (turno == 4):
        api2 = aceso2.cargar_API4()
    elif (turno == 5):
        api2 = aceso2.cargar_API5()
    elif (turno == 6):
        api2 = aceso2.cargar_API6()
    elif (turno == 7):
        api2 = aceso2.cargar_API7()
    elif (turno == 8):
        api2 = aceso2.cargar_API8()
    elif (turno == 9):
        api2 = aceso2.cargar_API9()
    elif (turno == 10):
        api2 = aceso2.cargar_API10()
    elif (turno == 11):
        api2 = aceso2.cargar_API11()
    elif (turno == 12):
        api2 = aceso2.cargar_API12()
    elif (turno == 13):
        api2 = aceso2.cargar_API13()
    elif (turno == 14):
        api2 = aceso2.cargar_API14()
    elif (turno == 15):
        api2 = aceso2.cargar_API15()
    elif (turno == 16):
        api2 = aceso2.cargar_API16()
    return api2

def ConsultaRelacion (apis, idTuit, idApunta, tema):  
    global Nconsulta 
    try:    
        relacion = apis.show_friendship(source_id = idTuit , target_id = idApunta )
        rela={
            'idTuit' : str(idTuit),
            'idApunta' : str(idApunta),
            'following' : relacion[0].following,
            'followed_by': relacion[0].followed_by        
            }
        
    except Exception as e:
        print("Error al hacer la solicitud al API "+ str(e))
        rela = {
            'Error' : "No se pudo saber la relacion",
            'tema' : tema,
            'idTuit' : "error",
            'idTuitError' : str(idTuit),
            'idApunta' : str(idApunta),
        }
    Nconsulta += 1    
    return rela

def ObtenerTodosLosNombres():
    try:
            ruta='C:\Python\PT2Final\DataLimpiezaTexto'
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+e)
        

def PrimeraLectura(archivo):
    rutautil="C:\Python\PT2Final\DataLimpiezaTexto"
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
    top_10 = pels_sorted[0:10]
    for n in top_10:
        Final.append(n[0])
    return Final


def GuardadoFinal(data,tema):
    os.makedirs('C:\Python\PT2Final\DataBase', exist_ok=True) 
    NomArchivo='C:\Python\PT2Final\DataBase/'+tema   
    try:
        with open(NomArchivo, 'w') as file:
         json.dump(data, file, indent=4, default=str)
    except Exception as e:
        print("Error al ultimo guardado del tema "+tema+" porque: "+str(e))
        time.sleep(5)
        
# def ObtenerYaHechos():
#     try:
#             ruta='C:\Python\PT2Final\DataBase'
#             contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
#             return contenido
            
#     except Exception as e:
#         print("Error al Obtener todas las carpetas: "+e)
        
# def Comparartemas(PorFiltrar, hechos):
#     final = []
#     for n in PorFiltrar:
#         if (n is )
    
#     return 


def main():
    data=[]
    tiempoInicio=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    archivos=TopTemas()
    #print (archivos)
    #hechos = ObtenerYaHechos()
    
    turno=1
    for tema in archivos:
        #dataJSON = PrimeraLectura(tema)
        try:
            print(tema)
            #time.sleep(3)
            dataJSON=PrimeraLectura(tema)
            contador = 0
            data=[]
            for tuit in dataJSON['tuits']:
                global Nconsulta
                global api
                date_object = datetime.strptime(tuit['created_at'], "%Y-%m-%d %H:%M:%S")
                fech =date_object.year*10000000000 + date_object.month*100000000 + date_object.day*1000000 + date_object.hour*10000 + date_object.minute*100 + date_object.second
                tuit['created_at']=fech
                if (Nconsulta >= 150):
                    if (turno <=15):
                        turno +=1
                    else:
                        turno = 1
                    Nconsulta =0
                    api = solicitaAPI(turno)
                     
                contador+=1
                relac ={}
                try:
                    if (tuit['idTipo'] == 3):
                            #print ("Consultando  relaciones de respuesta")
                            relac = ConsultaRelacion(api, tuit['user']['user_id'], tuit['in_reply_to_user_id'], tema)
                    elif (tuit['idTipo'] == 2):
                            #print("Consultando relaciones de retuit")
                            relac = ConsultaRelacion(api, tuit['user']['user_id'], tuit['retweeted_status']['id_user'], tema)
                    elif (tuit['idTipo'] == 1):
                            print("No tiene relacion a seguir, es un tuit original")
                            relac ={ "idTuit" : "original"}
                    tuit["relacion"] = relac
                except Exception as e:
                    print("Error en el ciclo lectura de tuits "+ str(e))
                    relac = {"Error": "error al hacer las validaciones", "tema": tema, "IDtuit":str(tuit['id'])}
                    tuit["ErrorRelacion"] = relac 
                print("Tuit: " + str(contador))
            GuardadoFinal(dataJSON,tema)   
        except Exception as e:
            print("Error en el ciclo principal detemas  "+ str(e))
        print("Termine el tema: " + tema)
        print("")
        print(archivos)

            
    print("Tiempo de inicio: " + tiempoInicio)
    print("Tiempo de fin: "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        

if __name__ == '__main__':
    main()
    