from html import entities
from importlib.resources import path
from unicodedata import name
from datetime import date, datetime
import datetime as dt
import tweepy
import aceso
import os
import json  #para append
import time

#Variables que se tienen que cambiar por SCRIPT
path="PT1.py"        #Esta variable se tiene que cambiar dependiendo del codigo
CDMX='19.188939, -99.084200,15km' # geocode de longitud y latidud, circunferencia de 15 kilometros de radio

API=aceso.cargar_API()
data = {}
data['tuits'] = []
contador_detuits=0
ruta=os.path.dirname(path)     #Valor Path se cambia dependiendo del script a usarse



def get_tendencias():
    woeid=116545   #trends1 = API.trends_place(116545) 116545 es el WOEID para México, México City
    #woeidCDMX=116545
    trends1 = API.trends_place(woeid)
    trends=""
    trends = set([trend['name'] for trend in trends1[0]['trends']])
    tendencias='%s'%(trends)
    tendencias=tendencias.replace('{','')
    tendencias=tendencias.replace('}','')    
    tendencias=tendencias.replace('\'','')
    tendencias=tendencias.replace(' ','')
    tendencias=tendencias.replace('"','')
    tendencias=tendencias.replace('/','')
    tendencias=tendencias.split(',')

    return tendencias[0:20]

def PrimeraLectura(tema):
    #Valor C1 se cambia la numeración dependiendo del script a usarse
    carpeta=ruta+"C1/" + tema
    os.makedirs(carpeta, exist_ok=True)
    NomArchivo=carpeta+'/C1_'+tema+'.json'
    global data
    try:
        with open(NomArchivo, 'r') as file:
            data = json.load(file)
    except:
            with open(NomArchivo, 'w') as file:
                print("se creo archivo JSON")
                data['tuits'] = []
    finally:
        return data
    
def GuardadoFinal(tema,data):
    carpeta=ruta+"C1/" + tema #Valor de C se cambia la numeración dependiendo del script a usarse
    NomArchivo=carpeta+'/C1_'+tema+'.json'    
    try:
        with open(NomArchivo, 'w') as file:
         json.dump(data, file, indent=4, default=str)
    except:
        print("Error al ultimo guardado")


    
    

