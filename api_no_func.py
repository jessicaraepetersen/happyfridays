import os
import sys
import spotipy
import spotipy.util as util
from math import ceil
import unidecode

scope = 'user-follow-read user-read-private playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

# # # # if len(sys.argv) > 1:
# # # #     username = sys.argv[1]
# # # # else:
# # # #     print "Usage: %s username" % (sys.argv[0],)
# # # #     sys.exit()

# # # # token = util.prompt_for_user_token(username, scope)

token = spotipy.util.prompt_for_user_token('jessmontalbano', scope=scope)



complete_new_release_album_ids = [] 
fixed_20_new_release_album_ids = []
new_release_artist_ids = []


# def get_api_data(token):
################################################################################
# Gets the first 20 album ids from the Spotify new release list in order to get 
# the artist ids

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
else:
    print "NO TOKEN"


################################################################################
# Takes the album ids from above and gets the corresponding 20 artist ids from 
# Spotify API

if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    album_results = sp.albums(complete_new_release_album_ids)

    new_release_artist_ids = []
    for i in range(len(album_results['albums'])):
        new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))

else:
    print "NO TOKEN"


################################################################################
#gets the rest of the album ids from the new release list
#and takes the album ids from above and gets the rest of the corresponding artist ids
#assumes the Spotify New Release list is larger than 20

if token:
    print "The token exists!"
    offset = (times_to_offset*2+2)
    for i in range(2, offset, 2):
        fixed_20_new_release_album_ids = []
        sp = spotipy.Spotify(auth=token)
        new_release_results2 = sp.new_releases(limit=20, offset=(i*10))
        for i in range(num_results):
            complete_new_release_album_ids.append(str(new_release_results2['albums']['items'][i]['id']))
            fixed_20_new_release_album_ids.append(str(new_release_results2['albums']['items'][i]['id']))
        if token:
            print "The token exists!"
            sp = spotipy.Spotify(auth=token)
            album_results = sp.albums(fixed_20_new_release_album_ids)
            for i in range(len(album_results['albums'])):
                new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))
            
else:
    print "NO TOKEN"


################################################################################
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

else:
    print "NO TOKEN"

################################################################################
#Gets the rest of the artist ids that the user follows

for i in range(num_to_loop):
    if token:
        print "The token exists!"
        sp = spotipy.Spotify(auth=token)
        artists_user_follows_results = sp.current_user_followed_artists(limit=50, 
                                                after=user_followed_artists_ids[-1])

        for i in range(len(artists_user_follows_results['artists']['items'])):
            user_followed_artists_ids.append(str(artists_user_follows_results['artists']['items'][i]['id']))

    else:
        print "NO TOKEN"

################################################################################
# compares New Release artist id to User followed artist ids and deletes the
# tuples (of album ids, artist ids) that do not share artist ids with the user,
# resulting in a final album list of tuples (album_ids, artist_ids).

tuple_album_id_artist_id_list = zip(complete_new_release_album_ids, new_release_artist_ids)
final_album_list = []
set_of_user_followed_artists_ids = set(user_followed_artists_ids)

for item in tuple_album_id_artist_id_list:
    if item[1] in set_of_user_followed_artists_ids:
        final_album_list.append(item)


################################################################################
# Helper Function

def special_char(results):
    '''Turns special characters in unicode into normal character string.'''

    '''This function checks to see if the unicode from the Spotify API can be
    turned into a string. If the error UnicodeEncodeError occurs, the function
    turns the special characters in the unicode into a string of normal 
    characters. This function is used in the code block below when querying the 
    Spotify API for the album names and the artist names, which will be displayed 
    to the user.'''
    try:
        str(results)
    except UnicodeEncodeError:
        results = unidecode.unidecode(results)
    return results


def move_the(results):
    '''Removes "The " from beginning of string and appends to the end with comma.'''

    '''This function checks the Spotify API album names for a "The " (including 
    a space at the end of "The ") and removes "The " from the beginning of the
    string and appends ", The" to the end of the string (along with a comma).'''

    if results[:4] == "The ":
        new_results = results[4:]
        new_results += ", The"
        return new_results
    else:
        return results


################################################################################
# Takes the final_album_list produced from the above step and loops through the list
# 20 at a time to retrieve the album info for each item.

