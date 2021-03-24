import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
from tensorflow.compat.v1.keras.models import load_model
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

global model
model = load_model('models/blue-tf-img-pred-model.h5')

@app.route('/', methods=['GET', 'POST'])
def main_page():
   if request.method == 'POST':
      file = request.files['file']
      filename = secure_filename(file.filename)
      file.save(os.path.join('uploads', filename))
      return redirect(url_for('prediction', filename=filename))
   return render_template('index.html')


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


app.run(host='127.0.0.1', port=80)