def main():
    tendencias = get_tendencias()
    for tema in tendencias:
        print('Buscando = ', tema)
        #Abrimos el archivo para almacenar los tuits
        data=PrimeraLectura(tema)
        global contador_detuits
        contador_detuits=0
        try:
            for tweet in tweepy.Cursor(API.search, q=tema, lang='es', tweet_mode='extended', geo=CDMX).items(10000):
                try:
                    for tweetIn in data:
                        if ( tweetIn == 'tuits' or tweet.id != tweetIn["id"]):
                            contador_detuits+= 1
                            try:
                                if (tweet.in_reply_to_status_id != None):
                                            data['tuits'].append({
                                                        'TipoNodo': "respuesta",
                                                        'idTipo': 3,
                                                        'created_at':tweet.created_at,
                                                        'id':tweet.id,
                                                        'text':tweet.full_text,                  
                                                        'users_mentions': tweet.entities["user_mentions"],
                                                        'in_reply_to_status_id': tweet.in_reply_to_status_id,
                                                        'in_reply_to_status_id_str': tweet.in_reply_to_status_id_str,
                                                        'in_reply_to_user_id': tweet.in_reply_to_user_id,
                                                        'in_reply_to_user_id_str': tweet.in_reply_to_user_id_str, 
                                                        'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
                                                        'user':{
                                                            'user_id': tweet.user.id,
                                                            'name': tweet.user.name,
                                                            'screen_name': tweet.user.screen_name,
                                                            'followers_count': tweet.user.followers_count
                                                        },
                                                        'retweet_count': tweet.retweet_count,
                                                        'favorite_count': tweet.favorite_count,
                                                        'favorited': tweet.favorited,
                                                        'retweeted': tweet.retweeted,
                                                        'zona':'C2'    #este cambia dependiendo del circulo en donde se este trabajando
                                                        })
                                        
                                elif (tweet.retweeted_status != None):
                                            data['tuits'].append({
                                                        'TipoNodo': "retuit",
                                                        'idTipo': 2,
                                                        'created_at':tweet.created_at,
                                                        'id':tweet.id,
                                                        'text':tweet.full_text,                  
                                                        'users_mentions': tweet.entities["user_mentions"],
                                                        'in_reply_to_status_id': tweet.in_reply_to_status_id,
                                                        'in_reply_to_status_id_str': tweet.in_reply_to_status_id_str,
                                                        'in_reply_to_user_id': tweet.in_reply_to_user_id,
                                                        'in_reply_to_user_id_str': tweet.in_reply_to_user_id_str, 
                                                        'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
                                                        'user':{
                                                            'user_id': tweet.user.id,
                                                            'name': tweet.user.name,
                                                            'screen_name': tweet.user.screen_name,
                                                            'followers_count': tweet.user.followers_count
                                                        },
                                                         'retweeted_status':{
                                                             'created_at' : tweet.retweeted_status.created_at,
                                                             'id' : tweet.retweeted_status.id,
                                                             'text': tweet.retweeted_status.full_text,
                                                             'id_user' : tweet.retweeted_status.user.id,
                                                             'name_user' : tweet.retweeted_status.user.name,
                                                             'screen_user' : tweet.retweeted_status.user.screen_name,
                                                             'in_reply_to_status_id': tweet.retweeted_status.in_reply_to_status_id,
                                                             'in_reply_to_user_id': tweet.retweeted_status.in_reply_to_user_id,
                                                             'in_reply_to_screen_name' : tweet.retweeted_status.in_reply_to_screen_name
                                                             },
                                                        'retweet_count': tweet.retweet_count,
                                                        'favorite_count': tweet.favorite_count,
                                                        'favorited': tweet.favorited,
                                                        'retweeted': tweet.retweeted,
                                                        'zona':'C2'    #este cambia dependiendo del circulo en donde se este trabajando
                                                        })
                            except Exception as e:
                                data['tuits'].append({
                                                'TipoNodo': "tuit",
                                                'idTipo': 1,
                                                'created_at':tweet.created_at,
                                                'id':tweet.id,
                                                'text':tweet.full_text,                  
                                                'users_mentions': tweet.entities["user_mentions"],
                                                'in_reply_to_status_id': tweet.in_reply_to_status_id,
                                                'in_reply_to_status_id_str': tweet.in_reply_to_status_id_str,
                                                'in_reply_to_user_id': tweet.in_reply_to_user_id,
                                                'in_reply_to_user_id_str': tweet.in_reply_to_user_id_str, 
                                                'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
                                                'user':{
                                                    'user_id': tweet.user.id,
                                                    'name': tweet.user.name,
                                                    'screen_name': tweet.user.screen_name,
                                                    'followers_count': tweet.user.followers_count
                                                },
                                                'retweet_count': tweet.retweet_count,
                                                'favorite_count': tweet.favorite_count,
                                                'favorited': tweet.favorited,
                                                'retweeted': tweet.retweeted,
                                                'zona':'C1'    #este cambia dependiendo del circulo en donde se este trabajando
                                                })
                                        
                            print(contador_detuits)
                        else:
                            print("Tuit ya existente")
                except Exception:
                    print("Fallo en el bucle de tuit "+tema + "continuo: con"+tema[+1])
        except Exception:
            print("Error en el bucle de busqueda de tuit con tema"+tema+"\n")
            #print("y tuit"+tweet+"\n")
        
        finally:
            GuardadoFinal(tema,data)    
    print("Termine todo el script PT1 exitosamente el: "+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    return True        
            
        

if __name__ == "__main__":
    main()