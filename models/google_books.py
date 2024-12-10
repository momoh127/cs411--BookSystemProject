import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

def search_books(title, max_results=5):
    """
    Search for books using the Google Books API.

    :param title: Title of the book to search for
    :param max_results: Maximum number of results to return
    :return: A list of book details
    """
    if not API_KEY:
        raise ValueError("Google Books API key is not set.")

    params = {
        "q": title,
        "maxResults": max_results,
        "key": API_KEY
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    
    if response.status_code == 200:
        books = response.json().get('items', [])
        results = []
        for book in books:
            volume_info = book.get("volumeInfo", {})
            results.append({
                "title": volume_info.get("title", "No Title"),
                "authors": volume_info.get("authors", ["Unknown"]),
                "description": volume_info.get("description", "No Description"),
                "categories": volume_info.get("categories", ["Uncategorized"]),
                "infoLink": volume_info.get("infoLink", "No Link")
            })
        return results
    else:
        raise Exception(f"Google Books API error: {response.status_code} - {response.text}")
    
