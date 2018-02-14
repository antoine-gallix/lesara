## Architecture choices

### Limitation with pickled model

There is a problem with the dill-pickled model. The model will raise an error if numpy is not imported at the top level caller. It works in a small script but it makes it difficult to embed in an application. This issue is very annoying to detect as it only happens in certain configuration of nested call context. It might not fail in a test script, but it will in unit test sometimes, depending on how the test is run. If embedded in an app it might also depends which module runs the app.

To circumvent this problem, two jobs are created, driven by command line call and run as subprocesses by the service app at startup time.

## Run tests
Install requirements::
        
    pip install -r requirements.txt

Creates test data::
    
    python make_test_data.py data/orders.csv data/orders_test.csv
    python extract_features.py data/orders_test.csv data/features_test.pkl
    python make_predictions.py data/features_test.pkl data/predictions_test.db

Run tests::

    py.test
