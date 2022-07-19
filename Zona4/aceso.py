import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. C4'''
    consumer_key='diWIdGV6yVjUPKI5B4lFeBmY6'
    consumer_secret='pPf2dJEzjvlMZkpoMoOf0JMoPqdwfjtBevZchtltDbVxshm54c'
    access_token='135715415-BREO00UJUAhJnwOzKAKTCMsDl6d8K4cpzLYlP6i9'
    access_token_secret='VNMNRM8ttd2B0XqyWqmmuDiEBa4pG50aaNaIm2wzY1AY4'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # load the twitter API via tweepy
    return api

