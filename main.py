import os
import matplotlib.pyplot as plt
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from resize import getfromurl, deletefiles, resize
from multicrop import multicrop, ten_crop_pred, mirror_image
from prediction import prediction as pred
import numpy as np
from multicrop import score

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

dl = 1

#Global variable slider to get access in both main_page and prediction method.
#slider = '0'

#app.route defines what will happen when client visits the main page both for "GET" and "POST" methods.
@app.route('/', methods=['GET', 'POST'])
def main_page():

	# Empties the "uploads" folder
	deletefiles()

	# Reset "score" dictionary
	for key in score.keys():
		score[key] = 0

	#If method is "POST" the file is saved in the uploads folder and the user is redirected to url /prediction/(uploaded filename)
	if request.method == 'POST':
		
		#saves file info in "file". (type = werkzeug.FileStorage)
		file = request.files['file']

		# Get url from textfield
		url = request.form["url"]

		#Writing globaly to slider
		#Getting value from html form and input name = slider
		#global slider
		slider = request.form['slider']

		#Prevent crash when no file is selected or
		#the file is not an image
		if file.filename == '' and url == '':
			print('inside if')
			return render_template('index.html')
		elif (file.filename != '' and
			os.path.splitext(file.filename)[1] != '.jpg' and
		 	os.path.splitext(file.filename)[1] != '.jpeg' and
		 	os.path.splitext(file.filename)[1] != '.png'):
			return render_template('index.html')
		
		# Gets the url and splits it to get the file extension. If the end of the URL isn't a file extension it sets it as .jpg
		a, b = os.path.splitext(url)
		if b != "jpg" or "png" or "jpeg":
			if "jpeg" in url:
				b = ".jpeg"
			if "jpg" in url:
				b = ".jpg"
			if "png" in url:
				b = ".png"
			else:
				b = '.jpg'
		
		#If no file is selected then return to index.html (to prevent crash)
		if file.filename != '':

			# secure_filename returns a string that is converted without any special characters. (ASCII only)
			filename = secure_filename(file.filename)

			# Saving file 'uploads/<filename.jpg>'
			# os.path.join conatinates one or more path components separated with a /
			file.save(os.path.join('static/uploads', filename))
			print(f'===> Slider in main: {slider}')
			# redirects to /prediction/<uploaded_file_name>
			return redirect(url_for('prediction', filename=filename, slider=slider))

			# If textfield isn't empty, "getfromurl" method downloads the image from the url
		global dl
		if url != "":
			getfromurl(url, dl, b)

			# redirects to /prediction/<downloaded_file_name>
			return redirect(url_for('prediction', filename=f"{str(dl)}{b}", slider=slider))
		dl += 1



	#Else (if method is "GET") send user to index.html
	return render_template('index.html')


#app.route defines what will happen when client visits /prediction/(uploaded filename)
@app.route('/prediction/<filename><slider>')
def prediction(filename, slider):

	original_image_path = "static/uploads/" + filename

	#Checking the value of variable 'slider'.
	#This is from the html slider in index.html 
	#to select pre-processing method.
	if slider == '1':
		type = 'original'
	elif slider == '2':
		type = 'mirror'
	elif slider == '3':
		type = 'center'
	elif slider == '4':
		type = '10crop'


	if type == "original":

		# Image is read from the uploads folder using the filename from the created url.
		image = plt.imread(os.path.join('static/uploads', filename))
		resize(filename, False, True)
		filename = "distorted" + filename
		#Sending image and filename to predict method and getting predictions and image_path in return
		predictions, image_path = pred(image, filename)

	#Makes a mirror version of the image
	elif type == "mirror":
		image = mirror_image(filename)
		filename = "mirror" + filename
		# Sending image and filename to predict method and getting predictions and image_path in return
		predictions, image_path = pred(image, filename)

	#Crops the center of the image. (long sides (height or width) gets cut off, short side (height or width) stays the same).
	elif type == "center":
		image = resize(filename)
		filename = "center_crop" + filename
		# Sending image and filename to predict method and getting predictions and image_path in return
		predictions, image_path = pred(np.array(image), filename)

	elif type == "10crop":

		#Sending filename to ten crop method to make 10 versions of the same image
		#The probability score gets combined for all 10 versions to make a final/combined probability score
		predictions, image_path = ten_crop_pred(filename)

	#return will send user to predict.html (in templates folder) and make the predictions dictionary available in the html code.
	return render_template('predict.html', predictions=predictions, image_path=image_path)

@app.route('/howItWasDone')
def howItWasDone():
	return render_template('how-it-was-done.html')

@app.route('/aboutUs')
def aboutUs():
   return render_template('aboutUs.html')


#start Flask server (debug=True to make the server restart after each save)
if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8080, debug=True)
