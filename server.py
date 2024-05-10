import logging
import time
from functools import wraps
from random import randint
from flask import Flask, jsonify, request, abort
from prometheus_client import make_wsgi_app, Counter, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['method', 'endpoint']
)
REQUEST_LATENCY = Histogram(
    'request_latency_miliseconds',
    'Request latency',
    ['method', 'endpoint']
)
RESPONSE_500_COUNT = Counter(
    'response_500_count',
    'Total 500 Responses Count'
)


# Decorator to measure request latency
def record_request_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            RESPONSE_500_COUNT.inc()
            raise e
        finally:
            request_latency = (time.time() - start_time) * 1000
            REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
            REQUEST_COUNT.labels(request.method, request.path).inc()
        return result
    return wrapper


api = Flask(__name__)
api.wsgi_app = DispatcherMiddleware(api.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@api.route("/")
@record_request_data
def first():
    return jsonify({"message": "Hello from the root page"})


@api.route("/hello")
@record_request_data
def hello():
    return jsonify(say_hello())


@api.route("/about")
@record_request_data
def about():
    time.sleep(randint(1, 4))
    return jsonify(call_about())

# Simulate 500 response
@api.route('/error')
@record_request_data
def error():
    abort(500)


def say_hello():
    return {"message": "hello from the /hello endpoint"}


def call_about():
    return {"message": "This the the about API"}
