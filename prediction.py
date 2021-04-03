import os
from skimage.transform import resize
from tensorflow.compat.v1.keras.models import load_model
import numpy as np

#Loading pretrained Tensorflow model
model = load_model('models/2nd_model.h5')

def prediction(image, filename):

    # Image is being resized to 32*32 pixels (the third argument/dimension number 3 is for RGB)
    image_resized = resize(image, (32, 32, 3))

    # Predicting the uploaded image with our pretrained model. np.array() is used to transform 3D-array to 4D-array.
    #  this is mandatory for the predict function.
    probabilities = model.predict(np.array([image_resized, ]))[0, :]

    # probabilities(array) index positions gets sorted from lowest to highest prediction values, and saved in array called 'index'.
    index = np.argsort(probabilities)

    # Array named 'index' is reversed with [::-1] to get the top predictions first.
    index = index[::-1]

    # Creating a list with all classes (this is for the prediction output text)
    classes = ['Airplane', 'Car', 'Bird',
               'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

    # Creating dictionary with top 3 predictions based on the index array.
    # probabilities value are converted to "percent" and int. ( 0.6789457384 = 68)
    predictions = {
        "class1": classes[index[0]],
        "class2": classes[index[1]],
        "class3": classes[index[2]],
        "prob1": int(round(probabilities[index[0]] * 100, 0)),
        "prob2": int(round(probabilities[index[1]] * 100, 0)),
        "prob3": int(round(probabilities[index[2]] * 100, 0))
    }

    # Creating
    image_path = os.path.join('../static/uploads', filename)

    return predictions, image_path
