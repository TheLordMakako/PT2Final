from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import mysql.connector
from mysql.connector import errorcode
import sys
import traceback
import asyncio
import json
import time
import re
import os
import unidecode
import aceso2

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
error = []

config = {
  'host':'proyecto-terminal2.mysql.database.azure.com',
  'user':'director@proyecto-terminal2',
  'password':'Terla1313',
  'database':'nombrestendencias',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '<path-to-SSL-cert>/DigiCertGlobalRootG2.crt.pem'
}
    
_gremlin_cleanup_graph = "g.V().drop()"

def print_status_attributes(result): 
    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))
    
def cleanup_graph(cliente):
    print("\n> {0}".format(_gremlin_cleanup_graph))
    callback = cliente.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result()

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

def ObtenerTodosLosNombres():
    try:
            ruta='C:\Python\PT2Final\DataBase'
            contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
            return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+str(e))

def TopTemas ():
    Tendencia = ObtenerTodosLosNombres()
    Tende =[]
    Final = []
    if (len(Tendencia) >= 10):
        for tema in Tendencia:
            contador = 0
            datas = PrimeraLectura(tema)
            for tuit in datas['tuits']:
                contador+=1
            #print ("El archivo es: "+ tema + "Tiene " +str(contador)+ " tuits")
            Tende.append((tema,contador))    
        pels_sorted = sorted(Tende, reverse=True, key=lambda tupla: tupla[1])
        top_10 = pels_sorted[:10]
        for n in top_10:
            Final.append(n[0])
        return Final
    return Tendencia

def insert_vertices(cliente, data):
    Nquery = 0
    Nmiles = 0 
    for query in data:
        if (Nquery >= 998):
            print("numero de solicitud superada, detengo el query por un segundo")
            print("Miles numero ---->  "+str(Nmiles))
            Nquery = 0
            Nmiles+= 1
            time.sleep(3)
        print("\n> {0}\n".format(query))
        callback = cliente.submitAsync(query)
        if callback.result() is []:
            print ("error al intentar el query ----> ")
            print(query)
    #     if callback.result() is not None:
    #         print("\tInsertando en la base: \n\t{0}".format(
    #             callback.result().all().result()))
    #     else:
    #         print("Algo salio mal con esta petición : {0}".format(query))
        Nquery+=1
    #     print("\n")
    #     print_status_attributes(callback.result())
    #     print("\n")
    # print("\n")
    
def insert_edges(cliente, data2):
    global error
    Nquery = 0
    Nmiles = 0
    for query in data2:
        if (Nquery >= 998):
            print("numero de solicitud superada, detengo el query por un segundo")
            print("Miles numero ---->  "+str(Nmiles))
            time.sleep(3)
            Nquery = 0
            Nmiles+= 1
        print("\n> {0}\n".format(query))
        callback = cliente.submitAsync(query)
        if callback.result() is []:
            error.append({
                "query" : query
            })
            print ("Error al intentar el query ----> ")
            print(query)
        Nquery+=1
            #time.sleep(10)
    #     if callback.result() is not None:
    #         #print("\t Respuesta de la base: \n\t{0}\n".format(callback.result().all().result()))
    #         #time.sleep(3)
    #     else:
    #         print("Something went wrong with this query:\n\t{0}".format(query))
    #     print_status_attributes(callback.result())
    #     print("\n")
    # print("\n")
    
def CambioDeCliente (n):
    cliente = client.Client('wss://temas.gremlin.cosmos.azure.com:443/', 'g',
                           username="/dbs/tendencias/colls/tendencia"+ str(n) +"",
                           password="440HwG8jQ2nHlBHoLdOLU4S6tnC3d8iwYJuTWlNCt6RvbfdMkv3AC8Nc4RyrlszVDEwPoMrNpsG9JCumDRalVQ==",
                           message_serializer=serializer.GraphSONSerializersV2d0())
    return cliente

def GuardadoFinal(data,tema):
    os.makedirs('C:\Python\PT2Final\ErrorDataBase', exist_ok=True) 
    NomArchivo='C:\Python\PT2Final\ErrorDataBase/'+tema   
    try:
        with open(NomArchivo, 'w') as file:
         json.dump(data, file, indent=4, default=str)
    except Exception as e:
        print("Error al ultimo guardado del tema "+tema+" porque: "+str(e))
        time.sleep(5)

def TablaTendencia(conn,tema,contador, grafo):
    cursor = conn.cursor()
    print(conn)
    print(tema)
    tema=tema.replace("#","").replace(".json","")
    tema2 = unidecode.unidecode(tema)
    print(tema2)
    print(contador)
    print(grafo)
    try:
        #Consulta si ya existe el tema
        cursor.execute("SELECT * FROM tendencia where name = '"+tema2+"';")
        rows = cursor.fetchall()
        if (cursor.rowcount > 0):
            cursor.execute("UPDATE tendencia SET tuits = %s, grafo = %s WHERE name = %s;", (contador, 12, tema2))
            print("ya hay uno igual, actualizamos los tuits, el grafo y la fecha") #los grafos 12 son los que tenemos la información pero estan fuera de linea por no estar en la base de azure
        else:
            cursor.execute("INSERT INTO tendencia (name, tuits, grafo, fecha) values ('" + tema2 + "',"+str(contador)+","+str(grafo) +", now());")
            print("No hay uno igual, se inserta")
    except Exception as e:
        print("Error al escribir en la base---->"+str(e))             
    conn.commit()
    cursor.close()
    conn.close()
    





