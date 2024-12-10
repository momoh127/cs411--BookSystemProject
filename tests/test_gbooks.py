import pytest
from models.google_books import search_books

def test_search_books_success(mocker):
    # Mock API response
    mock_response = {
        "items": [
            {
                "volumeInfo": {
                    "title": "1984",
                    "authors": ["George Orwell"],
                    "description": "A dystopian novel...",
                    "categories": ["Fiction"],
                    "infoLink": "https://books.google.com/..."
                }
            },
            {
                "volumeInfo": {
                    "title": "Animal Farm",
                    "authors": ["George Orwell"],
                    "description": "Another dystopian tale...",
                    "categories": ["Fiction"],
                    "infoLink": "https://books.google.com/..."
                }
            }
        ]
    }

    # Mock the requests.get call
    mocker.patch("google_books.requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))
    
    # Call the function
    books = search_books("1984")
    print("search_books ran successfully")

    # Assertions
    assert len(books) == 2
    assert books[0]["title"] == "1984"
    assert books[1]["title"] == "Animal Farm"
    assert "George Orwell" in books[0]["authors"]

def test_search_books_no_results(mocker):
    # Mock API response for no results
    mock_response = {"items": []}

    # Mock the requests.get call
    mocker.patch("google_books.requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    # Call the function
    books = search_books("Unknown Title")

    # Assertions
    assert len(books) == 0

def test_search_books_api_error(mocker):
    # Mock an API error
    mocker.patch("google_books.requests.get", return_value=mocker.Mock(status_code=500, text="Internal Server Error"))

    # Call the function and assert exception is raised
    with pytest.raises(Exception, match="Google Books API error: 500 - Internal Server Error"):
        search_books("1984")

print("Success!")