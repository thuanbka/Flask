# gunicorn_config.py
bind = "0.0.0.0:80"
workers = 4
worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
