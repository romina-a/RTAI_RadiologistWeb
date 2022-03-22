import json
import os

from annotation_handler import AnnotationHandler
from werkzeug.security import check_password_hash

import user_handler as uh

from flask import Flask, request, render_template, session, flash, redirect, url_for, Response, abort

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.errorhandler(401)
def custom_401(error):
    return Response('<Only authorized users can save or see the annotations>',
                    401, {'WWW-Authenticate':'Basic realm="Login Required"'})


@app.route('/', methods=['GET', 'POST'])
def radiologist_page():
    if request.method == 'GET':
        return render_template("annotation.html")
    if request.method == 'POST':
        if session.get('user_id') is None:
            abort(401)
        im = request.json['imageName']
        vertices = request.json['coordinates']

        AnnotationHandler(session.get('user_id')).update_row(im, json.dumps(vertices))
        return ''


@app.route('/annotations', methods=['POST'])
def get_annotations():
    if session.get('user_id') is None:
        vertices = "[]"
    else:
        im = request.json['imageName']
        print("get_annotations")
        print(session.get('user_id'))
        row = AnnotationHandler(session.get('user_id')).get_row(im)
        if row is None:
            vertices = "[]"
        else:
            vertices = row['annotations']
    return json.dumps(json.loads(vertices))


@app.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        print("login post")
        user_id = request.form['username']
        password = request.form['password']

        error = None

        if session.get('user_id') is not None:
            error = "Already logged in"

        user = uh.get_row(user_id)
        print("user is:", user)
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            print("here")
            session.clear()
            user_id = user['user_id']
            session['user_id'] = user_id
            return redirect(url_for("radiologist_page"))
            # return redirect(request.url) TODO try this

        flash(error)

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return "you're logged out!"


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(host="localhost", port=8000, debug=True)
