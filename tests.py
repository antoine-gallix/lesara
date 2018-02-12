from app import etl
from app import io
import random
import pytest


# ---------------------conf---------------------

nb_customer_for_test = 5
seed = 1000

# ---------------------fixtures---------------------
full_order_data = io.load_source_data()


@pytest.fixture
def customers():
    """random few customer ids"""

    customer_ids = full_order_data['customer_id']\
        .drop_duplicates()\
        .sample(nb_customer_for_test, random_state=seed)
    return customer_ids


@pytest.fixture
def order_data(customers):
    """order data, limited to a few customers"""
    test_data = full_order_data[full_order_data['customer_id']
                                .isin(customers)]
    return test_data


@pytest.fixture
def features(order_data):
    """features for a few customers"""
    return etl.extract_features(order_data)


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


def test_save_features(features):
    """
    """
    io.save_features(features)


def test_get_features(features, customers):
    """
    """
    io.save_features(features)
    cid = random.choice(list(customers))
    customer_features = io.get_features(cid)
    assert len(customer_features) == 6
