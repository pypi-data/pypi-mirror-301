import pytest


def test_import_package():
    try:
        import schedule_manager_ui
    except ImportError:
        pytest.fail("Package 'schedule_manager_ui' could not be imported")


def test_import_manager():
    try:
        from schedule_manager_ui import ScheduleManager
    except ImportError:
        pytest.fail("'ScheduleManager' could not be imported")


def test_import_dependecies():
    try:
        from flask import Flask
        from apscheduler.schedulers.background import BackgroundScheduler
        import os
    except ImportError:
        pytest.fail("Dependencies could not be imported")


def test_setup_dependecies():
    try:
        from flask import Flask
        from apscheduler.schedulers.background import BackgroundScheduler
        import os

        os.environ["SM_UI_APIKEY"] = 'abc123'
        app = Flask(__name__)
        app.testing = True
        app.test_client()
        scheduler = BackgroundScheduler()
        scheduler.start()
    except:
        pytest.fail("Dependencies could not be set up")


def test_setup_manager():
    try:
        from flask import Flask
        from apscheduler.schedulers.background import BackgroundScheduler
        from schedule_manager_ui import ScheduleManager
        import os

        os.environ["SM_UI_APIKEY"] = 'abc123'

        app = Flask(__name__)
        app.testing = True
        app.test_client()
        scheduler = BackgroundScheduler()
        ScheduleManager(app, scheduler, require_authentication=True)
        scheduler.start()
    except:
        pytest.fail("'ScheduleManager' could not be set up")
