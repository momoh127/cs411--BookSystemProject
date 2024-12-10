from flask import Flask, request, jsonify
from google_books import search_books

app = Flask(__name__)

@app.route('/search-books', methods=['GET'])
def search_books_route():
    title = request.args.get('title')
    if not title:
        return jsonify({"error": "Title parameter is required"}), 400

    try:
        books = search_books(title)
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)