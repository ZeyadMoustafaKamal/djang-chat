from . import BASE_DIR
from dotenv import load_dotenv
import dj_database_url
import os

load_dotenv('backend/settings/.env.dev')

SECRET_KEY = os.getenv('SECRET_KEY')


DATABASES = {
    'default': dj_database_url.parse('sqlite:///{}'.format(BASE_DIR / 'db.sqlite3'))
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# djang0-channels conf

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}


