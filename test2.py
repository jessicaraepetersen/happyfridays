import sys
import spotipy
import spotipy.util as util
from math import ceil

scope = '''user-follow-read, playlist-read-private, playlist-read-collaborative, 
            playlist-modify-public, playlist-modify-private'''


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username)

#Gets the first 20 album ids from the Spotify new release list
if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    new_release_results = sp.new_releases(limit=20, offset=)

    total_available = new_release_results['albums']['total']
    num_results = len(new_release_results['albums']['items'])
    times_to_offset = int(ceil(total_available/float(num_results)) - 1)

    new_release_album_ids = []
    for i in range(num_results):
        new_release_album_ids.append(str(new_release_results['albums']['items'][i]['id']))
        # album_ids_joined = ','.join(new_release_album_ids)
else:
    print "Can't get token for", username

#Takes the album ids from above and gets the corresponding artist id

if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    album_results = sp.albums(new_release_album_ids)

    new_release_artist_ids = []
    for i in range(len(album_results['albums'])):
        new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
        # album_ids_joined = ','.join(new_release_album_ids)
else:
    print "Can't get token for", username

#Gets the first 50 artists a user follows

if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    first_artist_followed_results = sp.current_user_followed_artists(limit=50)

    total_artists_user_follows = float(first_artist_followed_results['artists']['total'])
    num_results = len(first_artist_followed_results['artists']['items'])
    num_to_loop = int(ceil(total_artists_user_follows / float(num_results)) - 1)

    user_followed_artists_ids = []
    for i in range(num_results):
        user_followed_artists_ids.append(str(first_artist_followed_results['artists']['items'][i]['id']))

        # album_ids_joined = ','.join(new_release_album_ids)
else:
    print "Can't get token for", username

#Gets the rest of the artist ids that the user follows
def fill_user_follows():
    for i in range(num_to_loop):
        if token:
            print "The token exists!"
            sp = spotipy.Spotify(auth=token)
            artists_user_follows_results = sp.current_user_followed_artists(limit=50, 
                                                    after=user_followed_artists_ids[-1])

            for i in range(len(artists_user_follows_results['artists']['items'])):
                user_followed_artists_ids.append(str(artists_user_follows_results['artists']['items'][i]['id']))

fill_user_follows()












