# LoadImage, see git https://github.com/openimages/dataset.git README.md
# file validation/images.csv  -> validation/namesLabel.csv
import csv
from PIL import Image
from urllib.request import urlopen
a = []
# cur image's number
n = 0
with open('images/validation/namesLabel.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        n = n+1
        # if Part load
        # if n < 152561:
        #     continue
        if row['Thumbnail300KURL'] != '':
            image = Image.open(urlopen(row['Thumbnail300KURL']))
            image.save('image/'+row['ImageID'] + '.jpg')
            b1 = b1 + 1
            a.append((row['ImageID'], row['Thumbnail300KURL']))
            print(n)


# Далее в 5-ти частях описана работа с загруженными изображение.
# преобразование их в numpy массив. а также создание для них numpyмассива выходных данных с метками классов.
# использование функций из Func_for_preparing_Arrays
import csv
import os
# Part1
b = []
# составить файл с именами картинок что есть в датасете - составили namesPic.csv
# получаем полный список всех объектов в папке (куда загружены изображения необходимого размера уже 48*48 в нашем случае)
file_listing = os.listdir('imageSet')
for image_path in file_listing:
    if '.jpg' in image_path:
        str = image_path[:-4]
        b.append(str)
print(len(b))
file_listing = os.listdir('imageSet2')
for image_path in file_listing:
    if '.jpg' in image_path:
        str = image_path[:-4]
        b.append(str)
print(len(b))
file_listing = os.listdir('imageSet3')
for image_path in file_listing:
    if '.jpg' in image_path:
        str = image_path[:-4]
        b.append(str)
print(len(b))

file_listing = os.listdir('image5')
for image_path in file_listing:
    if '.jpg' in image_path:
        str = image_path[:-4]
        b.append(str)
print(len(b))

set1 = set(b)
print(len(set1))

b = list(set1)
# создали файл с именами изображений
with open('all/namesPic.csv', 'w', newline='') as csvfile:
    fieldnames = ['LabelName']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(b)):
        writer.writerow({'LabelName': b[i]})

print(b)
# Part 2
pic = []
n = 0
# предварительно создав данный файл обходом по всем меткам к загруженным изображниям и подсчитали сколько раз каждая метка встречается
# annotation/validation + val/labels   эти папки будут скачены при работе с OpenImage dataset - ссылка в начале файла
with open('all/namesLabel.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    # sortedlist = sorted(reader, key=lambda row:row['LabelName'], reverse=False)
    for row in reader:
        # записываем данные о первых 100 метках, количество упоминаний у которых не менее 450
        if int(row['Col']) > 450 and n < 100:
            n = n + 1
            pic.append((row['LabelName'],row['Name'],row['Col']))
print(n)
print(pic)
with open('all/namesPic.csv', 'w', newline='') as csvfile:
    fieldnames = ['LabelName']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(pic)):
        writer.writerow({'LabelName': pic[i]})

lastName = pic[-1]
b2 = []
b1 = 0
def load (b,b1):
    last = 0
    with open('val/labels.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            b1 = b1 + 1
            if last == 1 and lastName != row['ImageID']:
                break;
            if lastName == row['ImageID']:
                last = 1
            if float(row['Confidence']) > 0.9 and row['ImageID'] in pic:
                b.append((row['LabelName'],1))
    return b, b1

b2, b1 = load(b2,b1)
print(b1)
#939830 - last word - 899d665a061762ea,human,/m/057xtgl,0.0
setarr = set(b2)
# 6263 word setarr
print(len(setarr))
import numpy
setarr = list(setarr)
setarr = numpy.array(setarr)

with open('val/labels.csv') as csvfile:
    last = 0
    reader = csv.DictReader(csvfile)
    for row in reader:
        b1 = b1 + 1
        if last == 1 and lastName != row['ImageID']:
            break;
        if lastName == row['ImageID']:
            last = 1
        if float(row['Confidence']) > 0.9 and row['ImageID'] in pic:
            for i in range(len(setarr)):
                if setarr[i][0] == row['LabelName']:
                    setarr[i][1] = str((int(setarr[i][1]) + 1))
                    break;
print(len(setarr))
max = 0
for i in range(len(setarr)):
    if max < int(setarr[i][1]):
        max = int(setarr[i][1])
# 5979 for 30k image
print(max)

with open('all50/namesLabel.csv', 'w', newline='') as csvfile:
    fieldnames = ['LabelName', 'Name','Col']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(pic)):
        writer.writerow({'LabelName': pic[i][0],'Name': pic[i][1], 'Col': pic[i][2]})


