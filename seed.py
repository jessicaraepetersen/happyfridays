"""Utility file to seed albums database from Spotify API data in XXXXXXXXXXX"""

import datetime
from sqlalchemy import func
from api import 
from model import Album, Artist, Playlist, connect_to_db, db
from server import app


def load_albums():
    """Load albums from XXXXXXXXXXX into database."""

    print "Albums"

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

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
    """Load artists from XXXXXXXXXXX into database."""

    print "Artists"

    for i, row in enumerate(open("seed_data/u.item")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

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

    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()

        user_id, movie_id, score, timestamp = row.split("\t")

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        # We don't care about the timestamp, so we'll ignore this

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
