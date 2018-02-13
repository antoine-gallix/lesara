import random
import pytest
import numpy
import app


# ---------------------fixtures---------------------


test_order_data='data/order_dev.csv'

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
    features = etl.extract_features(order_data)
    return etl.predict(features)


# ---------------------tests---------------------


def test_test_order_data_is_not_null(order_data):
    assert len(order_data) > 0
    assert len(order_data['customer_id'].unique()) == nb_customer_for_test


def test_extract_features(order_data):
    """sanity check for feature extraction"""

    features = etl.extract_features(order_data)
    print(hash(tuple(features.index.values)))
    assert features is not None
    assert len(features) == nb_customer_for_test


def test_save_predictions(predictions):
    """
    """
    io.save_predictions(predictions)


def test_get_predictions(predictions, customers):
    """
    """
    io.store_predictions(predictions)
    cid = random.choice(list(customers))
    CLV = io.get_prediction(cid)
    assert CLV is not None
