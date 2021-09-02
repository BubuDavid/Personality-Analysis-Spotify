# Import important imports from flask
from flask import Flask, render_template,\
                  request, \
                  session, redirect
# Import Python imports
from decouple import config

# Import from my modules
from modules.spotify_api import SpotifyBubuApi

# Get environment variables from a hidden .env file
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
# Define the spotify scopes that we want access to.
scopes = ['user-top-read']



# Init our app flask object
app = Flask(__name__)
app.secret_key = secret_key

# Define routes below
@app.route('/')
def index_method():
    """
    Index route, where all beggins. It starts with
    nothing but a page title and an url for get
    spotify authorization
    """
    # Get the url for authorization
    spotify_auth_url = spotify.get_auth_url(scopes)
    # Create the context to pass it to the page
    context = {
        'page_title'      : 'Welcome!',
        'spotify_auth_url': spotify_auth_url,
    }
    # Render the index template with the contexts variables
    return render_template('index.html', context=context)

@app.route('/spotify-callback')
def spotify_callback_method():
    """
    Spotify callback function, where spotify redirects,
    after login. This handles the token and the logic 
    behind get the spotify information.
    """
    # Get the authorization code
    spotify_code = request.args.get('code')
    # Handle errors
    if not spotify_code:
        return redirect('/error_page')
    # Set the spotify token
    spotify.code_for_token = spotify_code
    spotify.set_token()
    print(spotify.access_token)
    # Redirect to the track page
    return redirect('/songs-page')

@app.route('/songs-page')
def songs_page_method():
    """
    This view will display 50 top songs of this user
    only if the user has played at least 50 songs on 
    his/her spotify account.
    """
    recent_songs = spotify.get_top_tracks_or_artists(
        key_names   = ['name', 'artists', 'id', 'uri']
    )

    # Define the context to pass to.
    context = {
        'page_title': 'Welcome!',
        'songs'     : recent_songs
    }
    # Render the template with 50 songs
    return render_template('song_view.html', context=context)

# This is a route for testing the spotify module
# @app.route('/spotify-callback')
# def spotify_callback_method():
#     spotify_code = request.args.get('code')
#     if not spotify_code:
#         f = open('modules/code.txt', 'w')
#         f.write('')
#         f.close()
#         return redirect('/')
#     f = open('modules/code.txt', 'w')
#     f.write(spotify_code)
#     f.close()
#     return redirect('/')

# Start the app
if __name__ == '__main__':
    app.run(debug=True, port=8888)