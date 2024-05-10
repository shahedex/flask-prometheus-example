# Flask App with Prometheus Metrics

## Application Structure
```
.
├── Dockerfile
├── LICENSE
├── README.md
├── mypy.ini
├── requirements.txt
├── server.py
└── wsgi.py
```


## Installation

Install requirements with pip:

```
$ pip install -r requirements.txt
```

### Run for development
```
$ export FLASK_APP=server.py
$ flask run --host 0.0.0.0 --port 8000
```

### Run for production

** Run with gunicorn **

```
$ pip install gunicorn
$ gunicorn -w 4 -b 0.0.0.0:8000 wsgi:api
```

* -w : number of worker
* -b : Socket to bind


### Run with Docker

```
$ docker build -t flask-prom .

$ docker run -p 8000:8000 --name flask-prom flask-prom 
 
```

This will make the app available at `http://127.0.0.1:8000`

Prometheus Metrics will be available at :  `http://127.0.0.1:8000/metrics`