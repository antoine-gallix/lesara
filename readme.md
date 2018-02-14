# Lesara Test Task : Customer Lifetime Value Prediction And Microservice

## Architecture choices

## Data processing

A first command line script `extract_features.py` extracts features from the source data file. A second one `make_predictions` uses the provided model to make CLV predictions, and store them in a sqlite database file. Both scripts uses pandas for data processing.

## Web Service

A simple service in `app.py` serves the predicted CLV through a json api. Flask web framework is used. The API returns the CLV value for any given `customer_id` if present in the database. 404 HTTP error is the `customer_id` is not in the database. As bonus, using `random` in place of `customer_id` in the query URL returns a random value from the database.

## Tests

Two files, `test_processing.py` and `test_app.py` performs a few unit tests for processing scripts and the application. They are written and run using `pytest` testing framework. To speedup the tests, a third script, `make_test_data.py` produces a reduced version of the original data. The data processing scripts can then work with it to create test features and predictions.

### Limitation with pickled model

There is a problem with the dill-pickled model. The model will raise an error if numpy is not imported at the top level caller. It works in a small script but it makes it difficult to embed in an application. This issue is very annoying to detect as it only happens in certain configuration of nested call context. It might not fail in a test script, but it will in unit test sometimes, depending on how the test is run. If embedded in an app it might also depends which module runs the app.

To circumvent this problem, two jobs are created, driven by command line call and run as subprocesses by the service app at startup time.

## Installation instructions

Clone the repository
Install requirements::
        
    pip install -r requirements.txt

Creates test data::
    
    python make_test_data.py data/orders.csv data/orders_test.csv
    python extract_features.py data/orders_test.csv data/features_test.pkl
    python make_predictions.py data/features_test.pkl data/predictions_test.db

Run tests::

    py.test

Creates production data::
    
    python extract_features.py data/orders.csv data/features.pkl
    python make_predictions.py data/features.pkl data/predictions.db

Run application manually::

    python app.py

Check application::

    # check application is online
    GET http://localhost:5000/test
    # get CLV from random customer
    GET http://localhost:5000/customers/random/predicted_CLV
    # get CLV from customer_id
    GET http://localhost:5000/customers/2504175708a53b19fe067b06472e4cec/predicted_CLV
