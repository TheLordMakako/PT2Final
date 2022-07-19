import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. '''
    consumer_key='SljqkNS6xHdYUAStSbIx50F1A'
    consumer_secret='auFZTQOvYQuUoAfqSxNPwwTDT0Vh1ESUSmv2WSl77oZ0PSP5Ye'
    access_token='135715415-PLzuDmI8YFLjqoV3jJ8wP1cOC2EckNHW5JOLVxX4'
    access_token_secret='u9fB3f87aKSbv2AaeCPdZZCAu3Zj2RwOfstE4OdppiKn3'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # load the twitter API via tweepy
    return api

