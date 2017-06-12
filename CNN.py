import keras
import numpy
import pydot_ng
from keras.applications import VGG16
from keras.callbacks import ModelCheckpoint
from keras.layers import Flatten, Dense, Dropout
from keras.models import Model, load_model

from keras import backend as K
from keras.optimizers import SGD
from keras.utils import plot_model

K.set_image_dim_ordering('th')
K.set_image_data_format('channels_last')
print(keras.backend.image_data_format())

import Func_for_Preparing_Arrays as s

# Задаем seed для повторяемости результатов
numpy.random.seed(42)
# СОЗДАЕМ МОДЕЛЬ. ПРИМЕР СОЗДАНИЯ АРХИТЕКТУРЫ МОДЕЛИ НА МОДЕЛИ ИСПОЛЬЗОВАННОЙ В КОНЕЧНОМ ПРИЛОЖЕНИИ
nb_classes = 99
model = VGG16(weights='imagenet', include_top=False, input_shape=(48, 48, 3))
model_in = Model(input=model.input, outputs=model.get_layer("block5_pool").output)
print(model_in.summary())
for layer in model_in.layers[0:10]:
    print(layer.name, layer.output_shape)
for layer in model_in.layers[0:10]:
    layer.trainable = False
print(model_in.summary())
pydot_ng.find_graphviz()
# Adding custom Layers
x = model_in.output
x = Dropout(0.25)(x)
x = Flatten()(x)
# x = Dense(1024, activation="relu")(x)
# x = Dropout(0.5)(x)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x)
predictions = Dense(nb_classes, activation="sigmoid")(x)

# creating the final model
model_final = Model(input=model.input, output=predictions)
print(model_final.summary())
#
# compile the model
model_final.compile(loss="binary_crossentropy", optimizer=SGD(lr=0.0001, momentum=0.9),
                    metrics=["accuracy"])
#
print(pydot_ng.find_graphviz())
plot_model(model_final, to_file='model.png', show_shapes=True)
print(model_final.summary())
# Имя модели -> пример
model_final.save('57-0.128.hdf5')
print("save")


# Обучение модели
checkpoint = ModelCheckpoint("all/stab/{epoch:02d}-{val_loss:.3f}.hdf5", monitor='val_acc', verbose=1, save_best_only=False, save_weights_only=False,
                             mode='auto', period=1)
# early = EarlyStopping(monitor='val_acc', min_delta=0, patience=10, verbose=1, mode='auto')
Y_train = s.load_image_numpy('all/X_newtrain.dat')
X_train = s.load_image_numpy('all/Y_newtrain.dat')
numpy.random.seed(31)
X_train = X_train.astype('float32')
# не надо делить на 255 так как для данных newtrain100laybles уже поделено
# X_train /= 255
batch_size = 128
# грузим сохраненную модель
model_final = load_model('all/stab/56-0.13.hdf5')
print(model_final.summary())
# если продолжаем обучение уже обучавшейся модели - меняем seem  numpy.random.seed(31)
# Train the model
model_final.fit(X_train, Y_train,
                epochs=100,
                batch_size=batch_size,
                validation_split=0.1,
                shuffle=True,
                initial_epoch=57,
                callbacks=[checkpoint])


# test
# указываем путь до созданных файлов
X_test = s.load_image_numpy('all/X_newtrain.dat')
X_test = X_test.astype('float32')
# X_test = X_test.astype('float32')
# X_test /= 255
Y_test = s.load_image_numpy('all/Y_newtrain.dat')
#указываем путь до модели
model_final = load_model('all/stab/57-0.128.hdf5')
y = model_final.predict(X_test[330:331], batch_size=128, verbose=0)
y1 = model_final.predict(X_test[229:230], batch_size=128, verbose=0)
y2 = model_final.predict(X_test[1969:1970], batch_size=128, verbose=0)
y_proba = model_final.predict(X_test[2:3], batch_size=128, verbose=0)

print(y)
print(Y_test[330].astype('float32'))
print(y_proba)
print(Y_test[2:3])
print(y1)
print(Y_test[229].astype('float32'))
print(y2)
print(Y_test[1969].astype('float32'))


# predict to my photo
mytest = []
mytest = s.loadimagewithoutannresize(mytest, 'pic','2.jpg')
mytest = numpy.asarray(mytest)
print(mytest)
mytest = mytest.astype('float32')
mytest /= 255
print(mytest)
model_final = load_model('all/model2/13-0.146.hdf5')
y = model_final.predict(mytest, batch_size=32, verbose=0)
print(y)

# После обучения модели модель помещается в папку application и используется в файле application/func.py
# там же работа с word2vec уже подготовленный файл application/wordsimilarAll.csv