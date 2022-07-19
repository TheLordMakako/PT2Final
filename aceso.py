import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. '''
    consumer_key='9VkHwII39Rsm6gRNW7WEfocYP'
    consumer_secret='k37XqkCvQBIENvO0TDoHK284X8ae3hdCkPH9lE5LsAiMJ7Aao0'
    access_token='1486853876292542464-FMa0uYCCjiRSRCvYGel3vmzUICbxpH'
    access_token_secret='MGReUSafE6tpzTKekLWty3tR73iy6BeUJeoWzKErDx067'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # load the twitter API via tweepy
    return api

