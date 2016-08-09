import sys
import spotipy
import spotipy.util as util

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
    album_results = sp.current_user_followed_artists(limit=50)

    # total_available = new_release_results['artists']['items']['total']
    # num_results = new_release_results['artists']['limit']

    # new_release_artist_ids = []
    # for i in range(20):
    #     new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
    #     # album_ids_joined = ','.join(new_release_album_ids)
else:
    print "Can't get token for", username
