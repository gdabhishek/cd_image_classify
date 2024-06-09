# app.py
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import numpy as np
from tensorflow.keras.models import load_model
import cv2

upload_folder = os.path.join('static', 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder

# Load the pre-trained VGG16 model
model = load_model('best_epoch_cnn.h5')
if not os.path.exists("static"):
    os.mkdir("static")
    os.mkdir(upload_folder)

def predict(image_path):
    image = cv2.imread(image_path) #read the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #cvt from BGR to RGB
    image = cv2.resize(image,(128, 128)) #RESIZE THE IMAGE TO 128,128
    image = image * (1.0/255.0) #Scaling
    image = np.array([image])#cvt from 128,128, to 1,128,128,3
    y_pred = model.predict(image, verbose = 0)
    y_pred = y_pred > 0.5
    y_pred = y_pred.astype("int")[0][0]
    classes = ["Cat","Dog"]
    return classes[y_pred]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    filename = None
    file_path = None
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(file_path)
        prediction = predict(file_path)
    return render_template('index.html', prediction=prediction, filename=filename,file_path=file_path)

if __name__ == '__main__':
    app.run(debug=False)
