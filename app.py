import flask
import random
import pandas as pd
import logging
import os
import sqlite3
from flask_json import FlaskJSON, JsonError, as_json
# logging
logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')


# ----| IO functions

def get_customer_prediction(customer_id=None):
    """Get predictions for a customer

    customer_id: returns random customer if None
    """
    logger.info('reading predictions from db')
    file=flask.current_app.config.predictions_file
    conn=sqlite3.connect(file)
    if customer_id:
        query='select CLV from predictions where customer_id = "{}"'
        results=conn.execute(query.format(customer_id)).fetchall()
        if results:
            prediction=results[0][0]
        else:
            raise JsonError(description='no data for this customer_id',
                status_=404)
    else:
        query='select * from predictions order by random() limit 1'
        customer_id, prediction=conn.execute(query).fetchall()[0]
    return customer_id, prediction


# CLV service
CLV_server = flask.Blueprint('CLV_server', 'CLV_server')


@CLV_server.route('/customers/<customer_id>/predicted_CLV')
@as_json
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
    return payload

@CLV_server.route('/test')
def test():
    return 'OK'

# ----| app startup


def create_app(config):
    app = flask.Flask('CLV_predict')
    app.register_blueprint(CLV_server)
    FlaskJSON(app)

    if config == 'debug':
        app.config.predictions_file = 'data/predictions_test.db'
        app.debug = True
        os.environ['WERKZEUG_DEBUG_PIN'] = 'off'
    elif config == 'test':
        app.config.predictions_file = 'data/predictions_test.db'
    elif config == 'prod':
        app.config.predictions_file = 'data/predictions.db'
    return app


if __name__ == '__main__':
    app = create_app('debug')
    app.run()
