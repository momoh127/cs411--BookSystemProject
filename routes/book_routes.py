from flask import Blueprint, request, jsonify
from utils.api_utils import search_books, fetch_book_details
from utils.db_utils import add_book_to_library, get_user_library, update_book_status

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
        return jsonify({"error": "Query parameter 'q' is required"}), 400

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
    details = fetch_book_details(book_id)
    return jsonify(details)

@book_blueprint.route("/add-to-library", methods=["POST"])
def add_to_library():
    """
    Add a book to the user's library.

    Inputes:
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
        return jsonify({"error": "User ID and Book ID are required"}), 400

    try:
        add_book_to_library(user_id, book_id, status)
        return jsonify({"message": "Book added to library successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_blueprint.route("/library/<int:user_id>", methods=["GET"])
def view_library(user_id):
    """
    Retrieve the user's library with book details and statuses.

    Args: user_id
    
    """
    try:
        library = get_user_library(user_id)  # Fetch library from db_utils
        if not library:
            return jsonify({"message": "Library is empty"}), 200
        
        # Format library data to match the expected response
        formatted_library = [
            {
                "title": book[0],
                "author": book[1],
                "status": book[2]
            }
            for book in library
        ]
        return jsonify({"library": formatted_library}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@book_blueprint.route("/update-status", methods=["POST"])
def update_status():
    """
    Update the status of a book in the user's library.

    inputes:
        - user_id: str
        - book_id: str
        - status: str
    """
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    new_status = data.get("status")

    if not user_id or not book_id or not new_status:
        return jsonify({"error": "user_id, book_id, and status are required"}), 400

    if new_status not in ["To read", "Have read", "Favorite"]:
        return jsonify({"error": "Invalid status"}), 400

    try:
        update_book_status(user_id, book_id, new_status)
        return jsonify({"message": "Book status updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500