import tweepy


def cargar_API():
    ''' Función que carga la API de twitter después de autorizar al usuario. '''
    consumer_key='TIDRheiPPX9QcgKX1aEYMIdLH'
    consumer_secret='cNvuSHDSsWagJgDlkM3h0VCHc2nWdmt6dO0NV4UEItdVEmXjze'
    access_token='135715415-L9ohTHBIpdTCufPpBWSYSaL4zTgB0d78QdXRzvMe'
    access_token_secret='DhCltIuQIc8b0Vt4snXvlQBWlkbs9oTAyrQeCLKPJDnjE'
    # Autentificamos la app
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Obtenemos nuestro objeto 'api'
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # load the twitter API via tweepy
    #return tweepy.API(auth)
    return api

