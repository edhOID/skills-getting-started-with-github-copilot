import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Helper: Reset activities state for isolation (if needed)
def reset_activities():
    app.dependency_overrides = {}
    # Optionally, reset in-memory DB here if you refactor for testability


def test_get_activities():
    # Arrange
    # (No setup needed for GET)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    # Arrange
    email = "testuser1@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")


def test_signup_duplicate():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")


def test_signup_activity_not_found():
    # Arrange
    email = "testuser3@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success():
    # Arrange
    email = "testuser4@mergington.edu"
    activity = "Gym Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]


def test_unregister_not_found():
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Gym Class"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
