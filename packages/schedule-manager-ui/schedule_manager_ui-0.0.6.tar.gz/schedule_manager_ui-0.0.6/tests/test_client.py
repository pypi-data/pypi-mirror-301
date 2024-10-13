from schedule_manager_ui import ScheduleManager

default_manager_path = "/schedule-manager-ui"


def test_endpoint(client, schedule_manager):
    response = client.get(default_manager_path)
    assert response.status_code == 200


def test_custom_path(client, app, scheduler):
    schedule_manager_custom_path = ScheduleManager(app, scheduler, path='/custom-url')
    response = client.get(schedule_manager_custom_path.HOME_PATH)
    assert response.status_code == 200

    response = client.get(default_manager_path)
    assert response.status_code == 404
