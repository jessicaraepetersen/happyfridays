# from jinja2 import StrictUndefined
import os # To access my OS environment variables, specifically spotify client id
import requests
import fill_db
from flask import Flask, render_template, render_template_string, request, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Artist, Album, Playlist, Track
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy 
import spotipy.util as util
from api_data import get_api_data
from random import random



import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# app.jinja_env.auto_reload = True


client_id=os.getenv('SPOTIPY_CLIENT_ID')
client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI')
scope = 'user-follow-read user-read-private playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'


api = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
client_credentials_manager = SpotifyClientCredentials()


@app.route('/') 
def index():
    """Homepage."""

    url1 = api.get_authorize_url()
    url = url1+'&show_dialog=true'
 
    return render_template("index.html", url=url)

@app.route('/callback')
def callback():
    """Authorizes the user by retrieving callback url code and exchanging the 
    code for an authorization token."""

    code = request.args.get('code')
    token_info = api.get_access_token(code)
    token = str(token_info['access_token'])
    session['token'] = token
    return render_template('building.html') 


@app.route('/list')
def list():
    """List of new release albums by artists the user follows."""

    if 'token' not in session:
        return redirect('/') 

    token = session['token']

    if session.get('albumsdone'):
        pass

    else:   
        album_info_dict = get_api_data(token)
        fill_db.fill_db(album_info_dict)
        session['user_id'] = album_info_dict['user_id']
        session['albumsdone'] = True
        
    user_id = session['user_id']


    albums = db.session.query(Album).join(Album.artists).join(Album.users).filter_by(user_id=user_id).order_by(Artist.artist_sorted_name).all()

    playlists = db.session.query(Playlist).join(Playlist.users).filter_by(user_id=user_id).order_by(Playlist.playlist_name).all()

    return render_template("list.html", albums=albums, playlists=playlists)  


@app.route('/clear')
def clear():
    """Clears SQL tables."""

    # if session['userid'] != 'sklfjsdlk':
    #     return redirect('/?failure')

    db.session.query(Track).delete()
    db.session.query(Playlist).delete()
    db.session.query(Album).delete() 
    db.session.query(Artist).delete() 
    db.session.query(User).delete() 

    db.session.commit()

    return redirect('/') 



@app.route('/add-to-playlist', methods=['POST'])
def add_to_playlist():
    """Add album to playlist."""

    token = session['token']
    print '-------TOKEN--------'
    print token
    user_id = session['user_id']
    playlist_id = request.form.get('playlist_id')
    album_id = request.form.get('album_id')
    

    tracks = db.session.query(Track).join(Track.albums).filter_by(album_id=album_id).all()
    list_of_track_uris = []

    for track in tracks:
        list_of_track_uris.append(track.album_track_uri)

    if token:
        print "The token exists to add tracks to playlist!"
        sp = spotipy.Spotify(auth=token)
        sp.user_playlist_add_tracks(user_id, playlist_id, list_of_track_uris)


    playlist = Playlist.query.filter_by(playlist_id=playlist_id).all()
    playlist_name = str(playlist[0].playlist_name)

    album = Album.query.filter_by(album_id=album_id).all()
    album_name = str(album[0].album_name)

    return jsonify({'playlist_name': playlist_name, 'album_name': album_name})

   

if __name__ == "__main__":
    # Set debug=True here since it has to be True at the point
    # that I invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", port=5000)
