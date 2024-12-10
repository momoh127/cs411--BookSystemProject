from flask import Flask
from routes.auth_routes import auth_blueprint
from routes.book_routes import book_blueprint
from config import SECRET_KEY

app = Flask(__name__)

# Set the secret key for session management
app.config["SECRET_KEY"] = SECRET_KEY

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