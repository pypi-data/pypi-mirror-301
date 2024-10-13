from schedule_manager_ui import ScheduleManager


def test_auth_present(client, app, scheduler):
    schedule_manager = ScheduleManager(app, scheduler)
    response = client.get(schedule_manager.HOME_PATH)
    assert b'<button id="auth-button" class="auth authenticate">Authenticate</button>' in response.data


def test_auth_not_present(client, app, scheduler):
    schedule_manager_custom_path = ScheduleManager(app, scheduler, require_authentication=False)
    response = client.get(schedule_manager_custom_path.HOME_PATH)
    assert b'<button id="auth-button" class="auth authenticate">Authenticate</button>' not in response.data
