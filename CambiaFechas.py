from datetime import datetime
import time
import json
import os

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
        print("No se encontro archivo JSON " + str(e))     
    finally:
        return data
        
def GuardadoFinal(data,tema):
    os.makedirs('C:\Python\PT2Final\DataBase2/', exist_ok=True) 
    NomArchivo='C:\Python\PT2Final\DataBase2/'+tema+'.json'
    print(NomArchivo)    
    try:
        with open(NomArchivo, 'w') as file:
         json.dump(data, file, indent=4, default=str)
    except:
        print("Error al ultimo guardado")


def main():
    data = []
    data2 = []
    tiempoInicio = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    archivos = ObtenerYaHechos()
    for tema in archivos:
        print("Tema:    "+tema)
        dataJSON = PrimeraLectura(tema)
        contador = 0
        try:
            for tuit in dataJSON['tuits']:
                contador+=1
                date_object = datetime.strptime(tuit['created_at'], "%Y-%m-%d %H:%M:%S")
                print (contador)
                fech =date_object.year*10000000000 + date_object.month*100000000 + date_object.day*1000000 + date_object.hour*10000 + date_object.minute*100 + date_object.second
                tuit['created_at']=fech
            GuardadoFinal(dataJSON,tema)
        except Exception as e:
            print("error -->  "+str(e))
    print("Inicie: "+tiempoInicio)
    tiempoFinal=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("Termine: "+tiempoFinal)





if __name__ == "__main__":
    main()