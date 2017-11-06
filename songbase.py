from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    # return HTML
    return "<h1>this is the index page!<h1>"


@app.route('/users')
def get_all_users():
    return "<h2>this is the page for all users</h2>"


@app.route('/users/<string:name>/')
def get_user_name(name):
    # return "hello " + name
    return "Hello %s, this is %s" % (name, 'administrator')


@app.route('/songs/<int:id>/')
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
