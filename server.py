# from jinja2 import StrictUndefined
import os # To access my OS environment variables, specifically spotify client id
import requests
import fill_db
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Artist, Album, Playlist, Track
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from api_data import get_api_data



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
    # url = "https://accounts.spotify.com/authorize/?response_type=code&show_dialog=true&client_id="+ client_id +"&redirect_uri=http://localhost:5000/callback&scope=user-follow-read%20user-read-private%20playlist-read-private%20playlist-read-collaborative%20playlist-modify-public%20playlist-modify-private"

    url1 = api.get_authorize_url()
    url = url1+'&show_dialog=true'
 
    return render_template("index.html", url=url)

@app.route('/callback')
def callback():
    """Homepage."""

    code = request.args.get('code')
    # token_info = api.get_access_token(code)
    # token = str(token_info['access_token'])
    # album_info_dict = get_api_data(token)
    # fill_db.fill_db(album_info_dict)

    # token_info = client_credentials_manager._request_access_token()
    # token_info = client_credentials_manager._add_custom_values_to_token_info(token_info)
    # is_token_expired = client_credentials_manager._is_token_expired(token_info)
    # if is_token_expired == True

    albums = db.session.query(Album).join(Album.artists).order_by(Artist.artist_sorted_name).all()

    # return render_template("connecting.html")
    return render_template("list.html", albums=albums)

# @app.route('/list')
# def list():
#     """Homepage."""



#     return render_template("list.html")

    

if __name__ == "__main__":
    # Set debug=True here since it has to be True at the point
    # that I invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", port=5000)
