from app import create_app
import json
import pytest

@pytest.fixture(scope='session')
def client():
    app=create_app('test')
    return app.test_client()

# -----------------------------------------------


def test_app_running(client):
    response=client.get('/test')
    assert response.status_code==200

def test_get_CLV(client):
    customer_id='2504175708a53b19fe067b06472e4cec'
    response=client.get('/customers/{}/predicted_CLV'.format(customer_id))
    assert response.status_code==200
    data=json.loads(response.data)
    assert data['customer_id']==customer_id
    assert isinstance(data['predicted_CLV'],float)

def test_get_random_CLV(client):
    response=client.get('/customers/random/predicted_CLV')
    assert response.status_code==200
    data=json.loads(response.data)
    assert 'customer_id' in data
    assert isinstance(data['predicted_CLV'],float)

def test_wrong_customer_id(client):
    response=client.get('/customers/1000/predicted_CLV')
    assert response.status_code==404
