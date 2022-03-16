import json
import os
import annotation_handler as an
import user_handler as uh

from flask import Flask, request, render_template, session, flash, redirect, url_for

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def radiologist_page():
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        im = request.json['imageName']
        vertices = request.json['coordinates']

        an.update_row(im, json.dumps(vertices))
        return ''


@app.route('/annotations', methods=['POST'])
def get_annotations():
    im = request.json['imageName']
    vertices = an.get_row(im)['annotations']
    if vertices is None:
        vertices = "[]"
    return json.dumps(json.loads(vertices))


@app.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        print("login post")
        user_id = request.form["username"]
        password = request.form["password"]

        print("user_id and password", user_id, " ", password)
        error = None
        user = uh.get_row(user_id)
        print("user is", user)
        if user is None:
            error = "Incorrect username."
        elif not user["password"] == password:
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            print("here")
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("radiologist_page"))

        flash(error)

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return ("you're logged out!")


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(host="localhost", port=8000, debug=True)
