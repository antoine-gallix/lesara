import dill
import numpy

model = dill.load(open('data/model.dill', 'rb'))


def predict_CLV(features):
    return model.predict(features)
