import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. '''
    consumer_key='frCma8T4bj21vAOkLjYig2yUM'
    consumer_secret='f9UaXx0XGWifVSu2FKLLZv4lzg2QlPNAZwtf2oJLDAJwcqeUjF'
    access_token='135715415-Wwc2NC71LiYtkp5DTHbBxetnPY4h370zJ8PLa7bO'
    access_token_secret='aMgOfC4pf6tQKuXPABhi2jn7KpIp0T7C2dsp5JEzsHPRM'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # load the twitter API via tweepy
    return api

