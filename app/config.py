# -*- coding: utf-8 -*-
import os


def create_postgresql_connection_string():
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_DATABASE', 'hello_world')
    user = os.environ.get('DB_USER', 'postgres')
    password = os.environ.get('DB_PASSWORD', '')

    url_string = "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(username=user,
                                                                                    password=password,
                                                                                    host=host,
                                                                                    port=port,
                                                                                    dbname=db_name)

    return url_string


class Config(object):
    ALLOWED_HOSTS = ["127.0.0.1"]
    LOG_SETTINGS = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
            },
        },
        'filters': {
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s %(levelname)s: %(message)s',
            },
        },
        'loggers': {
            'sanic.root': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': True
            },
        }
    }
    WORKERS = 1
    DB_URL = create_postgresql_connection_string() \
        if not os.environ.get('DATABASE_URL') else os.environ.get('DATABASE_URL')
    POOL_SIZE = 5
    APP_PRIVATE_KEY = os.environ.get('APP_PRIVATE_KEY', '-----BEGIN RSA PRIVATE KEY-----\nMIICWwIBAAKBgFbKy/72cEpDDXOvkQIIMii53b/71zo0Ct03O4QaSht4PpoFobF0\n3lShkY3/zGWtRPxwvVB/FDv8tAlQ0KuMDJvX3S7N3Xbnv9sMfUDyBf23/9A7o9JC\n4aKzWWBE+CVTktaswnkVRFWn+DAihSqs7Cl3pQzYMb82qRVJDAehCeppAgMBAAEC\ngYA4xAsIh0aKS7DQqVO+cH3eBTL0DlOGzeMNLMLQdCFkNhE7y9Mlrbp8v+/jYBrf\npaQpN9OagoNJeM6ICUNx7/eOcdKjB17tbUjaiDVLC9SBdC8atIwFhREo+I9C+PSq\nZg5O/qLy/at7oN9f2fZ1KxIgmnI9ziii5faKYmwBzAcYwQJBAKmlXLQyxA61pSja\nNkDLjj/0Rq+06tcsPGJWx96bGNzNTDsYBZWHFZ1zhragFMBdQDcowNlmdfgkZgBf\noqC2lZ8CQQCC+LkyBbyeCwYalXP9lPHzBmJAHZJeGXXuDvLwlyDA996mHZbBln5d\n3+pYXQQkISQKYfgXyrTZ1tzPwRr9ybL3AkBMuDHSdFrh5BfK/9QlPWkZVxlYgNLr\neF/egSxmaXG2+UkOOHDeDHcj+4jiskZwMDvINi/woTuceql+ZcGgOLI1AkAR2ZxD\n+Qwv7giy7tOUKAyhtqkFXAJq2MV94IOzzqUkJ6Qst7OoRr6KRM5HpMW/ttSWpauO\nco4bcnE9z2/CTw8ZAkEAml268J8MB0ytUddx9QoSiRhO18DixuOYvTx4PMHP8bQ/\nbder0bdRkl8wvgp+uuGTBg+eSqJPf7JRtUmcdKY/wA==\n-----END RSA PRIVATE KEY-----')
    APP_PUBLIC_KEY = os.environ.get('APP_PUBLIC_KEY', '-----BEGIN PUBLIC KEY-----\nMIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgFbKy/72cEpDDXOvkQIIMii53b/7\n1zo0Ct03O4QaSht4PpoFobF03lShkY3/zGWtRPxwvVB/FDv8tAlQ0KuMDJvX3S7N\n3Xbnv9sMfUDyBf23/9A7o9JC4aKzWWBE+CVTktaswnkVRFWn+DAihSqs7Cl3pQzY\nMb82qRVJDAehCeppAgMBAAE=\n-----END PUBLIC KEY-----')


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    TESTING = False
    ACCESS_LOG = True

    def __init__(self):
        self.LOG_SETTINGS.update({
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'logs/access.log',
                    'formatter': 'default',
                }
            },
            'loggers': {
                'sanic.root': {
                    'level': self.DEBUG,
                    'handlers': ['file']
                }
            }
        })


class StagingConfig(Config):
    ENV = 'staging'
    DEBUG = False
    TESTING = True
    ACCESS_LOG = True

    def __init__(self):
        self.LOG_SETTINGS.update({
            "handlers": {
                "file": "logging.handlers.RotatingFileHandler",
                "formatter": "precise",
                "filename": "logs/access.log"
            }
        })


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    TESTING = True
    ACCESS_LOG = True
    WORKERS = 4

    def __init__(self):
        self.LOG_SETTINGS.update({
            "handlers": {
                "file": "logging.handlers.RotatingFileHandler",
                "formatter": "precise",
                "filename": "logs/access.log"
            }
        })


class LocalConfig(Config):
    ENV = 'local'
    DEBUG = True
    TESTING = False
    ACCESS_LOG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = False
    TESTING = True
    ACCESS_LOG = False
