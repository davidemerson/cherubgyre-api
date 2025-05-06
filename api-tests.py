
import pytest
import httpx

# === CONFIGURATION VARIABLES === #
BASE_URL = "http://64.227.1.200:8080"
TEST_USERNAME = "testuser"
TEST_NORMAL_PIN = "1234"
TARGET_USER_ID = "target-user-id"  # Replace with a real user to follow/unfollow

# === AUTHENTICATION AND PROFILE === #
@pytest.fixture(scope="session")
def auth_data():
    login_res = httpx.post(f"{BASE_URL}/login", json={
        "username": TEST_USERNAME,
        "normal_pin": TEST_NORMAL_PIN
    })
    login_res.raise_for_status()
    token = login_res.json()["access_token"]

    profile_res = httpx.get(f"{BASE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    profile_res.raise_for_status()
    user_id = profile_res.json()["id"]

    return {"token": token, "user_id": user_id}

@pytest.fixture
def auth_token(auth_data):
    return auth_data["token"]

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def test_user_id(auth_data):
    return auth_data["user_id"]

# === TEST CASES === #
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

    response = httpx.post(f"{BASE_URL}/duress", headers=auth_headers, json=payload)
    assert response.status_code == 429

def test_cancel_duress(auth_headers):
    cancel_payload = {
        "normal_pin": TEST_NORMAL_PIN,
        "confirm": True
    }
    response = httpx.post(f"{BASE_URL}/duress/cancel", headers=auth_headers, json=cancel_payload)
    assert response.status_code in (200, 404, 403)

def test_update_preferences(auth_headers, test_user_id):
    update_payload = {
        "broadcast_duress": True,
        "receive_duress_broadcasts": True
    }
    response = httpx.patch(f"{BASE_URL}/users/{test_user_id}/preferences", headers=auth_headers, json=update_payload)
    assert response.status_code in (200, 403)

def test_follow_and_unfollow(auth_headers, test_user_id):
    follow_payload = {"identifier": TARGET_USER_ID}
    unfollow_payload = {"identifier": TARGET_USER_ID}

    response = httpx.post(f"{BASE_URL}/follow/{test_user_id}", headers=auth_headers, json=follow_payload)
    assert response.status_code in (200, 404)

    response = httpx.post(f"{BASE_URL}/unfollow/{test_user_id}", headers=auth_headers, json=unfollow_payload)
    assert response.status_code in (200, 404)

def test_remove_follower(auth_headers, test_user_id):
    response = httpx.delete(f"{BASE_URL}/followers/{test_user_id}", headers=auth_headers)
    assert response.status_code in (200, 404)

def test_get_map_data(auth_headers, test_user_id):
    response = httpx.get(f"{BASE_URL}/users/map", headers=auth_headers, params={"user_id": test_user_id})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
