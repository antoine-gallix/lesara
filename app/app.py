import flask
import io
import predict
import json

blueprint = flask.blueprint()


@blueprint.route('/')
def index():
    return 'mille!'


@blueprint.route('/customers/{customer_id}/predicted_CLV')
def predict_CLV(customer_id):
    features = io.get_features(customer_id)
    predicted_CLV = predict.predict_CLV(features)
    payload = {
        'customer_id': customer_id,
        'predicted_CLV': predicted_CLV
    }
    return json.dumps(payload)


def create_app():
    app = flask.Flask('CLV_predict')
    app.register_blueprint(blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
