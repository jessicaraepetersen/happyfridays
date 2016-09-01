import schedule
import time
from model import connect_to_db, db, User, Artist, Album, UserAlbum, Playlist, Track

#clear data from UserAlbum table, which is the list of Spotify new releases by 
#artists the user follows - a.k.a the list that the app builds
def job():
    db.session.query(UserAlbum).delete()

# schedule.every(1).minutes.do(job)
schedule.every().friday.at("0:15").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)