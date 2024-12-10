import os
from dotenv import load_dotenv, find_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, 'apikeys.env')

# Load the environment file
load_dotenv(dotenv_path)

api_key = os.getenv("GBOOKS_API_KEY")

SECRET_KEY = os.environ.get("SECRET_KEY", "your_random_secret_key")

# Google Books API
# GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY", "AIzaSyA-UKRc_k0oCo55iSiws_T8CIHiYEbKVhQ")
GOOGLE_BOOKS_API_KEY = os.environ.get("GOOGLE_BOOKS_API_KEY", api_key)
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# Database settings
DB_FOLDER = os.environ.get("DB_FOLDER", "databases")
DB_NAME = os.environ.get("DB_NAME", "books.db")
DATABASE_PATH = os.path.join(DB_FOLDER, DB_NAME)