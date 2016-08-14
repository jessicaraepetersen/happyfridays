"""Utility file to seed albums database from Spotify API data in api"""

import datetime
from sqlalchemy import func
from api import album_info_dict
from model import Album, Artist, Playlist, connect_to_db, db
from server import app


def load_albums():
    """Load albums from album_info_dict into database."""

    print "Albums"

    for i in range(len(album_info_dict['album_ids'])):
        album_id = album_info_dict['album_ids'][i]
        album_name = album_info_dict['album_names'][i]
        link_to_album = album_info_dict['album_links'][i]
        album_art = album_info_dict['album_art'][i]
        artist_id = album_info_dict['artist_ids'][i]
        # album_track_uri = album_info_dict['album_track_uris'][i]
        # #HELP QUEUE: How do I make an array as the item in the list?


        album = Album(album_id=album_id,
                    album_name=album_name,
                    link_to_album=link_to_album,
                    album_art=album_art,
                    artist_id=artist_id,
                    album_track_uri=album_track_uri)

        # We need to add to the session or it won't ever be stored
        db.session.add(album)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_artists():
    """Load artists from album_info_dict into database."""

    print "Artists"

    for i in range(len(album_info_dict['artist_ids'])):
        artist_id = album_info_dict['artist_ids'][i]
        artist_name = album_info_dict['artist_names'][i]
        link_to_artist = album_info_dict['artist_links'][i]

        artist = Artist(artist_id=artist_id,
                      artist_name=artist_name,
                      link_to_artist=link_to_artist)

        # We need to add to the session or it won't ever be stored
        db.session.add(artist)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_playlists():
    """Load playlists from u.data into database."""

    print "Playlists"

    for i in range(len(album_info_dict['user_playlist_ids'])):
        playlist_id = album_info_dict['user_playlist_ids'][i]
        playlist_name = album_info_dict['user_playlist_names'][i]

        playlist = Playlist(playlist_id=playlist_id,
                        playlist_name=playlist_name)

        # We need to add to the session or it won't ever be stored
        db.session.add(playlist)

        # provide some sense of progress
        if i % 1000 == 0:
            print i

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_albums()
    load_artists()
    load_playlists()

    db.session.commit()
