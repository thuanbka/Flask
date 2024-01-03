# app.wsgi
#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/mnt/flash_application/')
sys.path.insert(0, '/mnt/flash_application/virtualenv/lib/python3.11/site-packages')
from my_app import server as application
