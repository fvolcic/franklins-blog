import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "personal_site.wsgi:application"
chdir = "/home/franklinvolci/website"
user = "franklinvolci"
group = "franklinvolci"
accesslog = "/home/franklinvolci/website/logs/access.log"
errorlog = "/home/franklinvolci/website/logs/error.log"
capture_output = True
loglevel = "info"
