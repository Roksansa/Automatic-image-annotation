import PIL.Image
import csv
import re
import gensim
import numpy
import keras
import tensorflow as tf
from gensim.models import word2vec
from keras.models import load_model
from keras import backend as K
K.set_image_dim_ordering('th')
K.set_image_data_format('channels_last')
print(keras.backend.image_data_format())

model_final = load_model('application/57.hdf5')
graph = tf.get_default_graph()
word = []
with open('application/wordsimilarAll.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        word.append(list(filter(None, re.split('\W|\d', str(row['LabelName'])))))

def findword(df1):
    str1 = ""
    for i in range (len(df1)):
        if df1[i] == 1.0:
            b = numpy.arange(len(word[i]))
            numpy.random.shuffle(b)
            num = 0
            for j in range (int(len(b)/2)+1):
                if num > 3:
                    break
                str1 = str1 + " #"+str(word[i][j])
                num = num + 1
    return str1		

def handle_uploaded_file(f):
    with open('media/1.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def loadimageandresize(uploaded_file_url):
    df1 = []
    pil_image = PIL.Image.open('application'+uploaded_file_url).convert('RGB')
    width = height = 48
    resized_img = pil_image.resize((width, height), PIL.Image.ANTIALIAS)
    open_cv_image = numpy.array(resized_img)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    n_rows, n_cols, n_channels = open_cv_image.shape
    i = 0;
    pix = []
    while (i < n_rows):
        arr1 = []
        j = 0
        while (j < n_cols):
            arr2 = []
            arr2.append(open_cv_image[i, j][0])
            arr2.append(open_cv_image[i, j][1])
            arr2.append(open_cv_image[i, j][2])
            arr1.append(arr2)
            j = j + 1
        i = i + 1
        pix.append(arr1)
    df1.append(pix)
    df1 = numpy.array(df1)
    print(df1)
    return df1

def test(uploaded_file_url):
    mytest = []
    mytest = loadimageandresize(uploaded_file_url)
    mytest = numpy.asarray(mytest)
    mytest = mytest.astype('float32')
    mytest /= 255
    print(mytest.shape)
    global graph
    with graph.as_default():
        y = model_final.predict(mytest)
    #создадим границы
    x1 = [0.16540526, 0.52177811, 0.13316396, 0.53220683, 0.076892763, 0.082472451, 0.053068832, 0.077279359, 0.054314975, 0.055321094, 0.066137031, 0.78706443, 0.10230574, 0.98387676, 0.081188828, 0.9876917, 0.1121226, 0.13497181, 0.044200283, 0.22430354, 0.9805994, 0.066047497, 0.99674314, 0.24279112, 0.38912174, 0.054640368, 0.35634276, 0.14537176, 0.89284509, 0.038729966, 0.24797678, 0.17161623, 0.054184105, 0.36600137, 0.070102938, 0.077174321, 0.3126117, 0.30859897, 0.097237237, 0.11263698, 0.075618118, 0.07107307, 0.15260468, 0.93319422, 0.0641056, 0.20437017, 0.61966723, 0.072854668, 0.064676359, 0.074021481, 0.098677672, 0.1523295, 0.12643637, 0.99288917, 0.071373686, 0.077509232, 0.62575871, 0.12871926, 0.0514884, 0.052030697, 0.079218447, 0.25465313, 0.087667234, 0.10624457, 0.93361032, 0.043286476, 0.057392888, 0.13694133, 0.041564576, 0.07413394, 0.18821941, 0.15838365, 0.12190878, 0.91424507, 0.096441366, 0.23045985, 0.5890463, 0.062666468, 0.37185016, 0.047038008, 0.98665011, 0.72788501, 0.042495634, 0.053809647, 0.051710349, 0.047789354, 0.051971905, 0.054498043, 0.040952053, 0.045783304, 0.038993675, 0.039007213, 0.043737754, 0.027878881, 0.06535814, 0.047573935, 0.047026575, 0.05047255, 0.042612277]
    x11=[0 for i in range(99)]
    for i in range(len(x1)):
        if x1[i] > 0.5:
            x11[i] = x1[i]*0.7
            continue
        if x1[i] > 0.1:
            x11[i] = x1[i]*0.65
            continue
        x11[i] = x1[i]*0.65
    print(x11)

    for i in range(len(y)):
        for j in range(len(y[i])):
            if (y[i][j] > x11[j]):
                y[i][j] = 1
    sum1 = 0
    for i in range(len(y)):
        for j in range(len(y[i])):
            if (y[i][j] == 1 ):
                sum1 = sum1 + 1
    print(sum1)
    for k in range(6):
        max1 = 0
        i1 = -1
        for i in range(len(y)):
            for j in range(len(y[i])):
                if (y[i][j] > max1 and y[i][j] != 1 and sum1 < 5):
                    max1 = y[i][j]
                    i1 = j
            if (i1 != -1):
                y[i][i1] = 1
                sum1 = sum1 + 1
    print(y)
    y = findword(y[0])
    return y

