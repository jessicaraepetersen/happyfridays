"""Utility file to seed albums database from Spotify API data in api"""

from sqlalchemy import func
from model import User, Album, Artist, UserAlbum, Playlist, Track, connect_to_db, db
# from server import app



def load_users(spotify_api_dict):
    """Load Spotify Users from spotify_api_dict into database."""

    user_id = spotify_api_dict['user_id']
    if db.session.query(User).filter_by(user_id=user_id).scalar() is not None:
        pass
    else:
        user = User(user_id=user_id)
        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, commit the work
    db.session.commit()



def load_artists(spotify_api_dict):
    """Load artists from spotify_api_dict into database."""

    for i in range(len(spotify_api_dict['album_info'])):
        artist_id = spotify_api_dict['album_info'][i]['artist_id']
        if db.session.query(Artist).filter_by(artist_id=artist_id).scalar() is not None:
            pass
        else:
            artist_name = spotify_api_dict['album_info'][i]['artist_name']
            artist_sorted_name = spotify_api_dict['album_info'][i]['artist_sorted_name']
            link_to_artist = spotify_api_dict['album_info'][i]['artist_link']


            artist = Artist(artist_id=artist_id,
                          artist_name=artist_name,
                          artist_sorted_name=artist_sorted_name,
                          link_to_artist=link_to_artist)

            # We need to add to the session or it won't ever be stored
            db.session.add(artist)

    # Once we're done, we should commit our work
    db.session.commit()


def load_albums(spotify_api_dict):
    """Load albums from spotify_api_dict into database."""

    for i in range(len(spotify_api_dict['album_info'])):
        album_id = spotify_api_dict['album_info'][i]['album_id']
        if db.session.query(Album).filter_by(album_id=album_id).scalar() is not None:
            pass
        else:
            album_name = spotify_api_dict['album_info'][i]['album_name']
            link_to_album = spotify_api_dict['album_info'][i]['link_to_album']
            album_art = spotify_api_dict['album_info'][i]['album_art_300']
            artist_id = spotify_api_dict['album_info'][i]['artist_id']

            album = Album(album_id=album_id,
                        album_name=album_name,
                        link_to_album=link_to_album,
                        album_art=album_art,
                        artist_id=artist_id)

            # We need to add to the session or it won't ever be stored
            db.session.add(album)

    # Once we're done, we should commit our work
    db.session.commit()


def load_users_albums(spotify_api_dict):
    """Load users_albums from spotify_api_dict into database."""

    # user_album_id = FIX ME FIX ME FIX ME FIX ME FIX ME FIX ME
    user_id = spotify_api_dict['user_id']
    for i in range(len(spotify_api_dict['album_info'])):
        album_id = spotify_api_dict['album_info'][i]['album_id']

        user_album = UserAlbum(user_id=user_id, album_id=album_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(user_album)

    # Once we're done, we should commit our work
    db.session.commit()



def load_playlists(spotify_api_dict):
    """Load playlists from spotify_api_dict into database."""

    user_id = spotify_api_dict['user_id']
    for i in range(len(spotify_api_dict['playlist_info'])):
        playlist_id = spotify_api_dict['playlist_info'][i]['user_playlist_id']
        if db.session.query(Playlist).filter_by(playlist_id=playlist_id).scalar() is not None:
            pass
        else:
            playlist_name = spotify_api_dict['playlist_info'][i]['user_playlist_name']

            playlist = Playlist(playlist_id=playlist_id,
                            playlist_name=playlist_name,
                            user_id=user_id)

            # We need to add to the session or it won't ever be stored
            db.session.add(playlist)

    # Once we're done, we should commit our work
    db.session.commit()


def load_tracks(spotify_api_dict):
    """Load album track uris from spotify_api_dict into database."""

    for i in range(len(spotify_api_dict['album_info'])):
        album_id = spotify_api_dict['album_info'][i]['album_id']
        for n in range(len(spotify_api_dict['album_info'][i]['album_tracks_uris'])):
            album_track_uri = spotify_api_dict['album_info'][i]['album_tracks_uris'][n]
            if db.session.query(Track).filter_by(album_track_uri=album_track_uri).scalar() is not None:
                pass
            else:
                track = Track(album_track_uri=album_track_uri,
                                    album_id=album_id)
                # We need to add to the session or it won't ever be stored
                db.session.add(track)

    # Once we're done, we should commit our work
    db.session.commit()



def fill_db(spotify_api_dict):
    load_users(spotify_api_dict)
    load_artists(spotify_api_dict)
    load_albums(spotify_api_dict)
    load_users_albums(spotify_api_dict)
    load_playlists(spotify_api_dict)
    load_tracks(spotify_api_dict)
    


if __name__ == "__main__":
    connect_to_db(app)
    # db.create_all()




