import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 4
timeout = 120
keepalive = 5

# Logging - using journalctl means we should log to stdout/stderr
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "harada"

# Path to the WSGI application
wsgi_app = "config.wsgi:application"