if token:
    print "The token exists!"
    unzipped = zip(*final_album_list)
    album_ids = list(unzipped[0])
    artist_ids = list(unzipped[1])
    #calculates the number of times to loop through the list
    loop_thru = int(ceil(float(len(album_ids)) / 20.0))  
    album_names = []
    album_art_300 = []
    album_links = []
    artist_names = []
    artist_sorted_names = []
    artist_links = []
    album_track_uris = []
    for i in range(loop_thru):
        sp = spotipy.Spotify(auth=token)
        album_info_results = sp.albums(album_ids[0:20])
        del album_ids[:20]
        for i in range(len(album_info_results['albums'])):
            album_names.append(special_char(album_info_results['albums'][i]['name']))
            album_links.append(str(album_info_results['albums'][i]['external_urls']['spotify']))
            album_art_300.append(str(album_info_results['albums'][i]['images'][1]['url']))
            artist_names.append(special_char(album_info_results['albums'][i]['artists'][0]['name']))
            artist_sorted_names.append(move_the(special_char(album_info_results['albums'][i]['artists'][0]['name'])))
            artist_links.append(str(album_info_results['albums'][i]['artists'][0]['external_urls']['spotify']))
            #gets a list of album track URIs
            num_of_tracks = len(album_info_results['albums'][i]['tracks']['items'])
            list_of_current_album_track_uris = []
            for x in range(num_of_tracks):
                list_of_current_album_track_uris.append(str(album_info_results['albums'][i]['tracks']['items'][x]['uri']))
            album_track_uris.append(list_of_current_album_track_uris)

else:
    print "NO TOKEN"


################################################################################
#get current user's Spotify user_id
if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    user_profile_results = sp.current_user() 
    user_id = str(user_profile_results['id'])
else:
    print "NO TOKEN"

################################################################################
# gets first round of user's playlist ids & names
if token:
    print "The token exists!"
    sp = spotipy.Spotify(auth=token)
    #Spotify's max limit of playlist returns is 50
    user_playlists_results = sp.user_playlists(user_id, limit=50)  

    total_available = user_playlists_results['total']
    num_results = len(user_playlists_results['items'])
    #Maxiumum offset in Spotify for this endpoint is 100
    times_to_offset = int(ceil(float(total_available)/float(num_results)) - 1)  

    user_playlist_ids = [] 
    user_playlist_names = []
    for i in range(num_results):
        user_playlist_ids.append(str(user_playlists_results['items'][i]['id']))
        user_playlist_names.append(str(user_playlists_results['items'][i]['name']))
    #Maxiumum offset in Spotify for this endpoint is 100; so maximum loops to offset is 2 times
    if times_to_offset > 2:
            times_to_offset = 2
    if times_to_offset > 0:
        #Maxiumum offset in Spotify for this endpoint is 100; so maximum loops to offset is 2 times       
        offset = len(range(times_to_offset)) * 50
        for i in range(times_to_offset):
            sp = spotipy.Spotify(auth=token)
            #Maxiumum offset in Spotify for this endpoint is 100; so maximum loops to offset is 2 times
            user_playlists_results = sp.user_playlists(user_id, limit=50, offset=offset)
            num_results = len(user_playlists_results['items'])
            for i in range(num_results):
                user_playlist_ids.append(str(user_playlists_results['items'][i]['id']))
                user_playlist_names.append(str(user_playlists_results['items'][i]['name']))

else:
    print "NO TOKEN"

###########################################################################
# Creates a dictionary of all the API data needed to seed the database.
# Final album list is a final list of tuples (album_ids, artist_ids) that 
# represent a new album release by an artists that the user follows.

# gets only the album_ids
unzipped = zip(*final_album_list)
album_ids = list(unzipped[0])

album_info_dict = {
    'album_ids': album_ids,
    'album_names': album_names,
    'album_links': album_links,
    'album_art': album_art_300,
    'album_track_uris': album_track_uris,
    'artist_ids': artist_ids,
    'user_playlist_ids': user_playlist_ids,
    'user_playlist_names': user_playlist_names,
    'user_id': user_id
}

############################################################################
# Helper Function

def remove_duplicates(values):
    """This function removes duplicates from a list, using set, without 
    changing the order of the items in the original list.
    Because Artist will be its own table in SQL / model, there should not be 
    duplicate artists; though, there theoretically would be if the same 
    artist released multiple albums or singles."""

    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


artist_ids_no_duplicates = remove_duplicates(artist_ids)
artist_names = remove_duplicates(artist_names)
artist_sorted_names = remove_duplicates(artist_sorted_names)
artist_links = remove_duplicates(artist_links)


############################################################################
# Add artist info to album info dict

album_info_dict['artist_ids_no_duplicates'] = artist_ids_no_duplicates
album_info_dict['artist_names'] = artist_names
album_info_dict['artist_sorted_names'] = artist_sorted_names
album_info_dict['artist_links'] = artist_links

    # return album_info_dict

# album_info_dict = get_api_data(token)


