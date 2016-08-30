import os
import sys
import spotipy
import spotipy.util as util
from math import ceil
import unidecode

################################################################################
# # Authentication and Token Process
# scope = 'user-follow-read user-read-private playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
# token = spotipy.util.prompt_for_user_token('jas0njames', scope=scope)

################################################################################

complete_new_release_album_ids = [] 
fixed_20_new_release_album_ids = []
new_release_artist_ids = []
user_followed_artists_ids = []
final_album_list = []
user_playlist_list_of_dict = []

def get_api_data(token):
################################################################################
# Gets the first 20 album ids from the Spotify new release list in order to get 
# the artist ids

    def get_num_results_and_offsets(token):
        """Returns total number of Spotify new release albums and times to offset."""
        
        if token: 
            print "The token exists!"
            sp = spotipy.Spotify(auth=token)
            new_release_results = sp.new_releases(limit=20)
            total_available = new_release_results['albums']['total']
            num_results = len(new_release_results['albums']['items'])
            times_to_offset = int(ceil(total_available/float(num_results)))
            return {'sp': sp, 'num_results': num_results, 'times_to_offset': times_to_offset}
        else:
            print "NO TOKEN"

    num_results_and_offset = get_num_results_and_offsets(token)
    num_results = num_results_and_offset['num_results']
    times_to_offset = num_results_and_offset['times_to_offset']
    sp = num_results_and_offset['sp']


    def get_new_release_artist_ids(sp, times_to_offset, num_results):
            offset = (times_to_offset*2)
            for i in range(0, offset, 2):
                fixed_20_new_release_album_ids = []
                new_release_results2 = sp.new_releases(limit=20, offset=(i*10))
                for i in range(num_results):
                    complete_new_release_album_ids.append(str(new_release_results2['albums']['items'][i]['id']))
                    fixed_20_new_release_album_ids.append(str(new_release_results2['albums']['items'][i]['id']))
                album_results = sp.albums(fixed_20_new_release_album_ids)
                for i in range(len(album_results['albums'])):
                    new_release_artist_ids.append(str(album_results['albums'][i]['artists'][0]['id']))       

    get_new_release_artist_ids(sp, times_to_offset, num_results)


    def get_first_50_user_artist_ids(sp):
        """Gets first 50 artist ids user follows and figures number times to query."""

        first_artist_followed_results = sp.current_user_followed_artists(limit=50)

        total_artists_user_follows = float(first_artist_followed_results['artists']['total'])
        num_results = len(first_artist_followed_results['artists']['items'])
        num_to_loop = int(ceil(total_artists_user_follows / float(num_results)) - 1)

        for i in range(num_results):
            user_followed_artists_ids.append(str(first_artist_followed_results['artists']['items'][i]['id']))

        return num_to_loop

    num_to_loop = get_first_50_user_artist_ids(sp)


    def get_rest_user_artist_ids(sp, num_to_loop):
        """Gets the rest / entire list of Spotify user's followed artist ids. """

        for i in range(num_to_loop):
            artists_user_follows_results = sp.current_user_followed_artists(limit=50, 
                                                    after=user_followed_artists_ids[-1])
            for i in range(len(artists_user_follows_results['artists']['items'])):
                user_followed_artists_ids.append(str(artists_user_follows_results['artists']['items'][i]['id']))

    get_rest_user_artist_ids(sp, num_to_loop)


    ############################################################################


    def get_final_album_list_of_tuples(complete_new_release_album_ids, new_release_artist_ids):
        """Gets a final list of new release albums by artists the user follows."""

        """Compares New Release artist id to User followed artist ids and deletes 
        the tuples (of album ids, artist ids) that do not share artist ids with 
        the user, resulting in a final album list of tuples (album_ids, artist_ids)."""

        tuple_album_id_artist_id_list = zip(complete_new_release_album_ids, new_release_artist_ids)
        set_of_user_followed_artists_ids = set(user_followed_artists_ids)

        for item in tuple_album_id_artist_id_list:
            if item[1] in set_of_user_followed_artists_ids:
                final_album_list.append(item)

    get_final_album_list_of_tuples(complete_new_release_album_ids, new_release_artist_ids)


    ############################################################################
    #Helper Functions

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


    ############################################################################

    def get_album_info_list_of_dict(final_album_list, sp):
        """Get all info for each new release album by artists a user follows."""

        """Takes the final_album_list produced from the above step and loops 
        through the list 20 at a time to retrieve the album info for each item. """

        unzipped = zip(*final_album_list)
        album_ids = list(unzipped[0])
        artist_ids = list(unzipped[1])
        #calculates the number of times to loop through the list
        loop_thru = int(ceil(float(len(album_ids)) / 20.0)) 
        album_info_list_of_dict = []

        for i in range(loop_thru):
            album_info_results = sp.albums(album_ids[0:20])
            del album_ids[:20]
            for i in range(len(album_info_results['albums'])):
                current = {}
                current['album_id'] = album_info_results['albums'][i]['id']
                current['album_name'] = special_char(album_info_results['albums'][i]['name'])
                current['album_link'] = str(album_info_results['albums'][i]['external_urls']['spotify'])
                current['album_art_300'] = str(album_info_results['albums'][i]['images'][1]['url'])
                current['artist_id'] = album_info_results['albums'][i]['artists'][0]['id']
                current['artist_name'] = special_char(album_info_results['albums'][i]['artists'][0]['name'])
                current['artist_sorted_name'] = move_the(special_char(album_info_results['albums'][i]['artists'][0]['name']))
                current['artist_link'] = str(album_info_results['albums'][i]['artists'][0]['external_urls']['spotify'])
                #gets a list of album track URIs
                num_of_tracks = len(album_info_results['albums'][i]['tracks']['items'])
                list_of_current_album_track_uris = []
                for x in range(num_of_tracks):
                    list_of_current_album_track_uris.append(str(album_info_results['albums'][i]['tracks']['items'][x]['uri']))
                current['album_tracks_uris'] = list_of_current_album_track_uris
                album_info_list_of_dict.append(current)

        return album_info_list_of_dict

    album_info_list_of_dict = get_album_info_list_of_dict(final_album_list, sp)  
    

    ############################################################################
    # #get current user's Spotify user_id

    def get_user_id(sp):
        """Get user's Spotify user id."""

        user_profile_results = sp.current_user() 
        user_id = str(user_profile_results['id'])
        return user_id

    user_id = get_user_id(sp)

    ############################################################################
    # gets first round of user's playlist ids & names
    def get_users_playlist_info(sp):
        """Get a list of playlist dictionaries with playlist name and id."""

        #Spotify's max limit of playlist returns is 50
        user_playlists_results = sp.user_playlists(user_id, limit=50)  

        total_available = user_playlists_results['total']
        num_results = len(user_playlists_results['items'])
        #Maxiumum offset in Spotify for this endpoint is 100
        times_to_offset = int(ceil(float(total_available)/float(num_results)) - 1)  

        for i in range(num_results):
            current = {}
            current['user_playlist_id'] = str(user_playlists_results['items'][i]['id'])
            current['user_playlist_name'] = str(user_playlists_results['items'][i]['name'])
            user_playlist_list_of_dict.append(current)
        #Maxiumum offset in Spotify for this endpoint is 100; so maximum loops to offset is 2 times
        if times_to_offset > 2:
                times_to_offset = 2
        if times_to_offset > 0:
            #Maxiumum offset in Spotify for this endpoint is 100; so maximum loops to offset is 2 times       
            offset = len(range(times_to_offset)) * 50
            for i in range(times_to_offset):
                #Maxiumum offset in Spotify for this endpoint is 100; so maximum loops to offset is 2 times
                user_playlists_results = sp.user_playlists(user_id, limit=50, offset=offset)
                num_results = len(user_playlists_results['items'])
                for i in range(num_results):
                    current = {}
                    current['user_playlist_id'] = str(user_playlists_results['items'][i]['id'])
                    current['user_playlist_name'] = str(user_playlists_results['items'][i]['name'])
                    user_playlist_list_of_dict.append(current)

    get_users_playlist_info(sp)

    #############################################################################

    spotify_api_dict = {
    'album_info': album_info_list_of_dict,
    'playlist_info': user_playlist_list_of_dict,
    'user_id': user_id}

    return spotify_api_dict

# spotify_api_dict = get_api_data(token)



















