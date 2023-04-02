import os

import keras.models
import numpy as np
import re
import cv2

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D

model = keras.models.load_model(os.path.abspath("./app/chess_model.h5"))

piece_symbols = 'prbnkqPRBNKQ'

# def getModel():
#     model = Sequential()
#     model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(30, 30, 3)))
#     model.add(MaxPooling2D(pool_size=(3, 3)))
#     model.add(Convolution2D(16, (5, 5),activation='relu'))
#     model.add(Flatten())
#     model.add(Dropout(0.35))
#     model.add(Dense(13, activation='softmax'))
#     model.compile(optimizer='adam',
#                   loss='categorical_crossentropy',
#                   metrics=['accuracy'])
#     EPOCHS = 100
#     hist = model.fit(train_gen(train), steps_per_epoch=train_size // EPOCHS, epochs=EPOCHS,
#                      validation_data=pred_gen(test), validation_steps=test_size // EPOCHS)
#     return model;

def display_with_predicted_fen(image):

    pred = model.predict(preprocess_image("./app/media/" + str(image) + ".jpeg")).argmax(axis=1).reshape(-1, 8, 8)
    fen = fen_from_onehot(pred[0])
    return fen

def train_gen(features):
    for i, img in enumerate(features):
        y = onehot_from_fen(get_image_FEN_label(img))
        x = preprocess_image(img)
        yield x, y

def pred_gen(features):
    for i, img in enumerate(features):
        y = onehot_from_fen(get_image_FEN_label(img))
        x = preprocess_image(img)
        yield x, y

def onehot_from_fen(fen):
    eye = np.eye(13)
    output = np.empty((0, 13))
    fen = re.sub('[-]', '', fen)

    for char in fen:
        if(char in '12345678'):
            output = np.append(
              output, np.tile(eye[12], (int(char), 1)), axis=0)
        else:
            idx = piece_symbols.index(char)
            output = np.append(output, eye[idx].reshape((1, 13)), axis=0)

    return output

def fen_from_onehot(one_hot):
    output = ''
    for j in range(8):
        for i in range(8):
            if(one_hot[j][i] == 12):
                output += ' '
            else:
                output += piece_symbols[one_hot[j][i]]
        if(j != 7):
            output += '-'

    for i in range(8, 0, -1):
        output = output.replace(' ' * i, str(i))

    return output

def get_image_FEN_label(image_path):
    fen_label= image_path.replace('.jpeg', '').split('/')[-1]
    return fen_label


def preprocess_image(img_path):
    height = 240
    width = 240

    img = cv2.imread(os.path.abspath(img_path), cv2.COLOR_BGR2GRAY)
    # resize the image to the desired size
    gray_image = cv2.resize(img, (width, height))

    # Normalize the image
    gray_image = (gray_image - np.min(gray_image)) / (np.max(gray_image) - np.min(gray_image))

    squares = image_to_squares(gray_image, height, width)
    return squares

def image_to_squares(img,heights,widths):
  squares = []
  for i in range(0,8):
    for j in range(0,8):
      squares.append(img[i*heights//8:i*heights//8+heights//8,j*widths//8:j*widths//8+widths//8])
  return np.array(squares)