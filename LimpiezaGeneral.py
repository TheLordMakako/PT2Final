import json
import time
import re
import os
import emoji  #se instala la libreria
import unidecode #se instala la libreria
import tweepy
import aceso


data={}
data['tuits'] = []
dataJSON={}
dataJSON['tuits'] = []
dataJSON2={}
dataJSON2['tuits'] = []
dataFinal={}
dataFinal['tuits'] = []
ListaCarpetas=[] 
api=aceso.cargar_API()

def PrimeraLectura(archivo):
    rutautil="C:\Python\PT2Final\DatosFinales"
    NomArchivo=rutautil+'\\'+archivo
    global data
    try:
        with open(NomArchivo, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print("No se encontro archivo JSON " + str(e))     
    finally:
        return data

def deEmojify2(text):
    return emoji.replace_emoji(text)
    #return emoji.get_emoji_regexp().sub(r'', text.decode('utf8'))


    
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        u"\U00010000-\U0001FFFF"      #Todo
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def GuardadoFinal(data,tema):
    os.makedirs('C:\Python\PT2Final\DataLimpiezaTexto', exist_ok=True) 
    NomArchivo='C:\Python\PT2Final\DataLimpiezaTexto/'+tema   
    try:
        with open(NomArchivo, 'w') as file:
         json.dump(data, file, indent=4, default=str)
    except Exception as e:
        print("Error al ultimo guardado del tema "+tema+" porque: "+str(e))
        time.sleep(5)
        
def ObtenerTodosLosNombres():
    try:
        ruta='C:\Python\PT2Final\DatosFinales'
        contenido = os.listdir(ruta) #Obtiene toda la lista de esa ruta
        return contenido
            
    except Exception as e:
        print("Error al Obtener todas las carpetas: "+str(e))


    
def main():
    tiempoInicio=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    archivos=ObtenerTodosLosNombres()
    for archivo in archivos:
        try:
            print(archivo)
            dataJSON=PrimeraLectura(archivo) #Saca todos los tuits de un archivo enviando el nombre del archivo
            contador=0
            for tuit in dataJSON['tuits']:
                mencion = len(tuit['users_mentions'])
                #print("Numero de tuit: "+ str(contador))
                tuit['text']=tuit['text'].replace("@","o").replace("'","")
                tuit['user']['name'] = tuit['user']['name'].replace ("@","o").replace("'","")
                if (tuit['idTipo'] == 2):
                    tuit['retweeted_status']['text'] = tuit['retweeted_status']['text'].replace ("@","o").replace("'","")
                    SinTilde2 = unidecode.unidecode(tuit['retweeted_status']['text'])
                    limpiado2 = re.sub(r"[^a-z' 'A-Z0-9]","",SinTilde2)
                    tuit['retweeted_status']['text'] = limpiado2
                    tuit['retweeted_status']['name_user'] = tuit['retweeted_status']['name_user'].replace ("@","o").replace("'","")
                    SinTilde5 = unidecode.unidecode(tuit['retweeted_status']['name_user'])
                    limpiado5 = re.sub(r"[^a-z' 'A-Z0-9]","",SinTilde5)
                    tuit['retweeted_status']['name_user'] = limpiado5
                    tuit['retweeted_status']['text'] = tuit['retweeted_status']['text'].replace ("@","o").replace("'","")
                    tuit['retweeted_status']['name_user'] = tuit['retweeted_status']['name_user'].replace ("@","o").replace("'","")
                if ( mencion != 0):
                    lst = list (range(0,mencion))
                    for i in lst:    
                        tuit['users_mentions'][i]['name'] = tuit['users_mentions'][i]['name'].replace ("@","o").replace("'","")
                        SinTilde3 = unidecode.unidecode(tuit['users_mentions'][i]['name'])
                        limpiado3 = re.sub(r"[^a-z' 'A-Z0-9]","",SinTilde3)
                        tuit['users_mentions'][i]['name'] = limpiado3
                        tuit['users_mentions'][i]['name'] = tuit['users_mentions'][i]['name'].replace ("@","o").replace("'","")
                
                SinTilde = unidecode.unidecode(tuit['text'])
                SinTilde4 = unidecode.unidecode(tuit['user']['name'])
                limpiado = re.sub(r"[^a-z' 'A-Z0-9]","",SinTilde)
                limpiado4 = re.sub(r"[^a-z' 'A-Z0-9]","",SinTilde4)
                tuit['text'] = limpiado
                tuit['user']['name'] = limpiado4
                tuit['text']=tuit['text'].replace("@","o").replace("'","")
                tuit['user']['name'] = tuit['user']['name'].replace ("@","o").replace("'","")
                contador+=1
            GuardadoFinal(dataJSON,archivo)
        except Exception as e:
            print("Error en el bucle principal del main: "+ str(e))
    print("Inicie: "+tiempoInicio)
    tiempoFinal=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("Termine: "+tiempoFinal)
    time.sleep(5)


if __name__ == "__main__":
    main()