"""Models and database functions for New For You project."""

from flask_sqlalchemy import SQLAlchemy

import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Album(db.Model):
    """Album of New For You website."""

    __tablename__ = "albums"

    album_id = db.Column(db.String(50), primary_key=True)
    album_name = db.Column(db.String(100), nullable=False)
    link_to_album = db.Column(db.String(60), nullable=False)
    album_art = db.Column(db.String(70), nullable=False)
    artist_id = db.Column(db.String(50), nullable=False, db.ForeignKey('artists.artist_id'))
    album_track_uri = db.Column(db.String(), nullable=False) #HELP QUEUE: How do I make an arry as the item in the list?
    #Each Spotify album track URI is 36 characters in length, including the quotes

    # # Define relationship to Artist
    artist = db.relationship( 'Artist', backref='albums')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Album album_id=%s album_name=%s>" % (self.album_id, self.album_name)


class Artist(db.Model):
    """Artist of New For You website."""

    __tablename__ = "artists"

    artist_id = db.Column(db.String(50), primary_key=True)
    artist_name = db.Column(db.String(100), nullable=False)
    link_to_artist = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artist artist_id=%s artist_name=%s>" % (self.artist_id, self.artist_name)


class Playlist(db.Model):
    """Playlist of Spotify user."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.String(50), primary_key=True)
    playlist_name = db.Column(db.String(140))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Playlist playlist_id=%s playlist_name=%s>" % (
            self.playlist_id, self.playlist_name)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///albums'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
