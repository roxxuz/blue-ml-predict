
from PIL import Image, ImageOps
import math
import numpy as np
import os
from tensorflow.compat.v1.keras.models import load_model
import matplotlib.pyplot as plt
import cv2

#Dictionary to combine scores from all versions of the image
score = {
    'Airplane': 0,
    'Car': 0,
    'Bird': 0,
    'Cat': 0,
    'Deer': 0,
    'Dog': 0,
    'Frog': 0,
    'Horse': 0,
    'Ship': 0,
    'Truck': 0
}

#Tensorflow model for the predictions
model = load_model('models/2nd_model.h5')

def concat_image(filename):
    from PIL import Image

    ims1 = f"static/uploads/1{filename}"
    ims2 = f"static/uploads/2{filename}"
    ims3 = f"static/uploads/3{filename}"
    ims4 = f"static/uploads/4{filename}"
    ims5 = f"static/uploads/5{filename}"
    ims6 = f"static/uploads/6{filename}"
    ims7 = f"static/uploads/7{filename}"
    ims8 = f"static/uploads/8{filename}"
    ims9 = f"static/uploads/9{filename}"
    ims10 = f"static/uploads/10{filename}"

    all_ims = [ims1, ims2, ims3, ims4, ims5, ims6, ims7, ims8, ims9, ims10]

    for j, i in enumerate(all_ims):
        img = cv2.imread(i)

        color = [0, 0, 0]  # 'cause purple!

        # border widths; I set them all to 150
        top, bottom, left, right = [25] * 4

        bore = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        cv2.imwrite(f"static/uploads/x{j+1}{filename}", bore)

        #   plt.imshow(img_with_border)
        plt.show()

    im1 = Image.open(f"static/uploads/x1{filename}")
    im2 = Image.open(f"static/uploads/x2{filename}")
    im3 = Image.open(f"static/uploads/x3{filename}")
    im4 = Image.open(f"static/uploads/x4{filename}")
    im5 = Image.open(f"static/uploads/x5{filename}")
    im6 = Image.open(f"static/uploads/x6{filename}")
    im7 = Image.open(f"static/uploads/x7{filename}")
    im8 = Image.open(f"static/uploads/x8{filename}")
    im9 = Image.open(f"static/uploads/x9{filename}")
    im10 = Image.open(f"static/uploads/x10{filename}")

    w, h = im1.size

    print(w, h)

    newim = Image.new("RGB", (4 * w, 3 * w), (0, 0, 0))

    newim.paste(im1, (int(w), 0))
    newim.paste(im2, (int(w * 2), 0))
    newim.paste(im3, (int(0), w))
    newim.paste(im4, (w, w))
    newim.paste(im5, (w * 2, w))
    newim.paste(im6, (w * 3, w))
    newim.paste(im7, (0, w * 2))
    newim.paste(im8, (int(w), w * 2))
    newim.paste(im9, (int(w * 2), w * 2))
    newim.paste(im10, (int(w * 3), w * 2))

    newim.save("static/uploads/multiPic.jpg")
 #   newim.show()


