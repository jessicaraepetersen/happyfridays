import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

#Gets the first 20 album ids from the Spotify new release list
if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    new_release_results = sp.new_releases(limit=20)

    total_available = new_release_results['albums']['total']
    num_results = new_release_results['albums']['limit']
    times_to_offset = (total_available/num_results) - 1

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
    for i in range(20):
        new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
        # album_ids_joined = ','.join(new_release_album_ids)
else:
    print "Can't get token for", username

#Gets the first 50 artists a user follows

# scope = 'user-follow-read'
# token = util.prompt_for_user_token(username, scope)

# if token:
#     print "The token exists!"
#     sp = spotipy.Spotify(auth=token)
#     album_results = sp.current_user_followed_artists(limit=50)

#     total_available = new_release_results['artists']['items']['total']
#     num_results = new_release_results['artists']['limit']

#     # new_release_artist_ids = []
#     # for i in range(20):
#     #     new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
#     #     # album_ids_joined = ','.join(new_release_album_ids)
# else:
#     print "Can't get token for", username












