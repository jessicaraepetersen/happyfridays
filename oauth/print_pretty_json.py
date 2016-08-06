"""Pretty-prints JSON file given on command-line."""

from sys import argv
from pprint import pprint
import json

# Read JSON string from filename given on command-line
json_string = open(argv[1]).read()

# Turn into Python dictionary
json_dict = json.loads(json_string)

"Pretty print" it
pprint(json_dict)

new_releases = json_dict
num_results = new_releases['albums']['limit'] 

# Get a List of New Releases: The maximum number of items to return. 
# Default: 20. Minimum: 1. Maximum: 50.  

# Get Several Albums:ids - A comma-separated list of the Spotify IDs for the 
# albums. Maximum: 20 IDs.

# Spotify's new release list contains 500 new albums, last I checked.
# however, Spotify's highest query limit for multiple albums at a time is 20 
# album ID inputs. So, it's best to search for new release list in limits of 20.
# (Spotify's highest query limit for new releases is 50). I'll need to use 
# offset of 20, 24 times



for i in range(num_results):
    album_name = new_releases['albums']['items'][i]['name']
    album_id = new_releases['albums']['items'][i]['id']
    print "%s : %s" % (album_name, album_id)

album_ids = []

for i in range(num_results):
    album_ids.append(str(new_releases['albums']['items'][i]['id']))

print album_ids

ids = ','.join(album_ids)