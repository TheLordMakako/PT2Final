from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
import asyncio
import json
import time
import re
import os
import aceso2

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
_gremlin_cleanup_graph = "g.V().drop()"
Nconsulta = 0
turno=1
api = aceso2.cargar_API()

def solicitaAPI(turno):
    global api
    if (turno == 1):
        api=aceso2.cargar_API()
    elif (turno == 2):
        api=aceso2.cargar_API2()
    elif (turno == 3):
        api=aceso2.cargar_API3()
    elif (turno == 4):
        api=aceso2.cargar_API4()
    elif (turno == 5):
        api=aceso2.cargar_API5()
    elif (turno == 6):
        api=aceso2.cargar_API6()
    elif (turno == 7):
        api=aceso2.cargar_API7()
    elif (turno == 8):
        api=aceso2.cargar_API8()
    elif (turno == 9):
        api=aceso2.cargar_API9()
    elif (turno == 10):
        api=aceso2.cargar_API10()
    elif (turno == 11):
        api=aceso2.cargar_API11()
    elif (turno == 12):
        api=aceso2.cargar_API12()
 

def print_status_attributes(result): 
    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))

def cleanup_graph(cliente):
    print("\n> {0}".format(_gremlin_cleanup_graph))
    callback = cliente.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result()

def PrimeraLectura(archivo):
    rutautil="C:\Python\PT2Final\DataLimpiezaTexto"
    NomArchivo=rutautil+'\\'+archivo
    global data
    try:
        with open(NomArchivo, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("No se encontro archivo JSON " + str(e))     
    finally:
        return data

def ObtenerTodosLosNombres():
    try:
            ruta='C:\Python\PT2Final\DataLimpiezaTexto'
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+str(e))

def ConsultaRelacion (idTuit, idApunta):
    global Nconsulta
    if (Nconsulta >= 150):
        global turno
        if turno <=12:
            turno +=1
        else:
            turno = 1
        solicitaAPI(turno)    
        
    relacion = api.show_friendship(source_id = idTuit , target_id = idApunta )
    rela={
            'idTuit' : str(idTuit),
            'idApunta' : str(idApunta),
            'following' : relacion[0].following,
            'followed_by': relacion[0].followed_by        
        }
    Nconsulta += 1
    return rela
    
def insert_vertices(cliente, data):
    for query in data:
        print("\n> {0}\n".format(query))
        callback = cliente.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this vertex:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")
    print("\n")
    
def insert_edges(cliente, data2):
    for query in data2:
        print("\n> {0}\n".format(query))
        callback = cliente.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())
        print("\n")
    print("\n")
    
def CambioDeClient (n):
    cliente = client.Client('wss://prueba2022.gremlin.cosmos.azure.com:443/', 'g',
                           username="/dbs/tendencias/colls/tendencia"+ str(n) +"",
                           password="pTxq2nEit9Ce2nVBmumD9FQfsw6ytcYcWHCVwoJsKoZueQcOqhKYrWm5yCbjwPHwFiSmCA5eqcQZYYEoOKbtAQ==",
                           message_serializer=serializer.GraphSONSerializersV2d0())
    return cliente

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


def main():
    data=[]
    data2=[]                      
    tiempoInicio=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    archivos=TopTemas()
    n=0

    
    for tema in archivos:
        print(n)
        cliente= CambioDeClient(n)
        cleanup_graph(cliente)
        try:
                print(tema)
                time.sleep(5)
                dataJSON=PrimeraLectura(tema) #Saca todos los tuits de un archivo enviando el nombre del archivo
                contador=0
                data=[]
                data2=[]
                for tuit in dataJSON['tuits']:
                    contador+=1
                    relac = {}
                    try:
                        if (tuit['idTipo'] == 3):
                            #print ("Consultando  relaciones de respuesta")
                            relac = ConsultaRelacion(tuit['user']['user_id'], tuit['in_reply_to_user_id'])
                        elif (tuit['idTipo'] == 2):
                            #print("Consultando relaciones de retuit")
                            relac = ConsultaRelacion(tuit['user']['user_id'], tuit['retweeted_status']['id_user'])
                        else:
                            print("No tiene relacion a seguir, es un tuit original")
                    except Exception as e:
                        print("Error en el ciclo de las relaciones " + str(e))
                    #Crea todos los nodos
                    try:
                        if (tuit['idTipo'] == 3):
                            data.append("g.addV('respuesta').property('id', '"+ str(tuit['id']) +"').property('creado','"+tuit['created_at']+"').property('text','"+tuit['text']+"').property('user_id','"+ str(tuit['user']['user_id']) +"').property('user_nombre','"+tuit['user']['name']+"').property('user_followers',"+ str(tuit['user']['followers_count'])+").property('respuesta tuit id','"+tuit['in_reply_to_status_id_str']+"').property('nombre del tuit responde','"+tuit['in_reply_to_screen_name']+"').property('pk', '3')")
                        elif (tuit['idTipo'] ==2):
                            data.append("g.addV('retuit').property('id','"+ str(tuit['id']) +"').property('creado','"+tuit['created_at']+"').property('text','"+tuit['text']+"').property('user_id','"+ str(tuit['user']['user_id'])+"').property('user_nombre','"+tuit['user']['name']+"').property('user_followers',"+ str(tuit['user']['followers_count'])+").property('id tuit original', '"+ str(tuit['retweeted_status']['id'])+"').property('nombre del tuit original','"+tuit['retweeted_status']['name_user']+"').property('pk', '2')")
                        else:
                            data.append("g.addV('tuit').property('id', '"+ str(tuit['id']) +"').property('creado','"+tuit['created_at']+"').property('text','"+tuit['text']+"').property('user_id','"+ str(tuit['user']['user_id'])+"').property('user_nombre','"+tuit['user']['name']+"').property('user_followers',"+str(tuit['user']['followers_count'])+").property('pk', '1')")
                    except Exception as e:
                        print ("Error en el bucle de generar el query para la base" + str(e))
                    #Crea todas las relaciones
                    try:
                        if (tuit['idTipo'] == 3):
                            data2.append("g.V('"+ str(tuit['id']) +"').addE('Responde_a').to(g.V('"+ tuit['in_reply_to_status_id_str'] +"'))")
                        elif (tuit['idTipo'] ==2):
                            data2.append("g.V('"+ str(tuit['id']) +"').addE('retuit_de').to(g.V('"+ str(tuit['retweeted_status']['id']) +"'))")
                        if (relac != {}):
                            if (relac['following']):
                                data2.append("g.V('"+ relac['idTuit'] +"').addE('sigue').to(g.V('"+ relac['idApunta'] +"'))")
                            if (relac['followed_by']):
                                data2.append("g.V('"+ relac['idApunta'] +"').addE('sigue').to(g.V('"+ relac['idTuit'] +"'))")        
                    except Exception as e:
                        print("Error al crear las relaciones " + str(e))
                    print("Tuit: " + str(contador))
                try:
                    insert_vertices(cliente,data)
                    print("Termino de insertar nodos")
                    insert_edges(cliente, data2)
                except Exception as e:
                    print("Error al insertar en la base "+str(e))        
        except Exception as e:
                print ("Error en el bucle general " + str(e))
        print("Termine el tema: " + tema)
        print("Tiempo de inicio: " + tiempoInicio)
        print("Tiempo de fin: "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        n+=1
        time.sleep (10)
    


if __name__ == "__main__":
    main()