import multiprocessing

bind = "127.0.0.1:8181"
workers = multiprocessing.cpu_count() * 2 + 1

# this is too long because of uploading mp3s to s3, should switch to direct upload
timeout = 90

accesslog = "/var/log/gunicorn/twinsister.access.log"
errorlog = "/var/log/gunicorn/twinsister.error.log"
