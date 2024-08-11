from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
import pytest

from main import db, app as _app


@pytest.fixture(scope='session')
def app()-> Generator[Flask, None, None]:
    app = _app
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture(scope='session')
def client(app) -> FlaskClient:
    return app.test_client()
