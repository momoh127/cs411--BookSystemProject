from flask import Blueprint, request, jsonify
from utils.db_utils import insert_user, get_user
from utils.auth_utils import hash_password, verify_password

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/create-account", methods=["POST"])
def create_account():
    """
    Creates a new user account with a username and password.

    Inputs:
        username: str
        password: str

    Returns: A JSON response of either
        - succcess message and a HTTPS status 201: 
        - error message (failed to create the account) and a HTTPS status 400 or 401
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        hashed_password = hash_password(password)
        insert_user(username, hashed_password)
        return jsonify({"message": "Account created successfully!"}), 201  
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_blueprint.route("/login", methods=["POST"])
def login():
    """
    Allows user to login to their account after providing the username and password
    
    Inputs:
        username: str
        password: str
    
    ReturnsA JSON response of either
        - succcess message, a user ID, and a HTTPS status 200: 
        - error message (failed to login to the account) and a HTTPS status 400 or 401
       
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = get_user(username)
    if user and verify_password(password, user[2]): 
        return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401  