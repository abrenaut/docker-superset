import os
from werkzeug.contrib.cache import RedisCache

SUPERSET_WEBSERVER_PORT = os.getenv('PORT', 8088)

CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': os.getenv('CACHE_DEFAULT_TIMEOUT', 300),
    'CACHE_KEY_PREFIX': os.getenv('CACHE_KEY_PREFIX', 'superset_'),
    'CACHE_REDIS_HOST': os.getenv('CACHE_REDIS_HOST', 'redis'),
    'CACHE_REDIS_PORT': os.getenv('CACHE_REDIS_PORT', 6379),
    'CACHE_REDIS_DB': os.getenv('CACHE_REDIS_DB', 1),
    'CACHE_REDIS_URL': os.getenv('CACHE_REDIS_URL', 'redis://redis:6379/1')}

SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'postgresql+psycopg2://superset:superset@postgres:5432/superset')

SECRET_KEY = os.getenv('SECRET_KEY')


class CeleryConfig(object):
    BROKER_URL = os.getenv('CACHE_REDIS_URL', 'redis://redis:6379/1')
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_RESULT_BACKEND = os.getenv('CACHE_REDIS_URL',
                                      'redis://redis:6379/1')
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}


# Worker config
CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
    host=os.getenv('CACHE_REDIS_HOST', 'redis'),
    port=os.getenv('CACHE_REDIS_PORT', 6379),
    key_prefix='superset_results')
