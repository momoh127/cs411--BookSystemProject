import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.api_utils import search_books, fetch_book_details

def test_search_books():
    """
    Test the search_books function.
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

def test_fetch_book_details():
    """
    Test the fetch_book_details function.
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

if __name__ == "__main__":
    test_search_books()
    test_fetch_book_details()