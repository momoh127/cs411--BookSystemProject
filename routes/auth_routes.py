import logging
from flask import Blueprint, request, jsonify
from utils.db_utils import insert_user, get_user
from utils.auth_utils import hash_password, verify_password

# Initialize logger
logger = logging.getLogger(__name__)

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/create-account", methods=["POST"])
def create_account():
    """
    Creates a new user account with a username and password.

    Inputs:
        username: str
        password: str

    Returns:
        A JSON response of either:
        - success message and a HTTP status 201
        - error message (failed to create the account) and a HTTP status 400
    """
    logger.info("Accessed /create-account endpoint")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning("Username or password missing in create-account request")
        return jsonify({"error": "Username and password are required"}), 400

    try:
        hashed_password = hash_password(password)
        insert_user(username, hashed_password)
        logger.info(f"Account for user '{username}' created successfully")
        return jsonify({"message": "Account created successfully!"}), 201
    except Exception as e:
        logger.error(f"Failed to create account for user '{username}': {e}")
        return jsonify({"error": str(e)}), 400

@auth_blueprint.route("/login", methods=["POST"])
def login():
    """
    Allows user to login to their account after providing the username and password.

    Inputs:
        username: str
        password: str

    Returns:
        A JSON response of either:
        - success message, a user ID, and a HTTP status 200
        - error message (failed to login to the account) and a HTTP status 401
    """
    logger.info("Accessed /login endpoint")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning("Username or password missing in login request")
        return jsonify({"error": "Username and password are required"}), 400

    user = get_user(username)
    if user and verify_password(password, user[2]):
        logger.info(f"User '{username}' logged in successfully")
        return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
    else:
        logger.warning(f"Failed login attempt for user '{username}'")
        return jsonify({"error": "Invalid username or password."}), 401