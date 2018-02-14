"""Makes CKV predictions from pickle file to sqlite database file


use:
    python make_predictions.py data/features.pkl data/predictions.db

"""

import pandas as pd
from datetime import datetime
import logging
import numpy
import dill
import logging
import sqlite3
import click

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

@click.command()
@click.argument('features_file',type=click.Path())
@click.argument('predictions_file',type=click.Path())
def main(features_file,predictions_file):
    
    logger.info('reading features from {}'.format(features_file))
    features = pd.read_pickle(features_file)
    
    predictions = predict(features)
    
    connection=sqlite3.connect(predictions_file)
    
    logger.info('deleting previous tables')
    connection.cursor().execute('drop table if exists predictions')
    
    logger.info('writing predictions to {}'.format(predictions_file))
    predictions.to_sql('predictions',connection)

if __name__ == '__main__':
    main()
