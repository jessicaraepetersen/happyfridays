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
    new_release_results = sp.new_releases(limit=20)

    total_available = new_release_results['albums']['total']
    num_results = len(new_release_results['albums']['items'])
    times_to_offset = int(ceil(total_available/float(num_results)) - 1)

    complete_new_release_album_ids = []
    fixed_20_new_release_album_ids = []
    for i in range(num_results):
        complete_new_release_album_ids.append(str(new_release_results['albums']['items'][i]['id']))
        fixed_20_new_release_album_ids.append(str(new_release_results['albums']['items'][i]['id']))
        # album_ids_joined = ','.join(complete_new_release_album_ids)
else:
    print "Can't get token for", username

#Takes the album ids from above and gets the corresponding 20 artist ids

if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    album_results = sp.albums(complete_new_release_album_ids)

    new_release_artist_ids = []
    for i in range(len(album_results['albums'])):
        new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
        # album_ids_joined = ','.join(complete_new_release_album_ids)
    # tuple_album_id_artist_id_list = zip(complete_new_release_album_ids, new_release_artist_ids)

else:
    print "Can't get token for", username


#gets the rest of the album ids from the new release list
#and takes the album ids from above and gets the rest of the corresponding artist ids

def get_rest_new_release():
    if token:
        print "The token exists!"
        offset = (times_to_offset*2+2)
        for i in range(2, offset, 2):
            fixed_20_new_release_album_ids = []
            sp = spotipy.Spotify(auth=token)
            new_release_results = sp.new_releases(limit=20, offset=(i*10))
            for i in range(num_results):
                complete_new_release_album_ids.append(str(new_release_results['albums']['items'][i]['id']))
                fixed_20_new_release_album_ids.append(str(new_release_results['albums']['items'][i]['id']))
                # album_ids_joined = ','.join(complete_new_release_album_ids)
            if token:
                print "The token exists!"
                sp = spotipy.Spotify(auth=token)
                album_results = sp.albums(fixed_20_new_release_album_ids)
                for i in range(len(album_results['albums'])):
                    new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
                    # album_ids_joined = ','.join(complete_new_release_album_ids)
                

    else:
        print "Can't get token for", username

get_rest_new_release()


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

        # album_ids_joined = ','.join(complete_new_release_album_ids)
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

#compares New Release artist id to User follows artists ids and deletes the
#tuples (of album ids, artist ids) that do not share artist ids with the user
tuple_album_id_artist_id_list = zip(complete_new_release_album_ids, new_release_artist_ids)
final_album_list = []
set_of_user_followed_artists_ids = set(user_followed_artists_ids)

for item in tuple_album_id_artist_id_list:
    if item[1] in set_of_user_followed_artists_ids:
        final_album_list.append(item)


# Takes the final_album_list produced from the above step and loops through the list
# 20 at a time to retrieve the album info for each item, then prints album name
# and artist name

if token:
    print "The token exists!"
    unzipped = zip(*final_album_list)
    album_ids = list(unzipped[0])
    artist_ids = list(unzipped[1])
    loop_thru = int(ceil(float(len(album_ids)) / 20.0))  #calculates the number of times to loop through the list
    album_names = []
    album_art_300 = []
    album_links = []
    artist_names = []
    artist_links = []
    for i in range(loop_thru):
        sp = spotipy.Spotify(auth=token)
        album_info_results = sp.albums(album_ids[0:20])
        del album_ids[:20]
        for x in range(len(album_info_results['albums'])):
            album_names.append(str(album_info_results['albums'][x]['name']))
            album_links.append(str(album_info_results['albums'][x]['external_urls']['spotify']))
            album_art_300.append(str(album_info_results['albums'][x]['images'][1]['url']))
            artist_names.append(str(album_info_results['albums'][x]['tracks']['items'][0]['artists'][0]['name']))
            artist_links.append(str(album_info_results['albums'][x]['artists'][0]['external_urls']['spotify']))













