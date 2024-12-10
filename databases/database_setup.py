import sqlite3
import os


def create_database(db_folder="databases", db_name="books.db"):
    """
    Creates the SQLite database with the required tables: Users, Books, and User_Library.
    """
    # Ensure the target folder exists
    os.makedirs(db_folder, exist_ok=True)

    # Define the full path to the database file
    db_path = os.path.join(db_folder, db_name)

    # Connect to or create the database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL commands to create tables
    # SQL command to create Users table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    # SQL command to create Books table
    create_books_table = """
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_book_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        author TEXT,
        description TEXT,
        categories TEXT,
        published_date TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """

    # SQL command to create User_Library table
    create_user_library_table = """
    CREATE TABLE IF NOT EXISTS User_Library (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('To read', 'Have read', 'Favorite')) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
    );
    """

    try:
        # Execute SQL commands
        cursor.execute(create_users_table)
        cursor.execute(create_books_table)
        cursor.execute(create_user_library_table)

        conn.commit()
        print(f"Database setup complete! Database file is located at: {db_path}")

    except sqlite3.Error as e:
        print(f"Error during database setup: {e}")

    finally:
        conn.close()


# Run the script
if __name__ == "__main__":
    create_database()