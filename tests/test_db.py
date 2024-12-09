from utils.db_utils import insert_user, add_book

# Add a user
insert_user('alice', 'hashed_password_123')

# Add a book
add_book('1984', 'George Orwell', 'Dystopian')