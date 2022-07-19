from cmath import e
from html import entities
from importlib.resources import path
from tkinter import E
from turtle import position
from unicodedata import name
import os
import json
from datetime import date, datetime
import time
import sys
from os import remove
from os import path

zonas =[1,2,3,4,5,6]
data={}
data['tuits'] = []
dataJSON={}
dataJSON['tuits'] = []
dataJSON2={}
dataJSON2['tuits'] = []
dataFinal={}
dataFinal['tuits'] = []
ListaCarpetas=[]
dataAfter={}
dataAfter['tuits'] = []

def PrimeraLectura(ruta,carpeta,zona):
    rutautil=ruta+ "\\" + carpeta
    NomArchivo=rutautil+'\C'+str(zona)+'_'+carpeta+'.json'
    global data
    try:
        with open(NomArchivo, 'r') as file:
            data = json.load(file)
    except:
        print("No se encontro archivo JSON")     
    finally:
        return data


def GuardadoFinal(data,tema):
    os.makedirs('C:\Python\PT2Final\DatosFinales/', exist_ok=True) 
    NomArchivo='DatosFinales/'+tema+'.json'    
    try:
        with open(NomArchivo, 'w') as file:
         json.dump(data, file, indent=4, default=str)
    except Exception as e:
        print("Error al ultimo guardado ---->" + str(e))
        
def ObtenerTodasCarpetas():
    try:
        for zona in zonas:
            ruta='C:\Python\PT2Final\Zona'+str(zona)+'\C'+str(zona)
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            ListaCarpetas.extend(contenido) #agrega esa lista a la lista de carpetas como elemento independiente
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+str(e))
    
    resul=[]
    for element in ListaCarpetas:
        if element not in resul:
            resul.append(element)

    return resul
    
def SegundaLectura(carpeta):
    NomArchivo='C:\Python\PT2Final\DatosFinales/'+carpeta+'.json' 
    global dataAfter
    try:
        with open(NomArchivo, 'r') as file:
            dataAfter = json.load(file)
    except:
        print("No hay archivo con tuits anteriores a la fecha")     
    finally:
        return dataAfter
    
def TodosTuits(carpeta):
    global TodoData
    try:
            TodoData={}
            TodoData['tuits']=[] 
            for zona in zonas:
                ruta='C:\Python\PT2Final\Zona'+str(zona)+'\C'+str(zona)
                contenido = os.listdir(ruta)
                for carpetaComparar in contenido:
                    if (carpeta==carpetaComparar):
                        dataJSON=PrimeraLectura(ruta,carpeta,zona)
                        TodoData['tuits'].extend(dataJSON['tuits'])
    except Exception as s:
        print("Error por ----->  "+s)
    finally:
        return TodoData
    
def LimpiarTuits(TodoDatas):
    global TodoData
    try:
        for element in TodoDatas['tuits']:
                    repetidos=[]
                    for s in range(len(TodoDatas['tuits'])):
                        if (TodoDatas['tuits'][s]["id"] == element['id']):
                            repetidos.append(s)
                    if (len(repetidos) >> 1):
                        repetidos.pop(0)
                        repetidos.reverse()
                        for extraer in repetidos:
                            try:
                                TodoData['tuits'].pop(extraer)
                            except Exception as e:
                                print(e)
                                print("ciclo que paro: "+str(extraer))
    except Exception as e:
        print("error en la funcion LimpiarTuits: "+e)
    finally:
        return TodoData
    
def BorrarJSON(carpet):
    NomArchivo='DatosFinales/'+carpet+'.json'
    if path.exists(NomArchivo):
        remove(NomArchivo)
        return True
    else:
        return False
        
           
       
def main():
    tiempoInicio=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    ListaCarpetas=ObtenerTodasCarpetas()    
    for carpeta in ListaCarpetas:
        TodoData=TodosTuits(carpeta)
        print("Este es lo largo del TodoData en todas las zonas con repetidos "+str(len(TodoData['tuits']))) 
        TodoData=LimpiarTuits(TodoData)         
        print("Este es lo largo del TodoData en todas las zonas sin repetidos "+str(len(TodoData['tuits'])))
        # time.sleep(20)
        dataAfter=SegundaLectura(carpeta)
        repetid=[]
        contador=0
        if dataAfter['tuits']:
            for info in dataAfter['tuits']:
                for info2 in TodoData['tuits']:
                    if (info['id']==info2['id']):
                        repetid.append(contador)
                contador+=1
            repetid.reverse()
            for extr in repetid:
                try:
                    dataAfter['tuits'].pop(extr)
                except Exception as e:
                    print(e)
                    print("ciclo en el que paro"+str(extr))
            TodoData['tuits'].extend(dataAfter['tuits'])
            print(BorrarJSON(carpeta))
            print("Este es lo largo del TodoData al final sin repetidos "+str(len(TodoData['tuits'])))    
        GuardadoFinal(TodoData,carpeta)
    print("Inicie: "+tiempoInicio)
    tiempoFinal=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("Termine: "+tiempoFinal)
    #time.sleep(5)  
       
        


if __name__ == "__main__":
    main()