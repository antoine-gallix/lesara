import random
import pytest
import numpy
import app
import pandas as pd
import extract_features
import make_predictions

# ---------------------fixtures---------------------


test_order_data='data/orders_dev.csv'

@pytest.fixture
def order_data():
    """order data, limited to a few customers"""
    return pd.read_csv(test_order_data, parse_dates=['created_at_date'])

@pytest.fixture
def customers(order_data):
    """customers in test data"""
    return order_data.reset_index()['customer_id'].tolist()


@pytest.fixture
def predictions(order_data):
    """saved predictions"""
    features = extract_features.extract_features(order_data)
    return make_predictions.predict(features)


# ---------------------tests---------------------


def test_test_order_data_is_not_null(order_data):
    assert len(order_data) > 0


def test_extract_features(order_data):
    """sanity check for feature extraction"""

    features = extract_features.extract_features(order_data)
    nb_customers=order_data.reset_index()['customer_id'].nunique()
    print(hash(tuple(features.index.values)))
    assert features is not None
    assert len(features)==nb_customers


"""it's not possible to unit test the predic function because of the dill numpy import issue"""
