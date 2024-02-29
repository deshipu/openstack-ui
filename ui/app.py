#!/usr/bin/env python

import flask
import auth
import dashboard


app = flask.Flask(__name__)
app.secret_key='oink'
app.register_blueprint(dashboard.bp)


@app.route('/')
def index():
    print(app.url_map)
    return flask.redirect(flask.url_for('dashboard.projects'))


@app.route('/login', methods=('get', 'post'))
def login():
    if flask.request.method == 'POST':
        if auth.try_login(flask.request.form['username'],
                          flask.request.form['password']):
            return flask.redirect(flask.url_for('index'))
    return flask.render_template("login.html")


if __name__ == '__main__':
    app.run()
