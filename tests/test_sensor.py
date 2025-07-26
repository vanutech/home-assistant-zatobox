
"""Tests for the sensor module."""
from pytest_homeassistant_custom_component import test_util

from custom_components.zatobox.sensor import ZatoboxSensor


async def test_async_update_success(hass, aioclient_mock):

    sensor = ZatoboxSensor()
    await sensor.update()

    expected = {
        "clones": 100,
        "clones_unique": 50,
        "forks": 1000,
        "latest_commit_message": "Did a thing.",
        "latest_commit_sha": "e751664d95917dbdb856c382bfe2f4655e2a83c1",
        "latest_open_issue_url": "https://github.com/homeassistant/core/issues/1",
        "latest_open_pull_request_url": "https://github.com/homeassistant/core/pull/1347",
        "latest_release_tag": "v0.1.112",
        "latest_release_url": "https://github.com/homeassistant/core/releases/v0.1.112",
        "name": "Home Assistant",
        "open_issues": 4655,
        "open_pull_requests": 345,
        "path": "homeassistant/core",
        "stargazers": 9000,
        "views": 10000,
        "views_unique": 5000,
    }
    assert expected == sensor.attrs
    assert expected == sensor.device_state_attributes
    assert sensor.available is True