def multicrop(image, filename):
    global run

    #Get the size of the picture. Height/Width/Difference
    width, height = image.size
    diff = width - height
    exp_diff = int(diff ** 2)
    squared_diff = int(math.sqrt(exp_diff))
    half_crop = int(squared_diff / 2)

    squares = []

    if width > height:
        square = int(height * 0.7)
        negsquare = int(width / 2 - square / 2)
        sidecrop = int((width - square) / 2)
        topcrop = int((height - square) / 2)

        box1 = (0, 0, square, square)
        box2 = (negsquare, 0, square + negsquare, square)
        box3 = (width-square, 0, width, square)
        box4 = (0, height-square, square, height)
        box5 = (negsquare, height-square , square + negsquare, height)
        box6 = (width-square, height - square, width, height)
        box7 = (0, 0, width-squared_diff, height)
        box8 = (half_crop, 0, width - half_crop, height)
        box9 = (squared_diff, 0, width, height)
        box10 = (sidecrop, topcrop, width - sidecrop, height - topcrop)

        squares.extend((box1, box2, box3, box4, box5, box6, box7, box8, box9, box10))

    else:
        square = int(width * 0.7)
        negsquare = int(height / 2 - square / 2)
        sidecrop = int((width - square) / 2)
        topcrop = int((height - square) / 2)

        print(height)
        print(square)
        print(negsquare)

        box1 = (0, 0, square, square)
        box2 = (width-square, 0, width, square)
        box3 = (0, negsquare, square, square + negsquare)
        box4 = (width-square, negsquare, width, square + negsquare)
        box5 = (0, height - square, square, height)
        box6 = (width - square, height - square, width, height)
        box7 = (0, 0, width, height - squared_diff)
        box8 = (0, half_crop, width, height-half_crop)
        box9 = (0, squared_diff, width, height)
        box10 = (sidecrop, topcrop, width - sidecrop, height - topcrop)

        squares.extend((box1, box2, box3, box4, box5, box6, box7, box8, box9, box10))

    crop1 = image.crop(squares[0])
    crop2 = image.crop(squares[1])
    crop3 = image.crop(squares[2])
    crop4 = image.crop(squares[3])
    crop5 = image.crop(squares[4])
    crop6 = image.crop(squares[5])
    crop7 = image.crop(squares[6])
    crop8 = image.crop(squares[7])
    crop9 = image.crop(squares[8])
    crop10 = image.crop(squares[9])

    crop1.save(f"static/uploads/1{filename}")
    crop2.save(f"static/uploads/2{filename}")
    crop3.save(f"static/uploads/3{filename}")
    crop4.save(f"static/uploads/4{filename}")
    crop5.save(f"static/uploads/5{filename}")
    crop6.save(f"static/uploads/6{filename}")
    crop7.save(f"static/uploads/7{filename}")
    crop8.save(f"static/uploads/8{filename}")
    crop9.save(f"static/uploads/9{filename}")
    crop10.save(f"static/uploads/10{filename}")

    concat_image(filename)

    crops = [crop1, crop2, crop3, crop4, crop5, crop6, crop7, crop8, crop9, crop10]

    return crops


def ten_crop_pred(filename):

       #Image is read from the uploads folder using the filename from the created url.
    #   image = plt.imread(os.path.join('static/uploads', filename))

       image = Image.open("static/uploads/"+filename)
       cropped_image_array = multicrop(image, filename)

       #Image is being resized to 32*32 pixels (the third argument/dimension number 3 is for RGB)
    #   image_resized = resize(image, (32, 32, 3))

       #Predicting the uploaded image with our pretrained model. np.array() is used to transform 3D-array to 4D-array.
       #  this is mandatory for the predict function.

       for i in cropped_image_array:
            rez = i.resize((32, 32))
            # file    image_as_array = []
            #    image_as_array.append(np.asarray(rez))
            np_array = np.asarray(rez)
            np_array = np_array / 255
            np_array = np_array[:, :, :3]
            #predict(np_array)
            probabilities = model.predict(np.array([np_array,]))[0,:]

       #probabilities(array) index positions gets sorted from lowest to highest prediction values, and saved in array called 'index'.
            index = np.argsort(probabilities)

       #Array named 'index' is reversed with [::-1] to get the top predictions first.
            index = index[::-1]

       #Creating a list with all classes (this is for the prediction output text)
            classes = ['Airplane', 'Car', 'Bird',
                   'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']


            for i in index:
                score[classes[index[i]]] += probabilities[index[i]]

       combined_probability = 0
       for i in score.values():
           combined_probability += i

       for i in score.values():
           prob = i / combined_probability
           print("proba is " + str(prob * 100))

       first = (sorted(score.values(), reverse=True, )[0])
       second = (sorted(score.values(), reverse=True, )[1])
       third = (sorted(score.values(), reverse=True, )[2])

       for i, j in score.items():
           if j == first:
               first_prob = i
           elif j == second:
               second_prob = i
           elif j == third:
               third_prob = i
           else:
               pass

       #Creating dictionary with top 3 predictions based on the index array.
       #probabilities value are converted to "percent" and int. ( 0.6789457384 = 68)
       predictions = {
                      "class1": first_prob,
                      "class2": second_prob,
                      "class3": third_prob,
                      "prob1": int(round((first/combined_probability)*100, 0)),
                      "prob2": int(round((second/combined_probability)*100, 0)),
                      "prob3": int(round((third/combined_probability)*100, 0))
                      }

       # Creating
   #    image_path = os.path.join('../static/uploads', filename)

       image_path = "/static/uploads/multiPic.jpg"
       return predictions, image_path


def mirror_image(filename):

    #Make a mirror version of the image.
    image = Image.open("static/uploads/"+filename)
    mirror = ImageOps.mirror(image)
    mirror.save(f"static/uploads/mirror{filename}")

    #Makes an numpy array of the picture
    np_array = np.asarray(mirror)
    np_array = np_array/255

    return np_array
