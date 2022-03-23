# webpage code modified from https://towardsdatascience.com/build-a-web-application-for-predicting-apple-leaf-diseases-using-pytorch-and-flask-413f9fa9276a
from flask import Flask, request, render_template, redirect, flash, jsonify
from werkzeug.utils import secure_filename

import torch
import io
from torchvision import transforms

from PIL import Image
from C19Xception import C19Xception
from data import MyTopCropTransform


app = Flask(__name__)

# load model
device = 'cpu'
model = C19Xception(pretrained=False)
model.to(device)
model.load_state_dict(torch.load('xception-epochs_10-pretrained_True-batchsize_32-posweight_50-lr_0.003.pth', map_location=device))

# transform image
def transform(image_bytes):
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        MyTopCropTransform(0.08),
        # transforms.Resize(size=image_size), transforms.CenterCrop(image_size), # keeps the aspect ratio, crops the image
        transforms.Resize(size=(299, 299))  # doesn't keep the aspect ratio
    ])
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB") # model takes in images with three channels
    print(type(image))
    return test_transform(image).unsqueeze(0) # unsqueeze necessary to get 4-dimensional form

# get model prediction
threshold = 0.35
def get_prediction(image):
    model.to(device)
    model.eval()
    preds = []
    im = transform(image)
    print('transformed', im.size())
    im = im.to(device)
    with torch.set_grad_enabled(False):
        preds.extend(model(im))

    prob = torch.tensor(preds).sigmoid()

    if prob > threshold:
        detection = "positive"
    else:
        detection = "negative"
    prob = round(float(prob * 100),2)
    return prob,detection

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# web process
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/prediction', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            img_bytes = file.read()
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'img1'))
            prediction, detection = get_prediction(img_bytes)

            return str(detection)
    return "detection gets called"

if __name__ == '__main__':
    app.run(host = "localhost", port = 8000, debug = True)