import os

ENDPOINT = 'http://localhost:10115'
NOTIFY_AUTH_TOKEN = 'SAIS_AUTH_TOKEN'

LOGGER_NAME = 'sais'
DEBUG = int(os.environ.get('DS_DEBUG', 0))
