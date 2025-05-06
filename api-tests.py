
import pytest
import httpx

# === CONFIGURATION VARIABLES === #
BASE_URL = "http://64.227.1.200:8080"
TEST_USERNAME = "testuser"
TEST_NORMAL_PIN = "1234"
TEST_USER_ID = "test-user-id"  # Replace with valid user ID
TARGET_USER_ID = "target-user-id"  # Replace with a real user to follow/unfollow

@pytest.fixture(scope="session")
def auth_token():
    response = httpx.post(f"{BASE_URL}/login", json={
        "username": TEST_USERNAME,
        "normal_pin": TEST_NORMAL_PIN
    })
    response.raise_for_status()
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

def test_healthcheck():
    response = httpx.post(f"{BASE_URL}/health")
    assert response.status_code == 200

def test_login_invalid_credentials():
    response = httpx.post(f"{BASE_URL}/login", json={
        "username": "wronguser",
        "normal_pin": "wrongpin"
    })
    assert response.status_code == 401

def test_generate_invite(auth_headers):
    response = httpx.post(f"{BASE_URL}/invite", headers=auth_headers)
    assert response.status_code == 200
    assert "invite_code" in response.json()

def test_duress_rate_limit(auth_headers):
    payload = {
        "duress_type": "pin_code",
        "message": "Test duress",
        "timestamp": "2025-05-06T12:00:00Z",
        "additional_data": {}
    }
    for _ in range(2):
        response = httpx.post(f"{BASE_URL}/duress", headers=auth_headers, json=payload)
        assert response.status_code == 200

    # Third call should trigger 429
    response = httpx.post(f"{BASE_URL}/duress", headers=auth_headers, json=payload)
    assert response.status_code == 429

def test_cancel_duress(auth_headers):
    cancel_payload = {
        "normal_pin": TEST_NORMAL_PIN,
        "confirm": True
    }
    response = httpx.post(f"{BASE_URL}/duress/cancel", headers=auth_headers, json=cancel_payload)
    assert response.status_code in (200, 404, 403)  # Depending on active status

def test_update_preferences(auth_headers):
    update_payload = {
        "broadcast_duress": True,
        "receive_duress_broadcasts": True
    }
    response = httpx.patch(f"{BASE_URL}/users/{TEST_USER_ID}/preferences", headers=auth_headers, json=update_payload)
    assert response.status_code in (200, 403)

def test_follow_and_unfollow(auth_headers):
    follow_payload = {"identifier": TARGET_USER_ID}
    unfollow_payload = {"identifier": TARGET_USER_ID}

    # Follow
    response = httpx.post(f"{BASE_URL}/follow/{TEST_USER_ID}", headers=auth_headers, json=follow_payload)
    assert response.status_code in (200, 404)

    # Unfollow
    response = httpx.post(f"{BASE_URL}/unfollow/{TEST_USER_ID}", headers=auth_headers, json=unfollow_payload)
    assert response.status_code in (200, 404)

def test_remove_follower(auth_headers):
    response = httpx.delete(f"{BASE_URL}/followers/{TEST_USER_ID}", headers=auth_headers)
    assert response.status_code in (200, 404)

def test_get_map_data(auth_headers):
    response = httpx.get(f"{BASE_URL}/users/map", headers=auth_headers, params={"user_id": TEST_USER_ID})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
