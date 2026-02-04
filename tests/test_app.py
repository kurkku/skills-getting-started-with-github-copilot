import os
import sys

# Ensure we can import the application from the src directory
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
import pytest

from app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


def test_signup_and_remove_participant():
    activity = "Programming Class"
    email = "testuser@example.com"

    # Make sure test email isn't already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up the test user
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Signing up again should fail with 400
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Remove the participant
    resp_del = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]
