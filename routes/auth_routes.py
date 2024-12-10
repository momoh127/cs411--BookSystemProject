from flask import Blueprint, request, jsonify
from utils.db_utils import insert_user, get_user
from utils.auth_utils import hash_password, verify_password

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/create-account", methods=["POST"])
def create_account():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        hashed_password = hash_password(password)
        insert_user(username, hashed_password)
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = get_user(username)
    if user and verify_password(password, user[2]): 
        return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401