# Part 3
b = []
a = []
c = []
n = 0
min = 10000
with open('all/names.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # метки с каким количеством упоминаний выбирать
        if n < 20 and int(row['Col']) < 451 and int(row['Col']) > 445:
            if int(row['Col']) < min:
                min = int(row['Col'])
            a.append((row['LabelName']))
            c.append((row['LabelName'], row['Col']))
            n = n + 1
# 100
print(len(a))
# 507
print(min)
print(n)
print(a)
with open('all/namesLabel2.csv', 'w', newline='') as csvfile:
    fieldnames = ['LabelName', 'Col']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(a)):
        writer.writerow({'LabelName': c[i][0], 'Col': c[i][1]})
with open('dict1.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['LabelName'] in a:
            b.append((row['LabelName'], row['Name']))
print(len(b))
print((b[1][0]))


with open('all/namesLabel2.csv', 'w', newline='') as csvfile:
    fieldnames = ['LabelName', 'Name', 'Col']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(b)):
        for j in range (len(c)):
            if (b[i][0] == c[j][0]):
                writer.writerow({'LabelName': b[i][0], 'Name': b[i][1], 'Col': c[j][1]})

# Part 4
# создаем выборку для нашего сета обучающую # 141918 строк
# 190257# 1741384
a = []
b = []
c = []
n = 0
with open('all50/namesLabel.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        a.append((row['LabelName']))

with open('all/namesPic.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        b.append((row['LabelName']))

with open('ann/validation/labels.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (row['ImageID'] == 'e88f3c601641b901'):
            break;
        if (row['ImageID'] in b and row['LabelName'] in a):
            n = n + 1
            c.append((row['ImageID'], row['LabelName'], row['Confidence']))
            if n%1000 == 0:
                print(n)
print(len(c))

with open('all50/vixod.csv', 'w', newline='') as csvfile:
    fieldnames = ['ImageId','LabelName','Confidence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(c)):
        writer.writerow({'ImageId': c[i][0], 'LabelName': c[i][1], 'Confidence': c[i][2]})
print('all')

# Part 5
import numpy
import Func_for_Preparing_Arrays as s
# X_train = s.load_image_numpy('all128/x_train.dat')
# Y_train = s.load_image_numpy('all128/y_train.dat')
X_train = []
Y_train = []
X_train1 = []
Y_train1 = []
for i in range(0,104):
    print(i)
    X_train1, Y_train1 = s.func_load(X_train1, Y_train1,(i)*500+1, 'full','all/')
    X_train1 = numpy.asarray(X_train1)
    Y_train1 = numpy.asarray(Y_train1)
    if i == 0:
        X_train = X_train1
        Y_train = Y_train1
    else:
        if (X_train1.size != 0):
            X_train = numpy.concatenate((X_train, X_train1), axis=0)
            Y_train = numpy.concatenate((Y_train, Y_train1), axis=0)
    X_train1 = []
    Y_train1 = []
    # X_train.dump("all128/x_train.dat")
    # Y_train.dump("all128/y_train.dat")

X_train.dump("all96/x_trainall.dat")
Y_train.dump("all96/y_trainall.dat")
X_train = s.load_image_numpy('all96/x_trainall.dat')
Y_train = s.load_image_numpy("all96/y_trainall.dat")
print(X_train.shape)