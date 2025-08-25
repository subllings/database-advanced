"""
Book Manager Module

This module handles all book-related operations including queries, filters, and updates.
"""

import logging
from datetime import datetime
from bson import ObjectId
import re


class BookManager:
    """Manager for book operations in the library catalog."""
    
    def __init__(self, mongo_client):
        """
        Initialize book manager.
        
        Args:
            mongo_client: MongoDBClient instance
        """
        self.mongo_client = mongo_client
        self.db = mongo_client.get_database()
        self.books_collection = self.db.books
        self.logger = logging.getLogger(__name__)
    
    def find_all_books(self, limit=50, skip=0):
        """
        Find all books with pagination.
        
        Args:
            limit (int): Maximum number of books to return
            skip (int): Number of books to skip
            
        Returns:
            list: List of book documents
        """
        try:
            books = list(self.books_collection.find({}).limit(limit).skip(skip))
            return books
        except Exception as e:
            self.logger.error(f"Error finding all books: {e}")
            return []
    
    def find_books_by_title(self, title, exact_match=False):
        """
        Find books by title.
        
        Args:
            title (str): Book title to search for
            exact_match (bool): Whether to perform exact match or partial match
            
        Returns:
            list: List of matching book documents
        """
        try:
            if exact_match:
                query = {"title": title}
            else:
                # Case-insensitive partial match
                query = {"title": {"$regex": re.escape(title), "$options": "i"}}
            
            books = list(self.books_collection.find(query))
            self.logger.info(f"Found {len(books)} books matching title '{title}'")
            return books
            
        except Exception as e:
            self.logger.error(f"Error finding books by title: {e}")
            return []
    
    def find_books_by_author(self, author_name):
        """
        Find books by author name.
        
        Args:
            author_name (str): Author name to search for
            
        Returns:
            list: List of matching book documents
        """
        try:
            # Case-insensitive search in nested author.name field
            query = {"author.name": {"$regex": re.escape(author_name), "$options": "i"}}
            books = list(self.books_collection.find(query))
            self.logger.info(f"Found {len(books)} books by author '{author_name}'")
            return books
            
        except Exception as e:
            self.logger.error(f"Error finding books by author: {e}")
            return []
    
    def find_books_by_genre(self, genre):
        """
        Find books by genre.
        
        Args:
            genre (str): Genre to search for
            
        Returns:
            list: List of matching book documents
        """
        try:
            # Search in genres array with case-insensitive match
            query = {"genres": {"$regex": re.escape(genre), "$options": "i"}}
            books = list(self.books_collection.find(query))
            self.logger.info(f"Found {len(books)} books in genre '{genre}'")
            return books
            
        except Exception as e:
            self.logger.error(f"Error finding books by genre: {e}")
            return []
    
    def find_books_by_year_range(self, start_year, end_year):
        """
        Find books published within a year range.
        
        Args:
            start_year (int): Start year (inclusive)
            end_year (int): End year (inclusive)
            
        Returns:
            list: List of matching book documents
        """
        try:
            query = {
                "publication.year": {
                    "$gte": start_year,
                    "$lte": end_year
                }
            }
            books = list(self.books_collection.find(query))
            self.logger.info(f"Found {len(books)} books published between {start_year} and {end_year}")
            return books
            
        except Exception as e:
            self.logger.error(f"Error finding books by year range: {e}")
            return []
    
    def find_highly_rated_books(self, rating_threshold=4.0):
        """
        Find books with high ratings.
        
        Args:
            rating_threshold (float): Minimum average rating
            
        Returns:
            list: List of highly rated book documents
        """
        try:
            query = {"ratings.average": {"$gte": rating_threshold}}
            books = list(self.books_collection.find(query).sort("ratings.average", -1))
            self.logger.info(f"Found {len(books)} books with rating >= {rating_threshold}")
            return books
            
        except Exception as e:
            self.logger.error(f"Error finding highly rated books: {e}")
            return []
    
    def find_available_books(self):
        """
        Find books that are currently available for borrowing.
        
        Returns:
            list: List of available book documents
        """
        try:
            query = {"available_copies": {"$gt": 0}}
            books = list(self.books_collection.find(query))
            self.logger.info(f"Found {len(books)} available books")
            return books
            
        except Exception as e:
            self.logger.error(f"Error finding available books: {e}")
            return []
    
    def search_books_advanced(self, filters):
        """
        Advanced book search with multiple filters.
        
        Args:
            filters (dict): Dictionary of search filters
                - title: Book title (partial match)
                - author: Author name (partial match)
                - genre: Genre (partial match)
                - min_year: Minimum publication year
                - max_year: Maximum publication year
                - min_rating: Minimum average rating
                - max_rating: Maximum average rating
                - available_only: Include only available books
                
        Returns:
            list: List of matching book documents
        """
        try:
            query = {}
            
            # Title filter
            if filters.get("title"):
                query["title"] = {"$regex": re.escape(filters["title"]), "$options": "i"}
            
            # Author filter
            if filters.get("author"):
                query["author.name"] = {"$regex": re.escape(filters["author"]), "$options": "i"}
            
            # Genre filter
            if filters.get("genre"):
                query["genres"] = {"$regex": re.escape(filters["genre"]), "$options": "i"}
            
            # Year range filter
            year_filter = {}
            if filters.get("min_year"):
                year_filter["$gte"] = filters["min_year"]
            if filters.get("max_year"):
                year_filter["$lte"] = filters["max_year"]
            if year_filter:
                query["publication.year"] = year_filter
            
            # Rating range filter
            rating_filter = {}
            if filters.get("min_rating"):
                rating_filter["$gte"] = filters["min_rating"]
            if filters.get("max_rating"):
                rating_filter["$lte"] = filters["max_rating"]
            if rating_filter:
                query["ratings.average"] = rating_filter
            
            # Available only filter
            if filters.get("available_only"):
                query["available_copies"] = {"$gt": 0}
            
            books = list(self.books_collection.find(query))
            self.logger.info(f"Advanced search found {len(books)} books")
            return books
            
        except Exception as e:
            self.logger.error(f"Error in advanced book search: {e}")
            return []
    
    def get_book_by_id(self, book_id):
        """
        Get a book by its ObjectId.
        
        Args:
            book_id: Book ObjectId or string representation
            
        Returns:
            dict: Book document or None if not found
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            book = self.books_collection.find_one({"_id": book_id})
            return book
            
        except Exception as e:
            self.logger.error(f"Error getting book by ID: {e}")
            return None
    
    def add_rating(self, book_id, rating):
        """
        Add a rating to a book and update average.
        
        Args:
            book_id: Book ObjectId or string representation
            rating (int): Rating value (1-5)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            if not (1 <= rating <= 5):
                self.logger.error("Rating must be between 1 and 5")
                return False
            
            # Get current book data
            book = self.get_book_by_id(book_id)
            if not book:
                self.logger.error("Book not found")
                return False
            
            # Update rating statistics
            current_ratings = book.get("ratings", {})
            current_average = current_ratings.get("average", 0)
            current_count = current_ratings.get("count", 0)
            current_distribution = current_ratings.get("distribution", [0, 0, 0, 0, 0])
            
            # Calculate new average
            new_count = current_count + 1
            new_average = ((current_average * current_count) + rating) / new_count
            
            # Update distribution
            new_distribution = current_distribution.copy()
            new_distribution[rating - 1] += 1
            
            # Update database
            result = self.books_collection.update_one(
                {"_id": book_id},
                {
                    "$set": {
                        "ratings.average": round(new_average, 2),
                        "ratings.count": new_count,
                        "ratings.distribution": new_distribution,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                self.logger.info(f"Added rating {rating} to book {book_id}")
                return True
            else:
                self.logger.error("Failed to update book rating")
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding rating: {e}")
            return False
    
    def update_availability(self, book_id, available_copies=None, total_copies=None):
        """
        Update book availability.
        
        Args:
            book_id: Book ObjectId or string representation
            available_copies (int): New available copies count
            total_copies (int): New total copies count
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            update_fields = {"updated_at": datetime.utcnow()}
            
            if available_copies is not None:
                update_fields["available_copies"] = available_copies
            
            if total_copies is not None:
                update_fields["total_copies"] = total_copies
            
            result = self.books_collection.update_one(
                {"_id": book_id},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                self.logger.info(f"Updated availability for book {book_id}")
                return True
            else:
                self.logger.error("Failed to update book availability")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating availability: {e}")
            return False
    
    def borrow_book(self, book_id):
        """
        Borrow a book (decrease available copies).
        
        Args:
            book_id: Book ObjectId or string representation
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            # Check if book is available
            book = self.get_book_by_id(book_id)
            if not book:
                self.logger.error("Book not found")
                return False
            
            if book.get("available_copies", 0) <= 0:
                self.logger.error("No available copies to borrow")
                return False
            
            # Decrease available copies
            result = self.books_collection.update_one(
                {"_id": book_id, "available_copies": {"$gt": 0}},
                {
                    "$inc": {"available_copies": -1},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                self.logger.info(f"Book {book_id} borrowed successfully")
                return True
            else:
                self.logger.error("Failed to borrow book")
                return False
                
        except Exception as e:
            self.logger.error(f"Error borrowing book: {e}")
            return False
    
    def return_book(self, book_id):
        """
        Return a book (increase available copies).
        
        Args:
            book_id: Book ObjectId or string representation
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            # Get book to check total copies limit
            book = self.get_book_by_id(book_id)
            if not book:
                self.logger.error("Book not found")
                return False
            
            current_available = book.get("available_copies", 0)
            total_copies = book.get("total_copies", 0)
            
            if current_available >= total_copies:
                self.logger.error("Cannot return book: already at maximum copies")
                return False
            
            # Increase available copies
            result = self.books_collection.update_one(
                {"_id": book_id},
                {
                    "$inc": {"available_copies": 1},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                self.logger.info(f"Book {book_id} returned successfully")
                return True
            else:
                self.logger.error("Failed to return book")
                return False
                
        except Exception as e:
            self.logger.error(f"Error returning book: {e}")
            return False
    
    def get_book_statistics(self):
        """
        Get general statistics about the book collection.
        
        Returns:
            dict: Statistics about books
        """
        try:
            stats = {}
            
            # Total books count
            stats["total_books"] = self.books_collection.count_documents({})
            
            # Available books count
            stats["available_books"] = self.books_collection.count_documents({"available_copies": {"$gt": 0}})
            
            # Total and available copies
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_copies": {"$sum": "$total_copies"},
                        "available_copies": {"$sum": "$available_copies"}
                    }
                }
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            if result:
                stats["total_copies"] = result[0]["total_copies"]
                stats["total_available_copies"] = result[0]["available_copies"]
            else:
                stats["total_copies"] = 0
                stats["total_available_copies"] = 0
            
            # Average rating
            avg_pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "average_rating": {"$avg": "$ratings.average"}
                    }
                }
            ]
            
            avg_result = list(self.books_collection.aggregate(avg_pipeline))
            if avg_result:
                stats["average_rating"] = round(avg_result[0]["average_rating"], 2)
            else:
                stats["average_rating"] = 0
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting book statistics: {e}")
            return {}
