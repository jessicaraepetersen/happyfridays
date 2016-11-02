# from jinja2 import StrictUndefined
import os # To access my OS environment variables, specifically spotify client id
import requests
import fill
from flask import Flask, render_template, render_template_string, request, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Artist, Album, UserAlbum, Playlist, Track
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import spotipy
from api import ApiData


# prevents a non-essential warning
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# sets up my Flask app
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ABC")
app.jinja_env.auto_reload = True

#grabs my Spotify Client ID & Secret from my secret.sh file
client_id=os.getenv('SPOTIPY_CLIENT_ID')
client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI')
# the Spotify scope authorization for the user
scope = 'user-follow-read user-read-private playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

# use Spotipy python library to instantiate api as an instance of SpotifyOAuth class
api = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
client_credentials_manager = SpotifyClientCredentials()


@app.route('/')
def index():
    """Homepage where user clicks to auth their Spotify account."""
    # uses Spotipy method to construct the auth url
    url1 = api.get_authorize_url()
    url = url1+'&show_dialog=true'

    return render_template("index.html", url=url)



@app.route('/callback')
def callback():
    """Authorizes the user and get token."""

    # Grab code from Spotify, exchange code for token and store in session
    code = request.args.get('code')
    if code:
        token_info = api.get_access_token(code)
        session['token_info'] = token_info
        token = str(token_info['access_token'])
        session['token'] = token
        refresh_token = token = str(token_info['refresh_token'])
        session['refresh_token'] = refresh_token
        return render_template('building.html')
    else:
        return redirect('/')


@app.route('/list')
def list():
    """List of new release albums by artists the user follows."""

    # if no token, redirect to home
    if 'token' not in session:
        return redirect('/')
    # store token in sesssion
    token = session['token']
    refresh_token = session['refresh_token']
    token_info = session['token_info']

    if not api._is_token_expired(token_info):
        sp = spotipy.Spotify(auth=token)
        user_profile_results = sp.current_user()
        user_id = str(user_profile_results['id'])
        # if album list is built, prevents rebuilding on refresh for user; however,
        # list will rebuild for new / different users even if built for others
        if session.get(user_id + '_albums_done'):
            pass
        else:
            #create an instance of the ApiData class in api module passing in token
            #to query the Spotify API for data
            spotify_api_data = ApiData(token)
            #use the get_Spotify_data method to get dictionary
            spotify_api_dict = spotify_api_data.get_Spotify_data()
            # Checks whether user is following any artists
            if spotify_api_dict:
                #if the user is, fill db and model with data
                fill.fill_db(spotify_api_dict)
                session['user_id'] = spotify_api_dict['user_id']
                # alerts the session album list is built
                session[user_id + '_albums_done'] = True
            else:
                #otherwise, alert the user to follow some artists
                return render_template('no-albums.html')
    else:
        print '-----TOKEN EXPIRED------'
        token_info = api._refresh_access_token(refresh_token)
        print token_info
        session['token_info'] = token_info
        token = str(token_info['access_token'])
        session['token'] = token
        refresh_token = str(token_info['refresh_token'])
        session['refresh_token'] = refresh_token
        print '-----NEW TOKEN------'

    user_id = session['user_id']
    # query SQL db for albums to fill album cards and playlists for add to playlist button
    albums = db.session.query(Album).join(Album.artists).join(Album.users_albums).filter_by(user_id=user_id).order_by(Artist.artist_sorted_name).all()
    playlists = db.session.query(Playlist).join(Playlist.users).filter_by(user_id=user_id).order_by(Playlist.playlist_name).all()

    are_there_playlists = True
    if not playlists:
        are_there_playlists = False

    return render_template("list.html", albums=albums, playlists=playlists,
                                        are_there_playlists=are_there_playlists)



@app.route('/clear')
def clear():
    """Clears flask session and SQL tables once user is done ."""

    session.clear()
    db.session.query(Track).delete()
    db.session.query(Playlist).delete()
    db.session.query(UserAlbum).delete()
    db.session.query(Album).delete()
    db.session.query(Artist).delete()
    db.session.query(User).delete()
    db.session.commit()
    print "------User's session & data cleared from DB------"
    return redirect('/')



@app.route('/add-to-playlist', methods=['POST'])
def add_to_playlist():
    """Add album to user's Spotify playlist from dropdown menu."""

    token = session['token']
    user_id = session['user_id']
    playlist_id = request.form.get('playlist_id')
    album_id = request.form.get('album_id')


    # Query SQL db for track URIs, which are needed to add entire album to playlist
    tracks = db.session.query(Track).join(Track.albums).filter_by(album_id=album_id).all()
    list_of_track_uris = []

    for track in tracks:
        list_of_track_uris.append(track.album_track_uri)
    # uses the Spotipy method to add album to Spotify user's playlist
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.user_playlist_add_tracks(user_id, playlist_id, list_of_track_uris)
    #The user selects a playlist to add an album to. This queries the name of the
    # playlist to include in the flash-like message.
    playlist = Playlist.query.filter_by(playlist_id=playlist_id).one()
    playlist_name = str(playlist.playlist_name)
    #The user selects a playlist to add an album to. This queries the name of the
    # album to include in the flash-like message.
    album = Album.query.filter_by(album_id=album_id).one()
    album_name = album.album_name
    # return playlist_name and album_name for flash-like message
    return jsonify({'playlist_name': playlist_name, 'album_name': album_name})


@app.route('/no-albums')
def no_artists():
    """Alerts the user to follow more artists."""

    return render_template('no-albums.html')



if __name__ == "__main__":
    # Set debug=True here since it has to be True at the point
    # that I invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # This port works for deployed heroku site:
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ


    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)