def main():
    data=[]
    data2=[]                      
    tiempoInicio=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    archivos=TopTemas()
    n = 0
    for tema in archivos:
        global error
        error = []
        print("Cliente numero base --->"+str(n))
        cliente = CambioDeCliente(n)
        cleanup_graph(cliente)
        try:
            print(tema)
            dataJSON=PrimeraLectura(tema)
            contador = 0
            data=[]
            data2=[]
            for tuit in dataJSON['tuits']:
                contador+=1
                try:
                    #Crea todos los nodos
                    if (tuit['idTipo'] == 3):
                            data.append("g.addV('respuesta').property('id', '"+ str(tuit['id']) +"').property('creado',"+str(tuit['created_at'])+").property('text','"+tuit['text']+"').property('user_id','"+ str(tuit['user']['user_id']) +"').property('user_nombre','"+tuit['user']['name']+"').property('user_followers',"+ str(tuit['user']['followers_count'])+").property('respuesta tuit id','"+tuit['in_reply_to_status_id_str']+"').property('nombre del tuit responde','"+tuit['in_reply_to_screen_name']+"').property('pk', '3')")
                    elif (tuit['idTipo'] ==2):
                            data.append("g.addV('retuit').property('id','"+ str(tuit['id']) +"').property('creado',"+str(tuit['created_at'])+").property('text','"+tuit['text']+"').property('user_id','"+ str(tuit['user']['user_id'])+"').property('user_nombre','"+tuit['user']['name']+"').property('user_followers',"+ str(tuit['user']['followers_count'])+").property('id tuit original', '"+ str(tuit['retweeted_status']['id'])+"').property('nombre del tuit original','"+tuit['retweeted_status']['name_user']+"').property('pk', '2')")
                    else:
                            data.append("g.addV('tuit').property('id', '"+ str(tuit['id']) +"').property('creado',"+str(tuit['created_at'])+").property('text','"+tuit['text']+"').property('user_id','"+ str(tuit['user']['user_id'])+"').property('user_nombre','"+tuit['user']['name']+"').property('user_followers',"+str(tuit['user']['followers_count'])+").property('pk', '1')")
                except Exception as e:
                    print("Error en el ciclo del tuit "+tuit+" ---> Error: "+str(e))
                    time.sleep(3)
                
                try:
                    if (tuit['relacion']['idTuit'] != "original" and tuit['relacion']['idTuit'] != "error"):
                        if (tuit['idTipo'] == 3):
                            data2.append("g.V('"+ str(tuit['id']) +"').addE('Responde_a').to(g.V('"+ tuit['in_reply_to_status_id_str'] +"'))")
                        elif (tuit['idTipo'] ==2):
                            data2.append("g.V('"+ str(tuit['id']) +"').addE('Retuit_de').to(g.V('"+ str(tuit['retweeted_status']['id']) +"'))")
                        if (tuit['relacion']['idTuit'] != "error" ):
                            if (tuit['relacion']['following'] == True):
                                if (tuit['idTipo'] == 3):
                                    data2.append("g.V('"+ str(tuit['id']) +"').addE('sigue').to(g.V('"+ tuit['in_reply_to_status_id_str'] +"'))")
                                elif (tuit['idTipo'] ==2):
                                    data2.append("g.V('"+ str(tuit['id']) +"').addE('sigue').to(g.V('"+ str(tuit['retweeted_status']['id']) +"'))")
                            if (tuit['relacion']['followed_by'] == True):
                                if (tuit['idTipo'] == 3):
                                    data2.append("g.V('"+ tuit['in_reply_to_status_id_str'] +"').addE('sigue').to(g.V('"+ str(tuit['id']) +"'))")
                                elif (tuit['idTipo'] ==2):
                                    data2.append("g.V('"+ str(tuit['retweeted_status']['id']) +"').addE('sigue').to(g.V('"+ str(tuit['id']) +"'))")
                    elif (tuit['relacion']['idTuit'] == "error"):
                        data2.append("g.V('"+str(tuit['id'])+"').addE('Error_consulta_relacion').to(g.V('111')) ")       
                except Exception as e:
                        print("Error al crear las relaciones " + str(e))
                        time.sleep(3)
                print("Tuit: " + str(contador))
                
            try:
                data.append("g.addV('Error').property('id','111').property('text','Error no se pudo saber cual es la relacion con el tuit').property('pk', '4') ")
                data.append("g.addV('Error').property('id','222').property('text','El tuit al que refiere esta fuera en el muestreo').property('pk', '4') ")
                print("Trabajando solicitudes del tema ----->  "+tema)
                insert_vertices(cliente,data)
                print("Termino de insertar nodos")
                insert_edges(cliente, data2)
                print("Termino de insertar aristas")
                conn = mysql.connector.connect(**config)
                print("Connection a Azure mysql")
                time.sleep(5)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Nombre de usuario o password incorrectas")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Base de datos no existe")
                else:
                    print(err)
            except Exception as e:
                    print("Error al insertar en la base de Gremlin "+str(e))
                    time.sleep(3)
            else:
                #actualizamos la tabla mysql tendencias
                TablaTendencia(conn,tema,contador,n)
                print("Se mando a base SQL")
                time.sleep(4)
                
                
        except Exception as e:
            print("Error en el ciclo principal de temas con el tema "+tema+" ---> Error: "+str(e))
            time.sleep(3)
            
        print("Termine el tema: " + tema)
        GuardadoFinal(error,tema)
        n+=1
        time.sleep(20)
    
    print("Tiempo de inicio: " + tiempoInicio)
    print("Tiempo de fin: "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


if __name__ == "__main__":
    main()