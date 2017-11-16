from flask_script import Manager
from songbase import app, db, Artist, Song

manager = Manager(app)


# reset the database and create some initial data
@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    coldplay = Artist(name='Coldplay', about='Coldplay is a British rock band.')
    maroon5 = Artist(name='Maroon 5', about='Maroon 5 is an American pop rock band.')
    song1 = Song(name='Yellow', year=2000, lyrics="Look at the stars", artist=coldplay)
    song2 = Song(name='Sugar', year=2014, lyrics="I'm hurting, baby, I'm broken down", artist=maroon5)
    db.session.add(coldplay)
    db.session.add(maroon5)
    db.session.add(song1)
    db.session.add(song2)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
