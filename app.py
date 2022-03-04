import json
import annotation_handler as an

from flask import Flask, request, render_template

app = Flask(__name__)


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
    vertices = an.get_row(im)
    return json.dumps(json.loads(vertices))


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(host="localhost", port=8000, debug=True)
