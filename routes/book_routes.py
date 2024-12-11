from flask import Blueprint, request, jsonify
import logging
from utils.api_utils import search_books, fetch_book_details
from utils.db_utils import add_book_to_library, get_user_library, update_book_status

# Setting up the logger
logger = logging.getLogger(__name__)

book_blueprint = Blueprint("books", __name__)

@book_blueprint.route("/search", methods=["GET"])
def search():
    """
    Search for books using the Google Books API.

    Inputs: query (str): Search term.

    Returns: 
        - API response as JSON with HTTP status 200
        - error message with corresponding HTTP status code
    """
    query = request.args.get("q")
    if not query:
        logger.warning("Search request missing 'q' parameter")
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    logger.info(f"Search request received with query: {query}")
    results = search_books(query, max_results=10)
    return jsonify(results)

@book_blueprint.route("/details/<book_id>", methods=["GET"])
def details(book_id):
    """
    Fetch details for a specific book using the Google Books API.

    Args: book_id : Google Books ID.

    Returns:
        - API response as JSON with HTTP status 200
        - or an error message with corresponding HTTP status code
    """
    logger.info(f"Fetching details for book ID: {book_id}")
    details = fetch_book_details(book_id)
    return jsonify(details)

@book_blueprint.route("/add-to-library", methods=["POST"])
def add_to_library():
    """
    Add a book to the user's library.

    Inputs:
        user_id
        book_id
        status (optional)

    Returns:
        - Success message with HTTP status 201
        - error message with HTTP status 400
    """
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    status = data.get("status", "To read")  # Default status is "To read"

    if not user_id or not book_id:
        logger.warning("Add to library request missing 'user_id' or 'book_id'")
        return jsonify({"error": "User ID and Book ID are required"}), 400

    try:
        add_book_to_library(user_id, book_id, status)
        logger.info(f"Book ID {book_id} added to User ID {user_id}'s library with status '{status}'")
        return jsonify({"message": "Book added to library successfully!"}), 201
    except Exception as e:
        logger.error(f"Error adding book to library: {e}")
        return jsonify({"error": str(e)}), 400

@book_blueprint.route("/library/<int:user_id>", methods=["GET"])
def view_library(user_id):
    """
    Retrieve the user's library with book details and statuses.

    Args: user_id
    
    """
    try:
        logger.info(f"Fetching library for User ID: {user_id}")
        library = get_user_library(user_id)  # Fetch library from db_utils
        if not library:
            logger.info(f"User ID {user_id} has an empty library")
            return jsonify({"message": "Library is empty"}), 200
        
        formatted_library = [
            {
                "title": book[0],
                "author": book[1],
                "status": book[2]
            }
            for book in library
        ]
        logger.info(f"Library fetched for User ID {user_id}: {formatted_library}")
        return jsonify({"library": formatted_library}), 200
    except Exception as e:
        logger.error(f"Error fetching library for User ID {user_id}: {e}")
        return jsonify({"error": str(e)}), 500

@book_blueprint.route("/update-status", methods=["POST"])
def update_status():
    """
    Update the status of a book in the user's library.

    Inputs:
        - user_id: str
        - book_id: str
        - status: str
    """
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    new_status = data.get("status")

    if not user_id or not book_id or not new_status:
        logger.warning("Update status request missing 'user_id', 'book_id', or 'status'")
        return jsonify({"error": "user_id, book_id, and status are required"}), 400

    if new_status not in ["To read", "Have read", "Favorite"]:
        logger.warning(f"Invalid status provided: {new_status}")
        return jsonify({"error": "Invalid status"}), 400

    try:
        update_book_status(user_id, book_id, new_status)
        logger.info(f"Book status updated for User ID {user_id}, Book ID {book_id} to '{new_status}'")
        return jsonify({"message": "Book status updated successfully!"}), 200
    except Exception as e:
        logger.error(f"Error updating book status for User ID {user_id}, Book ID {book_id}: {e}")
        return jsonify({"error": str(e)}), 500