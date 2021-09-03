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
scopes = ['user-top-read', 'user-read-recently-played']


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
    # Set up default user_info
    if 'user_info' not in session:
        session['user_info'] = ''
    # Get the url for authorization
    spotify_auth_url = spotify.get_auth_url(scopes)
    # Create the context to pass it to the page
    context = {
        'page_title'      : 'Welcome!',
        'spotify_auth_url': spotify_auth_url,
        'user_info'       : session['user_info']
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
    # Get user information
    user_info = spotify.get_user_profile()
    session['user_info'] = {
            'username'  : user_info['display_name'],
            'spotify_id'   : user_info['id'],
            'user_image': user_info['images'][0]['url']
        }

    # Redirect to the track page
    return redirect('/')

@app.route('/songs-page/<type>/')
@app.route('/songs-page/<type>/<term>')
def songs_page_method(type='', term=''):
    """
    This view will display 50 top songs of this user
    only if the user has played at least 50 songs on 
    his/her spotify account.
    """
    # Check if the user is login and get into the right url
    if 'user_info' not in session or not type:
        redirect('/')
    # Display the correct information
    if type == 'top':
        songs = spotify.get_top_tracks_or_artists(
            key_names   = ['name', 'artists', 'id', 'uri','album']
        )
    elif type == 'recent':
        songs = spotify.get_recent_tracks(
            key_names   = ['name', 'artists', 'id', 'uri','album']
        )
    else:
        redirect('/')

    # Check if some error with the token
    if isinstance(songs, bool):
        return redirect('/logout')
    # Define the context to pass to.
    context = {
        'page_title': 'Your Songs!',
        'songs'     : songs,
        'user_info' : session['user_info']
    }
    # Render the template with 50 songs
    return render_template('song_view.html', context=context)

@app.route('/logout')
def logout_method():
    if session['user_info']:
        session.pop('user_info')
    
    return redirect('/')

# # This is a route for testing the spotify module
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