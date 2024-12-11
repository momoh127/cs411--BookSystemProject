import logging
from flask import Flask, g
from routes.auth_routes import auth_blueprint
from routes.book_routes import book_blueprint
from databases.database_setup import create_database
from config import SECRET_KEY
import os
import sqlite3

# Initialize the Flask app
app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY

# Path to the SQLite database file
DATABASE_PATH = os.path.join("databases", "books.db")
create_database()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"), 
        logging.StreamHandler()         
    ]
)
app.logger.info("Starting the Personalized Book System API...")

def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row  # Optional: To return rows as dictionaries
        app.logger.info("Database connection opened.")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """
    Closes the database again at the end of the request or application context.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
        app.logger.info("Database connection closed.")

# Health check route
@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check route to verify the service is running.
    """
    app.logger.info("Health check passed.")
    return {"status": "healthy"}, 200

# Database health check route
@app.route("/db-check", methods=["GET"])
def db_check():
    """
    Database health check route to verify connectivity.
    """
    try:
        db = get_db()
        db.execute("SELECT 1")  
        app.logger.info("Database check passed.")
        return {"database_status": "healthy"}, 200
    except Exception as e:
        app.logger.error(f"Database check failed: {str(e)}")
        return {"database_status": "unhealthy", "error": str(e)}, 500

# Register authentication and book-related routes
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(book_blueprint, url_prefix="/books")

@app.route("/", methods=["GET"])
def index():
    """
    Home route for testing the API.
    """
    app.logger.info("Home route accessed.")
    return {"message": "Welcome to the Personalized Book System API!"}, 200

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.error(f"An error occurred while running the app: {str(e)}")