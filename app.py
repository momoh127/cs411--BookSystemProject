from flask import Flask, g
from routes.auth_routes import auth_blueprint
from routes.book_routes import book_blueprint
from databases.database_setup import create_database
from config import SECRET_KEY
import os
import sqlite3

app = Flask(__name__)

# Set the secret key for session management
app.config["SECRET_KEY"] = SECRET_KEY

# Path to the SQLite database file
DATABASE_PATH = os.path.join("databases", "books.db")
create_database()

def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row  # Optional: To return rows as dictionaries
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """
    Closes the database again at the end of the request or application context.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


# for authentication and book-related routes
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(book_blueprint, url_prefix="/books")

@app.route("/", methods=["GET"])
def index():
    """
    Home route for testing the API.
    """
    return {"message": "Welcome to the Personalized Book System API!"}, 200

if __name__ == "__main__":
    app.run(debug=True)