from PIL import Image
import math
import numpy as np
import os
import requests


# Downloads an image from url
def getfromurl(url, dl, ext):
    try:
        r = requests.get(url)
        with open(f"static/uploads/{dl}{ext}", "wb") as f:
            f.write(r.content)
    except:
        print("Something wrong with downloading the picture.")


def deletefiles():
    for i in os.listdir("static/uploads/"):
        if i != ".gitignore":
            os.remove(f"static/uploads/{i}")


#def get_np_array(image):
#    ###GET RESIZED IMAGE AS NP ARRAY
#    image_as_array.append(image)


def resize(path, size_width=32, size_height=32, save_image=False, savepath="f{path}/resized"):

    image_as_array = []

    if save_image == True:
        try:
            os.mkdir(savepath)
        except:
            pass
    else:
        pass

    for i in os.listdir(path):

        try:
            image = Image.open(f"{path}/{i}")
            filename = i
            ### GET WIDTH AND HEIGHT FROM IMAGE
            width, height = image.size
            print(width, height)

            ### DIFF GETS DIFFERENCE BETWEEN WIDTH AND HEIGHT
            diff = width - height
            print(f"difference {diff}")

            ### SUPERADVANCED MATH STUFF (MAKING SURE YOU GET A POSITIVE VALUE)

            exp_diff = int(diff**2)
            print(f"Exponent {exp_diff}")
            squared_diff = int(math.sqrt(exp_diff))
            print(f"Squared difference {squared_diff}")

            ### GET HALF THE DIFFERENCE TO CENTER THE CROP

            half_crop = int(squared_diff/2)
            print(f"Half difference {half_crop}")

            print(half_crop, 0, width-half_crop, height)
            print(0, half_crop, 0, half_crop+height)


            if width > height:
                box = (half_crop, 0, width-half_crop, height)
            else:
                box = (0, half_crop, width, height-half_crop)


            cropped_image = image.crop(box)
            print(f"cropped size {cropped_image.size}")
            #x = cropped_image.thumbnail((32, 32))
            resized_image = cropped_image.resize((size_width, size_height))
            print(f"resized {resized_image.size}")

#            if save_image == True:
#                ###SAVE IMAGE IN NEW FOLDER AND ADD RESIZED TO NAME
#                resized_image.save(savepath+"resized"+filename)
#            else:
#                pass

            ###GET RESIZED IMAGE AS NP ARRAY
            image_as_array.append(np.asarray(resized_image))
            np_array = np.asarray(image_as_array)
            np_array = np_array/255
            print(type(np_array))

            return np_array

        except:
            print("Something went wrong")
