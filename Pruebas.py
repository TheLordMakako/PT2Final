import json
import os
import time
import aceso2
from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
_gremlin_cleanup_graph = "g.V().drop()"

api=aceso2.cargar_API()

client = client.Client('wss://prueba2022.gremlin.cosmos.azure.com:443/', 'g',
                           username="/dbs/sample-database/colls/sample-graph",
                           password="pTxq2nEit9Ce2nVBmumD9FQfsw6ytcYcWHCVwoJsKoZueQcOqhKYrWm5yCbjwPHwFiSmCA5eqcQZYYEoOKbtAQ==",
                           message_serializer=serializer.GraphSONSerializersV2d0()
                           )

def cleanup_graph(client):
    print("\n>esto hay {0}".format(
        _gremlin_cleanup_graph))
    callback = client.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result() 
    print("\n")
    print_status_attributes(callback.result())
    print("\n")

def print_status_attributes(result):
    # This logs the status attributes returned for successful requests.
    # See list of available response status attributes (headers) that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    #
    # These responses includes total request units charged and total server latency time.
    # 
    # IMPORTANT: Make sure to consume ALL results returend by cliient tothe final status attributes
    # for a request. Gremlin result are stream as a sequence of partial response messages
    # where the last response contents the complete status attributes set.
    #
    # This can be 
    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))


def PrimeraLectura(archivo):
    rutautil="DataLimpiezaTexto"
    NomArchivo=rutautil+'\\'+archivo
    global data
    try:
        with open(NomArchivo, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("No se encontro archivo JSON " + e)     
    finally:
        return data
    
def ObtenerTodosLosNombres():
    try:
            ruta='DataLimpiezaTexto'
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+e)

def ConsultaRelacion (idTuit, idApunta):
    
    relacion = api.show_friendship(source_id = idTuit , target_id = idApunta )
    rela={
        'idTuit' : str(idTuit),
        'idApunta' : str(idApunta),
        'following' : relacion[0].following,
        'followed_by': relacion[0].followed_by        
    }
    return rela

def insert_vertices(client, data):
    for query in data:
        print("\n> {0}\n".format(query))
        try:
            callback = client.submitAsync(query)
        except Exception as e:
            print("Error --> "+str(e))
        if callback.result() is not None:
            print("\tInserted this vertex:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")

    print("\n")
    
def insert_edges(client, data2):
    for query in data2:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        #print_status_attributes(callback.result())
        print("\n")

    print("\n")




       
def main():
        
    archivos=ObtenerTodosLosNombres()
    # print (archivos[1])
    # time.sleep (10)
    # for tema in archivos:
    #     contador = 0
    #     datas = PrimeraLectura(tema)
    #     for tuit in datas['tuits']:
    #         contador+=1
    #     print ("El archivo es: "+ tema + "Tiene " +str(contador)+ " tuits")
    #     time.sleep (2)
    cleanup_graph(client)
    tema = archivos[16]
    try:
                data=[]
                data2=[]
                print(tema)
                time.sleep(2)
                dataJSON=PrimeraLectura(tema) #Saca todos los tuits de un archivo enviando el nombre del archivo
                contador=0
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
                    print("esto es lo que hay en el arreglo data")
                    print (data)
                    print("Inicio de insertar nodos")
                    insert_vertices(client,data)
                    print("Termino de insertar nodos")
                    print("Inicio de insertar aristas")
                    insert_edges(client, data2)
                    print("Termino de insertar aristas")
                except Exception as e:
                    print("Error al insertar en la base "+str(e))        
    except Exception as e:
                print ("Error en el bucle general " + str(e))
                
    print ("termine")

if __name__ == '__main__':
    main()