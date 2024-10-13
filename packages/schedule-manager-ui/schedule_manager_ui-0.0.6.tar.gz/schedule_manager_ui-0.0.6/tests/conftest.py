import pytest
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from schedule_manager_ui import ScheduleManager
import os

os.environ["SM_UI_APIKEY"] = 'abc123'


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.testing = True
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    return scheduler


@pytest.fixture()
def schedule_manager(app, scheduler):
    return ScheduleManager(app, scheduler)


@pytest.fixture()
def schedule_manager_custom_path(app, scheduler):
    return ScheduleManager(app, scheduler, path='/custom-url')


@pytest.fixture()
def schedule_manager_api_key():
    return os.environ["SM_UI_APIKEY"]
