import sys
import spotipy
import spotipy.util as util
from math import ceil
import test2

scope = 'user-follow-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope) 

if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    first_artist_followed_results = sp.current_user_followed_artists(limit=50)

    total_artists_user_follows = float(first_artist_followed_results['artists']['total'])
    num_results = float(first_artist_followed_results['artists']['limit'])
    num_to_loop = int(ceil(total_artists_user_follows / num_results) - 1)

    user_followed_artists_ids = []
    for i in range(len(first_artist_followed_results['artists']['items'])):
        user_followed_artists_ids.append(str(first_artist_followed_results['artists']['items'][i]['id']))

        # album_ids_joined = ','.join(new_release_album_ids)
else:
    print "Can't get token for", username

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

















