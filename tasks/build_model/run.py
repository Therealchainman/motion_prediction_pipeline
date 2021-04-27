import pandas as pd
import os
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import sys
import tensorflow
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

"""
The names of the models
nn-softplus
nn-selu
nn-multilayer-softmax-relu
nn-relu
LR
CART
"""


def buildModel():
    df_train = pd.read_csv('/data/projects/car-insurance/data/df_train.csv')
    X_train, y_train = np.array(df_train.drop(
        columns=['car_insurance'])), np.array(df_train.car_insurance)
    n_shape = X_train.shape[1]
    if name == 'nn-softplus':
        model = Sequential()
        model.add(Dense(4, input_shape=(n_shape,), activation='softplus'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=1, batch_size=4, verbose=0)
        model.save(f'/data/projects/car-insurance/data/{name}.h5')
    elif name == 'nn-selu':
        model = Sequential()
        model.add(Dense(4, input_shape=(n_shape,), activation='selu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=1, batch_size=4, verbose=0)
        model.save(f'/data/projects/car-insurance/data/{name}.h5')
    elif name == 'nn-multilayer-softmax-relu':
        model = Sequential()
        model.add(Dense(4, input_shape=(n_shape,), activation='softmax'))
        model.add(Dense(4, activation='relu'))
        model.add(Dense(4, activation='relu'))
        model.add(Dense(2, activation='softmax'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=1, batch_size=4, verbose=0)
        model.save(f'/data/projects/car-insurance/data/{name}.h5')
    elif name == 'nn-relu':
        model = Sequential()
        model.add(Dense(4, input_shape=(n_shape,), activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=1, batch_size=4, verbose=0)
        model.save(f'/data/projects/car-insurance/data/{name}.h5')
    elif name == 'LR':
        model = LogisticRegression(random_state=0, solver="liblinear")
        model.fit(X_train, y_train)
        pickle.dump(model, open(
            f'/data/projects/car-insurance/data/{name}.sav', 'wb'))
    elif name == 'CART':
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        pickle.dump(model, open(
            f'/data/projects/car-insurance/data/{name}.sav', 'wb'))
    else:
        print("provide a valid model name")
        return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Enter the name of one model")
    name = sys.argv[1]
    if os.path.isfile(f'/data/projects/car-insurance/data/{name}.sav') and os.path.getsize(f'/data/projects/car-insurance/data/{name}.sav') > 0:
        print("Skipping as the model file already exists")
    else:
        buildModel()
