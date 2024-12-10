import requests
from config import GOOGLE_BOOKS_API_KEY

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(query, max_results=10):
    """
    Searches the Google Books API for books matching the query.

    Args:
        query (str): Search term.
        max_results (int): Number of results to fetch.

    Returns:
        dict: API response as JSON.
    """
    params = {
        "q": query,
        "maxResults": max_results,
        "key": GOOGLE_BOOKS_API_KEY
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch books: {response.status_code}"}

def fetch_book_details(book_id):
    """
    Fetches detailed information about a book by its Google Books ID.

    Args:
        book_id : Google Books ID.

    Returns:
        dict: API response as JSON.
    """
    url = f"{GOOGLE_BOOKS_API_URL}/{book_id}"
    params = {"key": GOOGLE_BOOKS_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch book details: {response.status_code}"}