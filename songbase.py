import os
from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# define database tables
class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    about = db.Column(db.Text)
    songs = db.relationship('Song', backref='artist', cascade="delete")


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    year = db.Column(db.Integer)
    lyrics = db.Column(db.Text)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))


@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/artists')
def show_all_artists():
    artists = Artist.query.all()
    return render_template('artist-all.html', artists=artists)


@app.route('/artist/add', methods=['GET', 'POST'])
def add_artists():
    if request.method == 'GET':
        return render_template('artist-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        about = request.form['about']

        # insert the data into the database
        artist = Artist(name=name, about=about)
        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('show_all_artists'))


@app.route('/artist/edit/<int:id>', methods=['GET', 'POST'])
def edit_artist(id):
    artist = Artist.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('artist-edit.html', artist=artist)
    if request.method == 'POST':
        # update data based on the form data
        artist.name = request.form['name']
        artist.about = request.form['about']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_artists'))


@app.route('/artist/delete/<int:id>', methods=['GET', 'POST'])
def delete_artist(id):
    artist = Artist.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('artist-delete.html', artist=artist)
    if request.method == 'POST':
        # delete the artist by id
        # all related songs are deleted as well
        db.session.delete(artist)
        db.session.commit()
        return redirect(url_for('show_all_artists'))


# song-all.html adds song id to the edit button using a hidden input
@app.route('/songs')
def show_all_songs():
    songs = Song.query.all()
    return render_template('song-all.html', songs=songs)


@app.route('/song/add', methods=['GET', 'POST'])
def add_songs():
    if request.method == 'GET':
        artists = Artist.query.all()
        return render_template('song-add.html', artists=artists)
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        year = request.form['year']
        lyrics = request.form['lyrics']
        artist_name = request.form['artist']
        artist = Artist.query.filter_by(name=artist_name).first()
        song = Song(name=name, year=year, lyrics=lyrics, artist=artist)

        # insert the data into the database
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('show_all_songs'))


@app.route('/song/edit/<int:id>', methods=['GET', 'POST'])
def edit_song(id):
    song = Song.query.filter_by(id=id).first()
    artists = Artist.query.all()
    if request.method == 'GET':
        return render_template('song-edit.html', song=song, artists=artists)
    if request.method == 'POST':
        # update data based on the form data
        song.name = request.form['name']
        song.year = request.form['year']
        song.lyrics = request.form['lyrics']
        artist_name = request.form['artist']
        artist = Artist.query.filter_by(name=artist_name).first()
        song.artist = artist
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_songs'))


@app.route('/song/delete/<int:id>', methods=['GET', 'POST'])
def delete_song(id):
    song = Song.query.filter_by(id=id).first()
    artists = Artist.query.all()
    if request.method == 'GET':
        return render_template('song-delete.html', song=song, artists=artists)
    if request.method == 'POST':
        # use the id to delete the song
        # song.query.filter_by(id=id).delete()
        db.session.delete(song)
        db.session.commit()
        return redirect(url_for('show_all_songs'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users')
def show_all_users():
    return render_template('user-all.html')


@app.route('/form-demo', methods=['GET', 'POST'])
def form_demo():
    # how to get form data is different for GET vs. POST
    if request.method == 'GET':
        first_name = request.args.get('first_name')
        if first_name:
            return render_template('form-demo.html', first_name=first_name)
        else:
            return render_template('form-demo.html', first_name=session.get('first_name'))
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        # return render_template('form-demo.html', first_name=first_name)
        return redirect(url_for('form_demo'))


@app.route('/user/<string:name>/')
def get_user_name(name):
    # return "hello " + name
    # return "Hello %s, this is %s" % (name, 'administrator')
    return render_template('user.html', name=name)


@app.route('/song/<int:id>/')
def get_song_id(id):
    # return "This song's ID is " + str(id)
    return "Hi, this is %s and the song's id is %d" % ('administrator', id)


# https://goo.gl/Pc39w8 explains the following line
if __name__ == '__main__':

    # activates the debugger and the reloader during development
    # app.run(debug=True)
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)
