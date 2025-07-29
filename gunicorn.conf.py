# gunicorn.conf.py

import multiprocessing

# WSGI application path
wsgi_app = 'wsgi:app'

# Server binding
bind = '127.0.0.1:8000'  # use 0.0.0.0:8000 for external access
backlog = 2048

# Worker settings
workers = multiprocessing.cpu_count() * 2 + 1  # (2 x CPU cores) + 1
worker_class = 'sync'
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
graceful_timeout = 30
keepalive = 5

# Security limits
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Logging to systemd journal (stdout/stderr)
accesslog = '-'
errorlog = '-'
loglevel = 'info'
