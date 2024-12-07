import logging
from typing import List

logger = logging.getLogger(__name__)
configure_logger(logger)


class UserModel:
    """A class to manage a user's account and its related data"""
    def __init__(self):
        """Initializes the user account with empty bookshelves"""
        self.to_read = []
        self.favorites = []
        self.have_read = []
        self.purchased = []
        self.reading_now = []
        self.reviewd = []
        self.my_ebooks = []
        self.recently_viewed = []
        self.books_for_you = []