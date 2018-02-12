"""Data IO, disk and memory
"""


import pandas as pd
import logging

logger = logging.getLogger(__name__)

source_file = 'data/orders.csv'
features_file = 'data/features.pkl'


def load_source_data():
    """import data from csv file"""

    logger.debug('load data from {}'.format(source_file))
    data = pd.read_csv(source_file, parse_dates=['created_at_date'])
    return data


def save_features(features):
    """save features to memory"""

    logger.debug('save features to {}'.format(features_file))
    features.to_pickle(features_file)


def get_features(customer_id):
    """get prediction features for a customer"""
    logger.debug('getting prediction features for customer {}'
                 .format(customer_id))
    features = pd.read_pickle(features_file)
    return features.loc[customer_id]
