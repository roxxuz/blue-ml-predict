import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
from tensorflow.compat.v1.keras.models import load_model
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

#Create Flask instance
app = Flask(__name__)

#Loding pretrained Tensorflow model
model = load_model('models/blue-tf-img-pred-model.h5')


#Default endpoint. App route defines what will happen when client visits the main page both for "GET" and "POST" methods.
#If method is "POST" the file is saved in the uploads folder and the client is redirected to /prediction/(uploaded filename)
#Else (if method is "GET") send user to index.html
@app.route('/', methods=['GET', 'POST'])
def main_page():
   if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join('uploads', filename))
      return redirect(url_for('prediction', filename=filename))
   return render_template('index.html')

#App route defines what will happen when client visits /prediction/(uploaded filename)
#Image is read from the uploads folder using the filename from the created url.
#Image is being resized to 32*32 pixels.
#Predicted the image with our pretrained model

@app.route('/prediction/<filename>')
def prediction(filename):
   image = plt.imread(os.path.join('uploads', filename))
   image_resized = resize(image, (32, 32, 3))
   probabilities = model.predict(np.array([image_resized, ]))[0, :]
   classes = ['Airplane', 'Car', 'Bird',
               'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
   index = np.argsort(probabilities)
   predictions = {
                  "class1": classes[index[9]],
                  "class2": classes[index[8]],
                  "class3": classes[index[7]],
                  "prob1": int(round(probabilities[index[9]]*100, 0)),
                  "prob2": int(round(probabilities[index[8]]*100, 0)),
                  "prob3": int(round(probabilities[index[7]]*100, 0))
                  }
   return render_template('predict.html', predictions=predictions)


app.run(host='127.0.0.1', port=8080, debug=True)
