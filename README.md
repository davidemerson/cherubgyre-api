# cherubgyre-api documentation

This documentation is kept OpenAPI 3.0.3 format, according to [this specification](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.3.md)

It's rendered for viewing [here](https://api.cherubgyre.com)

Non-API project documentation and notes are hosted [here](https://nnix.com/projects/cherubgyre/)

The server is [here](https://github.com/davidemerson/cherubgyre)

There's a stub of a website [here](https://cherubgyre.com) but it's mostly a collection of notes pending a production service.


# 🧪 CherubGyre API Test Suite

[CherubGyre API](http://64.227.1.200:8080). The tests are written in Python using `pytest` and `httpx`, covering key functionalities such as authentication, duress alerts, user preferences, and social interactions.

## 📦 Prerequisites

- Python 3.7 or higher
- `pip` package manager

## 🚀 Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/cherubgyre-api-tests.git
   cd cherubgyre-api-tests
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not present, install the necessary packages directly:*

   ```bash
   pip install pytest httpx
   ```

## ⚙️ Configuration

Before running the tests, update the configuration variables at the top of the `test_cherubgyre_api.py` file:

```python
# === CONFIGURATION VARIABLES === #
BASE_URL = "http://64.227.1.200:8080"
TEST_USERNAME = "your_test_username"
TEST_NORMAL_PIN = "your_test_pin"
TEST_USER_ID = "your_test_user_id"
TARGET_USER_ID = "target_user_id_to_follow"
```

Replace the placeholder values with valid credentials and user IDs relevant to your testing environment.

## 🧪 Running the Tests

Execute the test suite using `pytest`:

```bash
pytest test_cherubgyre_api.py
```

For more detailed output, use the verbose flag:

```bash
pytest -v test_cherubgyre_api.py
```

## 🧾 Test Coverage

The test suite includes the following:

- **Authentication**
  - Valid and invalid login attempts
- **Health Check**
  - Verifying system liveness
- **Invite Code Generation**
  - Creating new invite codes
- **Duress Alerts**
  - Sending duress notifications
  - Handling rate limits
  - Canceling duress status
- **User Preferences**
  - Updating and retrieving duress broadcast settings
- **Social Interactions**
  - Following and unfollowing users
  - Removing followers
- **Map Data**
  - Retrieving last known locations of followed users

## 🛠️ Customization

To add or modify tests:

1. Open `test_cherubgyre_api.py`.
2. Define new test functions following the existing structure.
3. Use `httpx` to make HTTP requests to the API endpoints.
4. Utilize `pytest` assertions to validate responses.

Example:

```python
def test_example_endpoint(auth_headers):
    response = httpx.get(f"{BASE_URL}/example", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["key"] == "expected_value"
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.
