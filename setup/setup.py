# Module for environment variables
from decouple import config
# Module for spotifyApi and MongoDB
from models.spotify_api import SpotifyBubuApi
from pymongo import MongoClient # MongoDB



def get_Spotify_API():
    # Get environment variables from a hidden .env file
    ###### Spotify credentials ######
    secret_key            = config('SECRET_KEY')
    spotify_client_id     = config('SPOTIFY_CLIENT_ID')
    spotify_client_secret = config('SPOTIFY_CLIENT_SECRET')
    spotify_redirect_uri  = config('SPOTIFY_REDIRECT_URI')

    # Instance of SpotifyBubuApi
    spotify = SpotifyBubuApi(
        spotify_client_id,
        spotify_client_secret,
        spotify_redirect_uri
    )

    return spotify

def get_mongo_client():
    ###### Mongo credentials ######
    # Get the mongo credentials
    mongo_username = config('MONGO_USERNAME')
    mongo_password = config('MONGO_PASSWORD')
    mongodb_name   = config('MONGODB_NAME')

    # Get access to the cluster
    mongo_client = MongoClient(f"mongodb+srv://{mongo_username}:{mongo_password}@spotlighfy-cluster1.f73bs.mongodb.net/{mongodb_name}?retryWrites=true&w=majority")
    # Create a Mongo client object and create the db
    db = mongo_client['users']

    return db