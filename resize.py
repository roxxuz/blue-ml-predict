from PIL import Image
import math
import numpy as np
import os
import requests
import urllib


# Downloads an image from url
def getfromurl(url, ext):
    try:
        r = requests.get(url)
        with open(f"static/uploads/1{ext}", "wb") as f:
            f.write(r.content)
    except:
        
        response = urllib.request.urlopen(url)

        with open('static/uploads/1.jpg', 'wb') as f:
            f.write(response.file.read())


def deletefiles():
    for i in os.listdir("static/uploads/"):
        if i != ".gitignore":
            os.remove(f"static/uploads/{i}")


def resize(filename, crop = True, save_image=True):

    image = Image.open("static/uploads/"+filename)

    ### GET WIDTH AND HEIGHT FROM IMAGE
    width, height = image.size
#    print(width, height)

    ### DIFF GETS DIFFERENCE BETWEEN WIDTH AND HEIGHT
    diff = width - height
#    print(f"difference {diff}")

    ### SUPERADVANCED MATH STUFF (MAKING SURE YOU GET A POSITIVE VALUE)

    exp_diff = int(diff**2)
#    print(f"Exponent {exp_diff}")
    squared_diff = int(math.sqrt(exp_diff))
#    print(f"Squared difference {squared_diff}")

    ### GET HALF THE DIFFERENCE TO CENTER THE CROP

    half_crop = int(squared_diff/2)

    if width > height:
        box = half_crop, 0, width-half_crop, height
        distorted_image = image.resize((height, height))
    else:
        box = 0, half_crop, width, height-half_crop
        distorted_image = image.resize((width, width))

        #Crop the sides of the image to make it square
    cropped_image = image.crop(box)

    if save_image == True:
        if crop == True:
            ###SAVE IMAGE IN NEW FOLDER AND ADD RESIZED TO NAME
            cropped_image.save(f"static/uploads/center_crop{filename}")
        else:
            distorted_image.save(f"static/uploads/distorted{filename}")

    ###GET RESIZED IMAGE AS NP ARRAY
    n_array = np.asarray(cropped_image)
    np_array = n_array/255
    np_array = np_array[:, :, :3]

    if crop == True:
        return np_array
    else:
        return distorted_image

