def insert_user_mongo_db(collection, spotify):
    user = create_user(spotify)
    # Check if the user is in the db
    current_user = list(collection.find({"spotify_id" : user['spotify_id']}))[0]
    if(current_user):
        # Update their recent songs
        current_user     = { "spotify_id": user['spotify_id'] }
        new_recent_songs = { "$set": { "recent_songs": user['recent_songs']} }
        collection.update_one(current_user, new_recent_songs)
        print('User updated!')
    else: 
        # Insert the user in the db
        collection.insert_one(user)
        print('User created!')

def create_user(spotify):
    user_info = spotify.get_user_profile()
    top_songs_obj = spotify.get_top_tracks_or_artists(
            key_names   = ['id'],
            time_range= 'medium_term'
    )
    recent_songs_obj = spotify.get_recent_tracks(
            key_names   = ['id']
    )

    top_songs = []
    recent_songs = []
    # Transform that tracks into lists
    for top, recent in zip(top_songs_obj, recent_songs_obj):
        top_songs.append(top['track_id'])
        recent_songs.append(recent['track_id'])

    user = {
        'username'    : user_info['display_name'],
        'spotify_id'  : user_info['id'],
        'email'       : user_info['email'],
        'top_songs'   : top_songs,
        'recent_songs': recent_songs,
    }

    return user
