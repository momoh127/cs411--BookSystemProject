import logging
from typing import List

logger = logging.getLogger(__name__)
configure_logger(logger)


class BookModel:
    """A class to manage a Book (Volume)"""
    def __init__(self, id, title, authors):
        """Initializes the BookModel with necessary data"""
        self.bID = id
        self.title = title
        self.authors = authors