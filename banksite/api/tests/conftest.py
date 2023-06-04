import subprocess
import time

import pytest

from banksite import settings


@pytest.fixture(scope="session")
def setup_and_teardown_db():
    start_command = 'docker compose -f tests/test_docker-compose.yml up -d'
    subprocess.run(['bash', '-c', start_command])
    time.sleep(1)
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'test',
            'USER': 'test',
            'PASSWORD': 'test',
            'HOST': 'localhost',
            'PORT': '5434'}
    }
    yield
    stop_command = 'docker rm test -f -v'
    subprocess.run(['bash', '-c', stop_command])
