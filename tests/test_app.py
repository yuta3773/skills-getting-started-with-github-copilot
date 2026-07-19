import pytest
from fastapi.testclient import TestClient
from urllib.parse import quote

import src.app as app_module
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activity_state():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    yield
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{participant_email}"
    )

    # Assert
    assert response.status_code == 200
    assert participant_email not in app_module.activities[activity_name]["participants"]
    assert "daniel@mergington.edu" in app_module.activities[activity_name]["participants"]
