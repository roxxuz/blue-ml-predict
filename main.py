import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
from tensorflow.compat.v1.keras.models import load_model
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from resize import getfromurl, deletefiles

#Create Flask instance
app = Flask(__name__)

#Disable cache store.
#When cache is stored the uploaded files are not updated if they got
#the same filename as a previous uploaded file.
@app.after_request
def add_header(r):
	
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

#Loading pretrained Tensorflow model
model = load_model('models/2nd_model.h5')

dl = 1

#app.route defines what will happen when client visits the main page both for "GET" and "POST" methods.
@app.route('/', methods=['GET', 'POST'])
def main_page():

	# Empties the "uploads" folder
	deletefiles()

	#If method is "POST" the file is saved in the uploads folder and the user is redirected to url /prediction/(uploaded filename)
	if request.method == 'POST':
		
		#saves file info in "file". (type = werkzeug.FileStorage)
		file = request.files['file']

		# Get url from textfield
		url = request.form["url"]

		# Gets the url and splits it to get the file extension. If the end of the URL isn't a file extension it sets it as .jpg
		a, b = os.path.splitext(url)
		if b != "jpg" or "png" or "jpeg":
			if "jpeg" in url:
				b = ".jpeg"
			if "jpg" in url:
				b = ".jpg"
			if "png" in url:
				b = ".png"
		
		#If no file is selected then return to index.html (to prevent crash)
		if file.filename != '':

			# secure_filename returns a string that is converted without any special characters. (ASCII only)
			filename = secure_filename(file.filename)

			# Saving file 'uploads/<filename.jpg>'
			# os.path.join conatinates one or more path components separated with a /
			file.save(os.path.join('static/uploads', filename))

			# redirects to /prediction/<uploaded_file_name>
			return redirect(url_for('prediction', filename=filename))

			# If textfield isn't empty, "getfromurl" method downloads the image from the url
		global dl
		if url != "":
			getfromurl(url, dl, b)

			# redirects to /prediction/<downloaded_file_name>
			return redirect(url_for('prediction', filename=f"{str(dl)}{b}"))
		dl += 1

		#prevent crash if a non-image file is uploaded
		if file.filename == '' and url == "" and\
			(file.filename.split('.')[1] != 'jpg' and
			file.filename.split('.')[1] != 'jpeg' and
			file.filename.split('.')[1] != 'png'):
			return render_template('index.html')


	#Else (if method is "GET") send user to index.html
	return render_template('index.html')


#app.route defines what will happen when client visits /prediction/(uploaded filename)
@app.route('/prediction/<filename>')
def prediction(filename):

	#Image is read from the uploads folder using the filename from the created url.
	image = plt.imread(os.path.join('static/uploads', filename))

	#Image is being resized to 32*32 pixels (the third argument/dimension number 3 is for RGB)
	image_resized = resize(image, (32, 32, 3))

	#Predicting the uploaded image with our pretrained model. np.array() is used to transform 3D-array to 4D-array.
	#  this is mandatory for the predict function.
	probabilities = model.predict(np.array([image_resized,]))[0,:]

	#probabilities(array) index positions gets sorted from lowest to highest prediction values, and saved in array called 'index'.
	index = np.argsort(probabilities)

	#Array named 'index' is reversed with [::-1] to get the top predictions first.
	index = index[::-1]

	#Creating a list with all classes (this is for the prediction output text)
	classes = ['Airplane', 'Car', 'Bird',
				'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

	#Creating dictionary with top 3 predictions based on the index array.
	#probabilities value are converted to "percent" and int. ( 0.6789457384 = 68)
	predictions = {
					"class1": classes[index[0]],
					"class2": classes[index[1]],
					"class3": classes[index[2]],
					"prob1": int(round(probabilities[index[0]]*100, 0)),
					"prob2": int(round(probabilities[index[1]]*100, 0)),
					"prob3": int(round(probabilities[index[2]]*100, 0))
					}

	#Creating
	image_path = os.path.join('../static/uploads', filename)

	#return will send user to predict.html (in templates folder) and make the predictions dictionary available in the html code.
	return render_template('predict.html', predictions=predictions, image_path=image_path)

#start Flask server (debug=True to make the server restart after each save)
app.run(host='127.0.0.1', port=8080, debug=True)
