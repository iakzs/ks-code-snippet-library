import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5

accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
