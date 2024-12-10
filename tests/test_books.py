import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app  # Importing the Flask app to test routes
from utils.api_utils import search_books, fetch_book_details

def test_search_books_utility():
    """
    Test the search_books function (utility).
    """
    query = "Python programming"
    print(f"Testing search_books with query: {query}")
    results = search_books(query, max_results=5)

    if "error" in results:
        print(f"Error: {results['error']}")
    else:
        for idx, book in enumerate(results.get("items", []), start=1):
            volume_info = book.get("volumeInfo", {})
            print(f"{idx}. Title: {volume_info.get('title')}, Authors: {volume_info.get('authors')}")

def test_fetch_book_details_utility():
    """
    Test the fetch_book_details function (utility).
    """
    book_id = "zyTCAlFPjgYC"  # Example Google Book ID
    print(f"\nTesting fetch_book_details with book_id: {book_id}")
    details = fetch_book_details(book_id)

    if "error" in details:
        print(f"Error: {details['error']}")
    else:
        volume_info = details.get("volumeInfo", {})
        print(f"Title: {volume_info.get('title')}, Authors: {volume_info.get('authors')}, "
              f"Description: {volume_info.get('description')}")

@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask app.
    """
    with app.test_client() as client:
        yield client

def test_search_route(client):
    """
    Test the /search route.
    """
    response = client.get("/books/search?q=Python")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert isinstance(data["items"], list)
    for book in data["items"]:
        assert "title" in book.get("volumeInfo", {})
        assert "authors" in book.get("volumeInfo", {})

def test_details_route(client):
    """
    Test the /details/<book_id> route.
    """
    book_id = "zyTCAlFPjgYC"  # Example Google Book ID
    response = client.get(f"/books/details/{book_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert "volumeInfo" in data
    volume_info = data["volumeInfo"]
    assert "title" in volume_info
    assert "authors" in volume_info
    assert "description" in volume_info

def test_add_to_library_route(client):
    """
    Test the /add-to-library route.
    """
    payload = {
        "user_id": 1,
        "book_id": 1,
        "status": "To read"
    }
    response = client.post(
        "/books/add-to-library",
        json=payload
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Book added to library successfully!"

def test_view_library_route(client):
    """
    Test the /library/<user_id> route.
    """
    user_id = 1
    response = client.get(f"/books/library/{user_id}")
    assert response.status_code == 200
    data = response.get_json()

    # If the library is empty
    if "message" in data and data["message"] == "Library is empty":
        assert data["message"] == "Library is empty"
    else:
        # If the library has items
        assert "library" in data
        assert isinstance(data["library"], list)
        for book in data["library"]:
            assert "title" in book
            assert "author" in book
            assert "status" in book

def test_update_status_route(client):
    """
    Test the /update-status route.
    """
    payload = {
        "user_id": 1,
        "book_id": 1,
        "status": "Have read"
    }
    response = client.post(
        "/books/update-status",
        json=payload
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Book status updated successfully!"

if __name__ == "__main__":
    test_search_books_utility()
    test_fetch_book_details_utility()