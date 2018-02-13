import pandas as pd
from datetime import datetime
import logging
import numpy
import dill
import logging
import sqlite3

logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')

features_file='data/features.pkl'
model_file = 'data/model.dill'
predictions_file = 'data/predictions.db'


def predict(features):
    """makes CLV predictions
    input: dataframe
    return: series of CLV predictions
    """
    model = dill.load(open(model_file, 'rb'))
    array = numpy.array(features.values)
    logger.info('precomputing CLV predictions')
    predictions = model.predict(array)
    return pd.Series(predictions, index=features.index, name='CLV')

if __name__ == '__main__':
    logger.info('reading features from {}'.format(features_file))
    features = pd.read_pickle(features_file)
    predictions = predict(features)
    logger.info('writing predictions to {}'.format(predictions_file))
    connection=sqlite3.connect(predictions_file)
    predictions.to_sql('predictions',connection)
