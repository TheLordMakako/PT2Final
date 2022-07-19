import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. '''
    consumer_key='r9p6YbPA6lT0TdlsVFoVbQABv'
    consumer_secret='nHHlg3idS79IT5L7jPzZUiLHG1EC6v8mUZE2XvUAMytXt8xeZN'
    access_token='135715415-HmBzopkp0UIO1u7hLxkWZcrW5k7sHm81TAbftNry'
    access_token_secret='w5IJC7DxgBykVDLVZ2gulX05EIekMHzNcDCqU1kHSeuai'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    #return tweepy.API(auth)
    return api

