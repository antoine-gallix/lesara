import flask
import random
import pandas as pd
import logging
import os
import sqlite3

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')

# data config
predictions_file = 'data/predictions.db'

# ----| IO functions

def get_customer_prediction(customer_id=None):
    """Get predictions for a customer

    customer_id: returns random customer if None
    """
    logger.info('reading predictions from db')
    conn=sqlite3.connect(predictions_file)
    if customer_id:
        query='select CLV from predictions where customer_id = "{}"'
        prediction=conn.execute(query.format(customer_id)).fetchall()[0][0]
    else:
        query='select * from predictions order by random() limit 1'
        customer_id, prediction=conn.execute(query).fetchall()[0]
    return customer_id, prediction


# CLV service
CLV_server = flask.Blueprint('CLV_server', 'CLV_server')


@CLV_server.route('/customers/<customer_id>/predicted_CLV')
def CLV_prediction(customer_id):
    """Return CLV prediction for the given customer_id

    if customer_id is 'random', the customer id is chosen at random from the available data.

    ex:
        >>GET /customers/2504175708a53b19fe067b06472e4cec/predicted_CLV
        {
            "customer_id": "2504175708a53b19fe067b06472e4cec", 
            "predicted_CLV": 116.92
        }
    """
    if customer_id == 'random':
        customer_id = None
    customer_id, predicted_CLV = get_customer_prediction(customer_id)
    payload = {
        'customer_id': customer_id,
        'predicted_CLV': predicted_CLV
    }
    return flask.json.jsonify(payload)


# ----| app startup


def create_app(config):
    app = flask.Flask('CLV_predict')
    app.register_blueprint(CLV_server)
    if config == 'debug':
        app.debug = True
        os.environ['WERKZEUG_DEBUG_PIN'] = 'off'
    return app


if __name__ == '__main__':
    app = create_app('debug')
    app.run()
