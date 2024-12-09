import sqlite3
import os 

def create_database(db_folder="databases", db_name="books.db"):
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
        hashed_password TEXT NOT NULL
    );
    """
    # SQL command to create Books table
    create_books_table = """
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL
    );
    """
    # SQL command to create User_library table
    create_user_library_table = """
    CREATE TABLE IF NOT EXISTS User_Library (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('To read', 'Have read', 'Favorite')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (book_id) REFERENCES Books(book_id)
    );
    """

    # Execute SQL commands
    cursor.execute(create_users_table)
    cursor.execute(create_books_table)
    cursor.execute(create_user_library_table)

    conn.commit()
    conn.close()
    print(f"Database setup complete! Database file is located at: {db_path}")

# Run the script
if __name__ == "__main__":
    create_database()