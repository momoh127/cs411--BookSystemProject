import pytest
import logging
from io import StringIO
from app import app


@pytest.fixture
def log_stream():
    """
    To capture logs during tests.
    Sets up an in-memory log stream and attaches it to the app's logger.
    Yields the stream and removes the handler after tests.
    """
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    yield log_stream
    app.logger.removeHandler(handler)


@pytest.fixture
def client():
    """
    Fixture to set up a test client for the Flask app.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_user_creation_logging(client, log_stream):
    """
    Test logging for user account creation.
    Verifies that a log entry is generated when a new user account is created.
    """
    username = "logtestuser"
    response = client.post(
        "/auth/create-account",
        json={"username": username, "password": "testpassword"}
    )
    assert response.status_code in [200, 201]  
    assert "Account created successfully" in response.get_json()["message"]

    log_stream.seek(0)
    logs = log_stream.read()
    assert f"User '{username}' added successfully!" in logs


def test_login_success_logging(client, log_stream):
    """
    Test logging for successful login attempts.
    Verifies that a log entry is generated when a user logs in successfully.
    """
    username = "loginlogtest"
    client.post(
        "/auth/create-account",
        json={"username": username, "password": "testpassword"}
    )

    response = client.post(
        "/auth/login",
        json={"username": username, "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "Login successful!" in response.get_json()["message"]

    log_stream.seek(0)
    logs = log_stream.read()
    assert f"User '{username}' logged in successfully!" in logs


def test_book_add_logging(client, log_stream):
    """
    Test logging for adding a book to the user's library.
    Verifies that a log entry is generated when a book is added to the library.
    """
    response = client.post(
        "/books/add-to-library",
        json={"user_id": 1, "book_id": "testbookid", "status": "To read"}
    )
    assert response.status_code in [200, 201]  
    assert "Book added to library successfully!" in response.get_json()["message"]

    log_stream.seek(0)
    logs = log_stream.read()
    assert "Book ID testbookid added to User ID 1's library with status 'To read'." in logs