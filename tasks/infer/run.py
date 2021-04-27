import pandas as pd
import pickle
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
import csv
import sys
import tensorflow
from tensorflow.keras.models import load_model

"""
The names of the models
nn-softplus
nn-selu
nn-multilayer-softmax-relu
nn-relu
LR
CART
"""


def savePredictionsv1(preds, file):
    with open(f"/data/projects/motion_prediction/data/{file}", "w") as csv_file:
        fieldnames = ["prediction"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for _, pred in enumerate(preds):
            writer.writerow({"prediction": str(pred)})


def savePredictionsv2(preds, file, outcomes):
    with open(f"/data/projects/motion_prediction/data/{file}", "w") as csv_file:
        fieldnames = ["prediction"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i, pred in enumerate(preds):
            if outcomes[i] == 1:
                writer.writerow({"prediction": str(1)})
            else:
                writer.writerow({"prediction": str(pred)})


def savePredictionsv3(preds, file, outcomes, duration):
    with open(f"/data/projects/motion_prediction/data/{file}", "w") as csv_file:
        fieldnames = ["prediction"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for _, pred in enumerate(preds):
            if outcomes[i] == 1 or duration > 1000:
                writer.writerow({"prediction": str(1)})
            else:
                writer.writerow({"prediction": str(pred)})


def infer():
    df_test = pd.read_csv('/data/projects/motion_prediction/data/df_test.csv')
    X_test = np.array(df_test)
    outcomes = [row['Outcome'] for _, row in df_test.iterrows()]
    durations = [row['duration'] for _, row in df_test.iterrows()]
    if name == 'LR' or name == 'CART':
        model = pickle.load(
            open(f'/data/projects/motion_prediction/data/{name}.sav', 'rb'))
    else:
        model = load_model(f'/data/projects/motion_prediction/data/{name}.h5')
    target = model.predict(X_test)
    savePredictionsv1(target, f'results_{name}1.csv')
    savePredictionsv2(target, f'results_{name}2.csv', outcomes)
    savePredictionsv3(target, f'results_{name}3.csv', outcomes, durations)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Enter the name of one model")
    else:
        name = sys.argv[1]
        infer()
