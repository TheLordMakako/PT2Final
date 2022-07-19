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

from neo4j import Query


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
_gremlin_cleanup_graph = "g.V().hasLabel('tuit').values('creado').min()"

def print_status_attributes(result):

    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))


def consulta(cliente, query):
    callback = cliente.submitAsync(query)
    if callback.result () is not None:
        print(callback.result().all.result())
        query2="g.V().has('tuit','creado',"+str(callback.result().all.result())+")"
        print(query2)
    return query2

def minimo(client):
    print("\n>esto hay {0}".format(
        _gremlin_cleanup_graph))
    callback = client.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        valor = callback.result().all().result()[0]
    
    valor = int(valor)    
    return valor

def nodo(cliente,fecha):
    query2 ="g.V().has('tuit','creado',"+str(fecha)+")" 
    print("\n>esto hay {0}".format(
        query2))
    callback = cliente.submitAsync(query2)
    if callback.result() is not None:
        valor = callback.result().all().result()
    return valor
    
def centralidad (cliente, id):
    query3 = "g.V('"+str(id)+"').inE().count()"
    print("\n>esto hay {0}".format(
        query3))
    callback = cliente.submitAsync(query3)
    if callback.result() is not None:
        valor = callback.result().all().result()[0]
    print(valor)
    time.sleep(2)
    return valor
    
    
def main ():
    cliente = client.Client('wss://tendencias.gremlin.cosmos.azure.com:443/', 'g',
                           username="/dbs/ProyectoTerminal/colls/tendencia0",
                           password="sTFKKjM662CHmYlqApb84htpahDb0AEPBurUlPYXF3ac0bdNihJhU2EaECP6NoQJUUCFRaFATgkfsiFgtf8yBA==",
                           message_serializer=serializer.GraphSONSerializersV2d0())
    
    
    _gremlin_traversals = {
    "Get all persons older than 40": "g.V().hasLabel('person').has('age', gt(40)).values('firstName', 'age')",
    "Get all persons and their first name": "g.V().hasLabel('person').values('firstName')",
    "Get all persons sorted by first name": "g.V().hasLabel('person').order().by('firstName', incr).values('firstName')",
    "Get all persons that Thomas knows": "g.V('thomas').out('knows').hasLabel('person').values('firstName')",
    "People known by those who Thomas knows": "g.V('thomas').out('knows').hasLabel('person').out('knows').hasLabel('person').values('firstName')",
    "Get the path from Thomas to Robin": "g.V('thomas').repeat(out()).until(has('id', 'robin')).path().by('firstName')"
    }
    
    centralid =[]
    resp = minimo(cliente)
    nod = nodo(cliente, resp)
    validar = len(nod)
    if validar == 0:
        print("no trae nada")
    elif validar == 1:
        aristas = centralidad(cliente, nod[0]["id"])
        print(aristas)
        print("solo tiene uno")
    else:
        bandera = 0
        for n in nod:
            if bandera==0:
                aristas = centralidad(cliente, n["id"])
                centralid.append((n["id"],aristas))
        print(centralid)
        pels_sorted = sorted(centralid, reverse=True, key=lambda tupla: tupla[1])
        top=pels_sorted[0]
        print("El tuit con id: "+str(top[0])+"es el top al tener: "+str(top[1])+" Aristas")
        time.sleep(5)
        

    
    time.sleep(5)

    
    
if __name__ == "__main__":
    main()