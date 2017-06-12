#  Файл содержит все функции использованые для подготовки и загрузки массивов данных x, y
import csv
import os
import cv2
import numpy
# создаем один входной поток с картинками ввиде numpyarray
import gc
# получаем полный список всех объектов в папке
# общая функция вызываемая из вне
def func_load(df1, df2, num, path='set', path2=''):
    b = []
    n = 0
    with open(path2+'vixod.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            b.append((row['ImageId'],row['LabelName'],row['Confidence']))

    file_listing = os.listdir(path)
    file_listing.sort()
    mytxt = filter(lambda x: x.endswith('.jpg'), file_listing)
    for txt in mytxt:
        n = n + 1
        if n < num:
            continue
        # вписваем нужную функцию из представленных ниже -> loadimage, loadimagewithoutann и другие.
        # если нужно корректируем выходные данные
        df1, df2 = loadimage(df1,df2, path, path2, txt, b)
        if n % 1000 == 0:
            print(n)
            gc.collect()
            break
    print("all" + path)
    return df1, df2

def loadimage(df1, df2, path, path2, txt, b):
    txt = path + "/" + txt
    # print(txt)
    img = cv2.imread(txt)
    n_rows, n_cols, n_channels = img.shape
    i = 0;
    j = 0;
    pix = []
    a = []
    flag = 0
    while (i < n_rows):
        arr1 = []
        j = 0
        while (j < n_cols):
            arr2 = []
            arr2.append(img[i, j][0])
            arr2.append(img[i, j][1])
            arr2.append(img[i, j][2])
            arr1.append(arr2)
            j = j + 1
        i = i + 1
        pix.append(arr1)
    str = txt[len(path)+1:]
    str = str[:-4]
    with open(path2+'namesLabel.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            a.append((row['LabelName']))
    csvfile.close()
    arr = [0 for i in range(200)]
    for i in range(len(b)):
        if b[i][0] != str and flag == 0:
            continue
        if b[i][0] == str:
            for j in range(len(a)):
                if a[j] == b[i][1]:
                    arr[j] = round(float(b[i][2]), 2)
                    break;
            flag = 1
            continue
        if b[i][0] != str and flag == 1:
            break
    df1.append(pix)
    df2.append(arr)
    return df1, df2

def loadimagewithoutann(df1, path, txt):
    txt = path + "/" + txt
    img = cv2.imread(txt)
    n_rows, n_cols, n_channels = img.shape
    i = 0;
    pix = []
    while (i < n_rows):
        arr1 = []
        j = 0
        while (j < n_cols):
            arr2 = []
            arr2.append(img[i, j][0])
            arr2.append(img[i, j][1])
            arr2.append(img[i, j][2])
            arr1.append(arr2)
            j = j + 1
        i = i + 1
        pix.append(arr1)
    df1.append(pix)
    return df1


def loadimagewithoutannresize(df1, path, txt):
    txt = path + "/" + txt
    img = cv2.imread(txt)
    n_rows, n_cols, n_channels = img.shape
    i = 0;
    pix = []
    while (i < n_rows):
        arr1 = []
        j = 0
        while (j < n_cols):
            arr2 = []
            arr2.append(img[i, j][0])
            arr2.append(img[i, j][1])
            arr2.append(img[i, j][2])
            arr1.append(arr2)
            j = j + 1
        i = i + 1
        pix.append(arr1)
    df1.append(pix)
    return df1

def func_load_without_ann(df1, num, path='set', path2=''):
    n = 0
    file_listing = os.listdir(path)
    file_listing.sort()
    mytxt = filter(lambda x: x.endswith('.jpg'), file_listing)
    for txt in mytxt:
        n = n + 1
        if n < num:
            continue
        df1 = loadimagewithoutann(df1, path, txt)
        if n % 1000 == 0:
            print(n)
            gc.collect()
            break
    print("all" + path)
    return df1

def load_ann(df1, num, path, path2):
    b = []
    n = 0
    with open(path2 + 'vixod.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            b.append((row['ImageId'], row['LabelName'], row['Confidence']))
    file_listing = os.listdir(path)
    file_listing.sort()
    mytxt = filter(lambda x: x.endswith('.jpg'), file_listing)
    for txt in mytxt:
        n = n + 1
        if n < num:
            continue
        df1 = loadann(df1, path, path2, txt, b)
        if n % 1000 == 0:
            print(n)
            gc.collect()
            break
    print("all" + path)
    return df1

def loadann(df1, path, path2, txt, b):
    txt = path + "/" + txt
    a = []
    flag = 0
    str = txt[len(path) + 1:]
    str = str[:-4]
    with open(path2 + 'namesLabel.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            a.append((row['LabelName']))
    csvfile.close()
    arr = [0 for i in range(200)]
    for i in range(len(b)):
        if b[i][0] != str and flag == 0:
            continue
        if b[i][0] == str:
            for j in range(len(a)):
                if a[j] == b[i][1]:
                    arr[j] = round(float(b[i][2]), 2)
                    break;
            flag = 1
            continue
        if b[i][0] != str and flag == 1:
            break
    df1.append(arr)
    return df1


def load_ann_human(df1, num, path, path2):
    b = []
    c = []
    a = []
    n = 0
    with open(path2 + 'vixodTest.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            b.append((row['ImageId'], row['LabelName'], row['Confidence']))
    print(len(b))
    with open('val/test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            c.append((row['ImageID'], row['LabelName'], row['Confidence']))
    print(len(c))
    with open(path2 + 'namesLabel.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            a.append((row['LabelName']))
    print(len(a))
    csvfile.close()
    file_listing = os.listdir(path)
    file_listing.sort()
    mytxt = filter(lambda x: x.endswith('.jpg'), file_listing)
    for txt in mytxt:
        n = n + 1
        if n < num:
            continue
        df1 = loadannhuman(df1, path, txt, b, c, a)
        if n % 1000 == 0:
            print(n)
            gc.collect()
            break
    print("all" + path)
    return df1

def loadannhuman(df1, path, txt, b, c, a):
    txt = path + "/" + txt
    flag = 0
    str = txt[len(path) + 1:]
    str = str[:-4]
    arr = [0 for i in range(200)]
    for i in range(len(b)):
        if b[i][0] != str and flag == 0:
            continue
        if b[i][0] == str:
            for j in range(len(a)):
                if a[j] == b[i][1]:
                    arr[j] = round(float(b[i][2]), 2)
                    break;
            flag = 1
            continue
        if b[i][0] != str and flag == 1:
            break
    flag = 0
    for i in range(len(c)):
        if c[i][0] != str and flag == 0:
            continue
        if c[i][0] == str:
            for j in range(len(a)):
                if a[j] == c[i][1]:
                    arr[j] = round(float(c[i][2]), 2)
                    break;
            flag = 1
            continue
        if c[i][0] != str and flag == 1:
            break
    df1.append(arr)
    return df1

def load_image_numpy(path):
    df = numpy.load(path)
    return df



