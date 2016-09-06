"""Models and database functions for HappyFridays project."""

# Suppresses InsecureRequestWarning: Unverified HTTPS request is being made in Python2.6
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; I'm getting this through
# the Flask-SQLAlchemy helper library. On this, I can find the `session`
# object, where I'll do some of my interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """Info of User of HappyFridays website."""

    __tablename__ = "users"

    user_id = db.Column(db.String(50), primary_key=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s>" % (self.user_id)



class Artist(db.Model):
    """Artist of HappyFridays website."""

    __tablename__ = "artists"

    artist_id = db.Column(db.String(50), primary_key=True, unique=False)
    artist_name = db.Column(db.String(100), nullable=False)
    artist_sorted_name = db.Column(db.String(100), nullable=False)
    link_to_artist = db.Column(db.String(60), nullable=False)
    
    # # Define relationship to Album
    albums = db.relationship('Album')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artist artist_id=%s artist_name=%s>" % (self.artist_id, 
                                                        self.artist_name)



class Album(db.Model):
    """Album of HappyFridays website."""

    __tablename__ = "albums"

    album_id = db.Column(db.String(50), primary_key=True)
    album_name = db.Column(db.String(100), nullable=False)
    link_to_album = db.Column(db.String(60), nullable=False)
    album_art = db.Column(db.String(70), nullable=False)
    album_release_date = db.Column(db.String(15), nullable=False)
    artist_id = db.Column(db.String(50), db.ForeignKey('artists.artist_id'))

    # # Define relationship to Artist
    artists = db.relationship('Artist')
    # # Define relationship to Track
    tracks = db.relationship('Track')    
    # # Define relationship to UserAlbum
    users_albums = db.relationship('UserAlbum')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Album album_id=%s album_name=%s>" % (self.album_id, 
                                                      self.album_name)

class UserAlbum(db.Model):
    __tablename__ = 'users_albums'

    user_album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(60),
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    album_id = db.Column(db.String(50),
                         db.ForeignKey('albums.album_id'),
                         nullable=False)

    # # Define relationship to User
    users = db.relationship('User')
    # # Define relationship to Album
    albums = db.relationship('Album')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserAlbum user_album_id=%s user_id=%s album_id=%s>" % (self.user_album_id, 
                                                                        self.user_id,
                                                                        self.album_id)


class Playlist(db.Model):
    """Playlist of Spotify user."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.String(50), primary_key=True)
    playlist_name = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.user_id'))

    # # Define relationship to User
    users = db.relationship('User')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Playlist playlist_id=%s playlist_name=%s>" % (
            self.playlist_id, self.playlist_name)



class Track(db.Model):
    """Album track uris of HappyFridays website."""

    __tablename__ = "tracks"

    #Each Spotify album track URI is 36 characters in length, including the quotes
    album_track_uri = db.Column(db.String(40), primary_key=True)
    album_id = db.Column(db.String(50), db.ForeignKey('albums.album_id'))

    # # Define relationship to Album
    albums = db.relationship('Album')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Track album_track_uri=%s album_id=%s>" % (self.album_track_uri, 
                                                                self.album_id)


##############################################################################
# Helper functions


def connect_to_db(app, db_uri=None):
    """Connect the database to Flask app."""

    #Configure to use my PostgreSQL database either via deployed HappyFridays database or locally using this:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///albums'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if I run this module interactively, it will leave
    # me in a state of being able to work with the database directly.


    from server_copy import app
    connect_to_db(app)
    print "Connected to DB."

