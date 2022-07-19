import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. '''
    consumer_key='AjUNkih2FmRZbzgYHYYZfw0jc'
    consumer_secret='S7Br34IxM9QWB6Q5VwWSz3xFLPLKal76JjxuFtPARxTWeewHP6'
    access_token='912691702514749440-hZTvXXS8rG40A0lp37ed8thAdvlGbLp'
    access_token_secret='gTb2WuaLhlelc68zqYMgnUh4AHvvHwGSDrO17lK1RCU3i'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # load the twitter API via tweepy
    return api

