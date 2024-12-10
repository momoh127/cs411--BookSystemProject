from flask import Blueprint, request, jsonify
from utils.api_utils import search_books, fetch_book_details
from utils.db_utils import add_book_to_library, get_user_library

book_blueprint = Blueprint("books", __name__)

@book_blueprint.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = search_books(query, max_results=10)
    return jsonify(results)

@book_blueprint.route("/details/<book_id>", methods=["GET"])
def details(book_id):
    details = fetch_book_details(book_id)
    return jsonify(details)

@book_blueprint.route("/add-to-library", methods=["POST"])
def add_to_library():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    status = data.get("status", "To read")

    if not user_id or not book_id:
        return jsonify({"error": "User ID and Book ID are required"}), 400

    try:
        add_book_to_library(user_id, book_id, status)
        return jsonify({"message": "Book added to library successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@book_blueprint.route("/library/<user_id>", methods=["GET"])
def view_library(user_id):
    library = get_user_library(user_id)
    if not library:
        return jsonify({"message": "Library is empty"}), 200

    return jsonify({"library": library}), 200