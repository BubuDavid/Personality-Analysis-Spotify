# Import important imports
from webbrowser import Error
import requests
import base64

# Create our API object for spotify
class SpotifyBubuApi:
    # Create the necessary attributes
    client_id      = None
    client_secret  = None
    redirect_uri   = None
    show_dialog    = None
    code_for_token = None
    access_token   = None
    # Create the constructor
    def __init__(   self, 
                    client_id,
                    client_secret, 
                    redirect_uri='bubu',
                    show_dialog='true'
                ):
        self.client_id     = client_id
        self.client_secret = client_secret
        self.redirect_uri  = redirect_uri
        self.show_dialog   = show_dialog

    # Method to get url authorization
    def get_auth_url(self, scopes=''):
        # Create the endpoint and the query 
        # parameters for the get request.
        endpoint         = 'https://accounts.spotify.com/authorize'
        query_parameters = {
            'client_id'    : self.client_id,
            'response_type': 'code',
            'redirect_uri' : self.redirect_uri,
            'show_dialog'  : self.show_dialog
        }
        # If no scopes passed then the api
        # only will be able to access public info.
        if scopes:
            query_parameters['scope'] = ','.join(scopes)
        # Requesting get for authorization.
        r = requests.get(
            endpoint, 
            params=query_parameters
        )
        return r.url
        
    # Method to get the token
    def set_token(self):
        # Create the endpoint, query parameters and headers
        endpoint         = 'https://accounts.spotify.com/api/token'
        query_parameters = {
            'grant_type'   : 'authorization_code',
            'code'         : self.code_for_token,
            'redirect_uri' : self.redirect_uri
        }
        # For the headers we need to encode base 64 the client_id
        # and the client_secret
        client_credentials = f'{self.client_id}:{self.client_secret}'
        client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()
        headers = {
            'Authorization' : f'Basic {client_credentials_b64}'
        }
        # Make the post call
        r = requests.post(
            endpoint, 
            data=query_parameters, 
            headers=headers
        )
        # Store token
        response = r.json()
        self.access_token = response['access_token']
        # I am not going to implement the refresh thing
        # nor the 'expires' thing. Not usefull for this project.
        return 

    def get_headers_authorization(self):
        return {
            'Accept'       : 'application/json',
            'Content-Type' : 'application/json',
            'Authorization': f'Bearer {self.access_token}' 
        }
    
    def check_and_format(self, tracks, key_names):
        # If not key names given, return all the data
        if not key_names:
            print('no key names')
            return tracks
        # Filter track keys value pairs
        track_list = []
        for track in tracks:
            track_list.append(
                { key:value for (key, value) in track.items() if key in key_names}
            )
        # Change the id key because of the databse problematic
        for track in track_list:
            track['track_id'] = track.pop('id')
        # Give format for artists field (for now, just the names)
        if 'artists' not in key_names:
            return track_list
        for track in track_list:
            artists_list = []
            for artist in track['artists']:
                artists_list.append(artist['name'])
            track['artists'] = artists_list

        return track_list

    def get_top_tracks_or_artists(self, key_names = '', type='tracks', time_range='medium_term',limit=50, offset=0):
        # Define endpoint, headers and query parameters
        endpoint = f'https://api.spotify.com/v1/me/top/{type}?'
        headers = self.get_headers_authorization()
        query_parameters = {
            'time_range': time_range,
            'limit'     : str(limit),
            'offset'    : str(offset * limit)
        }
        # Make the get call with all parameters
        r = requests.get(
            endpoint, 
            params=query_parameters, 
            headers=headers
        )
        # Catching an error
        if not r.status_code in range(200, 209):
            print(r.status_code)
            print(r.text)
            raise Error('Hey hey heeey, amon vacations')
        # Get the items in a json way
        tracks = r.json()['items']
        # Format
        return self.check_and_format(tracks, key_names)

    def get_recent_tracks(self, limit=50, after='', before='', key_names=''):
        # Define the endpoint, headers, query parameters.
        endpoint = 'https://api.spotify.com/v1/me/player/recently-played?'
        headers = self.get_headers_authorization()
        query_parameters = {
            'limit': limit
        }
        # In case of after or before
        # You can not call both of them
        if after:
            query_parameters['after'] = after
        elif before:
            query_parameters['before'] = before
        # Make the get call for the json
        r = requests.get(
            endpoint, 
            params=query_parameters,
            headers=headers
        )
        # Catching an error
        if not r.status_code in range(200, 209):
            print(r.status_code)
            print(r.text)
            raise Error('Hey hey heeey, amon vacations')
        # Get the items in a json way
        json_items = r.json()['items']
        # Filter the items, we just want the track object
        tracks = []
        for item in json_items:
            tracks.append(item['track'])
        # Format and handling errors
        return self.check_and_format(tracks, key_names)                

# Create function for testing
if __name__ == '__main__':
    # Import test things
    from decouple import config
    import webbrowser
    import json
    # Get keys
    client_id     = config('SPOTIFY_CLIENT_ID')
    client_secret = config('SPOTIFY_CLIENT_SECRET')
    redirect_uri  = config('SPOTIFY_REDIRECT_URI')
    # Create spotify bubu api object for testing
    spotify = SpotifyBubuApi(client_id,client_secret,redirect_uri)
    # Define scopes
    scopes = ['user-top-read', 'user-read-recently-played']
    # Authorization test
    url = spotify.get_auth_url(scopes=scopes)
    webbrowser.open(url)
    # Wait for the response
    input('Hello: ')
    # Get the code
    f = open('code.txt', 'r')
    code = f.read()
    if not code:
        raise Error('Not code bro...')
    spotify.code_for_token = code
    # Request and set the token
    spotify.set_token()
    # Now we can access spotify data like top tracks
    # and recently tracks for this user.
    ### Top Tracks part ###
    # Valid time range are long_term, medium_term and short_term 
    top_tracks_json = spotify.get_top_tracks_or_artists(
        type        = 'tracks',
        time_range  = 'short_term',
        limit       = 0,
        key_names   = ['name', 'artists', 'id', 'uri']
    )
    ### Recently played part ###
    recently_tracks = spotify.get_recent_tracks(
        limit       = 1,
        key_names   = ['name', 'artists', 'id', 'uri']
    )

    # Done
    print('Everything is done')