import pandas as pd
from app import io
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def preprocess_features():
    """Preprocess and store customer features"""
    
    data = io.load_source_data()
    features = extract_features(data)
    io.save_features(features)


def extract_features(data):
    """Create features for prediction"""

    logger.debug('computing features')

    features = pd.DataFrame()

    # ----| 1) Max number of items per order
    logger.debug('1) Max number of items per order')
    features['max_items_by_order'] =\
        data\
        .groupby(['customer_id', 'order_id'])['num_items']\
        .sum()\
        .groupby('customer_id')\
        .max()

    # ----| 2) Max revenue per order
    logger.debug('2) Max revenue per order')
    features['max_revenue_by_order'] = \
        data\
        .groupby(['customer_id', 'order_id'])['revenue']\
        .sum()\
        .groupby('customer_id').max()

    # ----| 3) Total revenue
    logger.debug('3) Total revenue')
    features['total_revenue'] =\
        data\
        .groupby('customer_id')['revenue']\
        .sum()

    # ----| 4) number of orders
    logger.debug('4) number of orders')
    features['nb_orders'] = \
        data\
        .groupby('customer_id')['order_id']\
        .nunique()

    # ----| 5) days since last order
    logger.debug('5) days since last order')
    now = datetime(year=2017, month=10, day=17)
    features['days_since_last_order'] = now - \
        data\
        .groupby('customer_id')['created_at_date']\
        .max()

    # ----| 6) if more than one order: longest interval between two orders
    # if only one order: average of first group + days since last order
    logger.debug('6) longest interval between two orders')

    # identify multiple and single clients
    multiple_clients = \
        features[features['nb_orders'] > 1]\
        .reset_index()['customer_id']
    single_clients = \
        features[features['nb_orders'] == 1]\
        .reset_index()['customer_id']

    # metric for multiple clients
    longest_interval = \
        data[data['customer_id'].isin(multiple_clients)]\
        .sort_values('created_at_date')\
        .groupby('customer_id')['created_at_date']\
        .apply(lambda g: g.diff().max())

    # substitute metric for single clients
    longest_interval_substitute = \
        features\
        .loc[single_clients, 'days_since_last_order']\
        + longest_interval.mean()

    # merge results
    features['longest_interval'] = pd.concat(
        [longest_interval, longest_interval_substitute])

    # ----| convert timedelta dtypes into float number of
    #       days with hour resolution

    logger.debug('converting timedelta into days')
    for c in ['days_since_last_order', 'longest_interval']:
        features[c] = features[c].astype('timedelta64[h]') / 24

    # ----| ensure correct feature order
    logger.debug('ordering features')
    features_order = [
        'max_items_by_order',
        'max_revenue_by_order',
        'total_revenue',
        'nb_orders',
        'days_since_last_order',
        'longest_interval']
    features = features[features_order]
    return features
