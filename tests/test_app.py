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


def test_signup_for_activity_returns_400_for_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email={participant_email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_activity_returns_400_when_at_capacity(client):
    # Arrange
    activity_name = "Chess Club"
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(12)
    ]

    # Act
    response = client.post(
        f"/activities/{quote(activity_name)}/signup?email=newstudent@mergington.edu"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_remove_participant_returns_404_when_participant_does_not_exist(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name)}/participants/{participant_email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
