"""
User Manager Module

This module handles user-related operations including borrowing, returning books,
and managing user accounts.
"""

import logging
from datetime import datetime, timedelta
from bson import ObjectId


class UserManager:
    """Manager for user operations in the library catalog."""
    
    def __init__(self, mongo_client):
        """
        Initialize user manager.
        
        Args:
            mongo_client: MongoDBClient instance
        """
        self.mongo_client = mongo_client
        self.db = mongo_client.get_database()
        self.users_collection = self.db.users
        self.books_collection = self.db.books
        self.logger = logging.getLogger(__name__)
    
    def find_all_users(self, limit=50, skip=0):
        """
        Find all users with pagination.
        
        Args:
            limit (int): Maximum number of users to return
            skip (int): Number of users to skip
            
        Returns:
            list: List of user documents
        """
        try:
            users = list(self.users_collection.find({}).limit(limit).skip(skip))
            return users
        except Exception as e:
            self.logger.error(f"Error finding all users: {e}")
            return []
    
    def find_user_by_id(self, user_id):
        """
        Find user by user_id.
        
        Args:
            user_id (str): User ID to search for
            
        Returns:
            dict: User document or None if not found
        """
        try:
            user = self.users_collection.find_one({"user_id": user_id})
            return user
        except Exception as e:
            self.logger.error(f"Error finding user by ID: {e}")
            return None
    
    def find_user_by_email(self, email):
        """
        Find user by email.
        
        Args:
            email (str): Email to search for
            
        Returns:
            dict: User document or None if not found
        """
        try:
            user = self.users_collection.find_one({"email": email})
            return user
        except Exception as e:
            self.logger.error(f"Error finding user by email: {e}")
            return None
    
    def find_users_by_membership(self, membership_type):
        """
        Find users by membership type.
        
        Args:
            membership_type (str): Membership type (basic, premium, student)
            
        Returns:
            list: List of matching user documents
        """
        try:
            users = list(self.users_collection.find({"membership.type": membership_type}))
            self.logger.info(f"Found {len(users)} users with {membership_type} membership")
            return users
        except Exception as e:
            self.logger.error(f"Error finding users by membership: {e}")
            return []
    
    def get_user_borrowing_history(self, user_id):
        """
        Get borrowing history for a user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: List of borrowing records with book details
        """
        try:
            user = self.find_user_by_id(user_id)
            if not user:
                self.logger.error(f"User {user_id} not found")
                return []
            
            borrowing_history = user.get("borrowing_history", [])
            
            # Enrich with book details
            enriched_history = []
            for record in borrowing_history:
                book_id = record.get("book_id")
                if book_id:
                    book = self.books_collection.find_one({"_id": book_id})
                    if book:
                        enriched_record = record.copy()
                        enriched_record["book_details"] = {
                            "title": book.get("title"),
                            "author": book.get("author", {}).get("name"),
                            "genres": book.get("genres", [])
                        }
                        enriched_history.append(enriched_record)
                    else:
                        enriched_history.append(record)
                else:
                    enriched_history.append(record)
            
            return enriched_history
            
        except Exception as e:
            self.logger.error(f"Error getting user borrowing history: {e}")
            return []
    
    def get_currently_borrowed_books(self, user_id):
        """
        Get books currently borrowed by a user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: List of currently borrowed books
        """
        try:
            user = self.find_user_by_id(user_id)
            if not user:
                return []
            
            currently_borrowed = []
            borrowing_history = user.get("borrowing_history", [])
            
            for record in borrowing_history:
                if record.get("returned_date") is None:
                    book_id = record.get("book_id")
                    if book_id:
                        book = self.books_collection.find_one({"_id": book_id})
                        if book:
                            enriched_record = record.copy()
                            enriched_record["book_details"] = {
                                "title": book.get("title"),
                                "author": book.get("author", {}).get("name"),
                                "genres": book.get("genres", [])
                            }
                            currently_borrowed.append(enriched_record)
            
            return currently_borrowed
            
        except Exception as e:
            self.logger.error(f"Error getting currently borrowed books: {e}")
            return []
    
    def borrow_book(self, user_id, book_id, due_days=14):
        """
        Borrow a book for a user.
        
        Args:
            user_id (str): User ID
            book_id: Book ObjectId or string representation
            due_days (int): Number of days until due
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            # Check if user exists
            user = self.find_user_by_id(user_id)
            if not user:
                self.logger.error(f"User {user_id} not found")
                return False
            
            # Check if book exists and is available
            book = self.books_collection.find_one({"_id": book_id})
            if not book:
                self.logger.error(f"Book {book_id} not found")
                return False
            
            if book.get("available_copies", 0) <= 0:
                self.logger.error("No available copies to borrow")
                return False
            
            # Check if user already has this book borrowed
            currently_borrowed = self.get_currently_borrowed_books(user_id)
            for borrowed in currently_borrowed:
                if borrowed.get("book_id") == book_id:
                    self.logger.error("User already has this book borrowed")
                    return False
            
            # Create borrowing record
            borrowed_date = datetime.utcnow()
            due_date = borrowed_date + timedelta(days=due_days)
            
            borrowing_record = {
                "book_id": book_id,
                "borrowed_date": borrowed_date,
                "due_date": due_date,
                "returned_date": None,
                "rating": None
            }
            
            # Update user's borrowing history
            result = self.users_collection.update_one(
                {"user_id": user_id},
                {"$push": {"borrowing_history": borrowing_record}}
            )
            
            if result.modified_count > 0:
                # Decrease book's available copies
                self.books_collection.update_one(
                    {"_id": book_id},
                    {
                        "$inc": {"available_copies": -1},
                        "$set": {"updated_at": datetime.utcnow()}
                    }
                )
                
                self.logger.info(f"User {user_id} borrowed book {book_id}")
                return True
            else:
                self.logger.error("Failed to update user borrowing history")
                return False
                
        except Exception as e:
            self.logger.error(f"Error borrowing book: {e}")
            return False
    
    def return_book(self, user_id, book_id, rating=None):
        """
        Return a book for a user.
        
        Args:
            user_id (str): User ID
            book_id: Book ObjectId or string representation
            rating (int): Optional rating (1-5)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if isinstance(book_id, str):
                book_id = ObjectId(book_id)
            
            # Check if user exists
            user = self.find_user_by_id(user_id)
            if not user:
                self.logger.error(f"User {user_id} not found")
                return False
            
            # Check if book is currently borrowed by user
            currently_borrowed = self.get_currently_borrowed_books(user_id)
            book_found = False
            
            for borrowed in currently_borrowed:
                if borrowed.get("book_id") == book_id:
                    book_found = True
                    break
            
            if not book_found:
                self.logger.error("User does not have this book borrowed")
                return False
            
            # Validate rating if provided
            if rating is not None and not (1 <= rating <= 5):
                self.logger.error("Rating must be between 1 and 5")
                return False
            
            # Update borrowing record
            returned_date = datetime.utcnow()
            
            result = self.users_collection.update_one(
                {
                    "user_id": user_id,
                    "borrowing_history": {
                        "$elemMatch": {
                            "book_id": book_id,
                            "returned_date": None
                        }
                    }
                },
                {
                    "$set": {
                        "borrowing_history.$.returned_date": returned_date,
                        "borrowing_history.$.rating": rating
                    }
                }
            )
            
            if result.modified_count > 0:
                # Increase book's available copies
                self.books_collection.update_one(
                    {"_id": book_id},
                    {
                        "$inc": {"available_copies": 1},
                        "$set": {"updated_at": datetime.utcnow()}
                    }
                )
                
                # Add rating to book if provided
                if rating is not None:
                    from book_manager import BookManager
                    book_manager = BookManager(self.mongo_client)
                    book_manager.add_rating(book_id, rating)
                
                self.logger.info(f"User {user_id} returned book {book_id}")
                return True
            else:
                self.logger.error("Failed to update borrowing record")
                return False
                
        except Exception as e:
            self.logger.error(f"Error returning book: {e}")
            return False
    
    def get_overdue_books(self, user_id=None):
        """
        Get overdue books for a specific user or all users.
        
        Args:
            user_id (str): Optional user ID to filter by
            
        Returns:
            list: List of overdue borrowing records
        """
        try:
            current_date = datetime.utcnow()
            
            pipeline = [
                {"$unwind": "$borrowing_history"},
                {
                    "$match": {
                        "borrowing_history.returned_date": None,
                        "borrowing_history.due_date": {"$lt": current_date}
                    }
                }
            ]
            
            # Add user filter if specified
            if user_id:
                pipeline.insert(0, {"$match": {"user_id": user_id}})
            
            # Add book details lookup
            pipeline.extend([
                {
                    "$lookup": {
                        "from": "books",
                        "localField": "borrowing_history.book_id",
                        "foreignField": "_id",
                        "as": "book_details"
                    }
                },
                {"$unwind": "$book_details"},
                {
                    "$project": {
                        "user_id": 1,
                        "user_name": "$name",
                        "user_email": "$email",
                        "book_id": "$borrowing_history.book_id",
                        "book_title": "$book_details.title",
                        "book_author": "$book_details.author.name",
                        "borrowed_date": "$borrowing_history.borrowed_date",
                        "due_date": "$borrowing_history.due_date",
                        "days_overdue": {
                            "$ceil": {
                                "$divide": [
                                    {"$subtract": [current_date, "$borrowing_history.due_date"]},
                                    86400000  # milliseconds in a day
                                ]
                            }
                        }
                    }
                },
                {"$sort": {"days_overdue": -1}}
            ])
            
            result = list(self.users_collection.aggregate(pipeline))
            self.logger.info(f"Found {len(result)} overdue books")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting overdue books: {e}")
            return []
    
    def update_user_preferences(self, user_id, favorite_genres=None, reading_frequency=None):
        """
        Update user preferences.
        
        Args:
            user_id (str): User ID
            favorite_genres (list): List of favorite genres
            reading_frequency (str): Reading frequency preference
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            update_fields = {}
            
            if favorite_genres is not None:
                update_fields["preferences.favorite_genres"] = favorite_genres
            
            if reading_frequency is not None:
                update_fields["preferences.reading_frequency"] = reading_frequency
            
            if not update_fields:
                self.logger.error("No fields to update")
                return False
            
            result = self.users_collection.update_one(
                {"user_id": user_id},
                {"$set": update_fields}
            )
            
            if result.modified_count > 0:
                self.logger.info(f"Updated preferences for user {user_id}")
                return True
            else:
                self.logger.error("Failed to update user preferences")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating user preferences: {e}")
            return False
    
    def get_user_recommendations(self, user_id, limit=10):
        """
        Get book recommendations for a user based on their preferences and history.
        
        Args:
            user_id (str): User ID
            limit (int): Number of recommendations to return
            
        Returns:
            list: List of recommended books
        """
        try:
            user = self.find_user_by_id(user_id)
            if not user:
                return []
            
            favorite_genres = user.get("preferences", {}).get("favorite_genres", [])
            
            # Get books the user has already borrowed
            borrowed_book_ids = [record.get("book_id") for record in user.get("borrowing_history", []) if record.get("book_id")]
            
            # Find highly-rated books in user's favorite genres that they haven't borrowed
            pipeline = [
                {
                    "$match": {
                        "_id": {"$nin": borrowed_book_ids},
                        "genres": {"$in": favorite_genres},
                        "ratings.average": {"$gte": 4.0},
                        "available_copies": {"$gt": 0}
                    }
                },
                {
                    "$project": {
                        "title": 1,
                        "author": "$author.name",
                        "genres": 1,
                        "average_rating": "$ratings.average",
                        "rating_count": "$ratings.count",
                        "available_copies": 1
                    }
                },
                {"$sort": {"average_rating": -1, "rating_count": -1}},
                {"$limit": limit}
            ]
            
            recommendations = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error getting user recommendations: {e}")
            return []
    
    def get_user_statistics(self, user_id):
        """
        Get statistics for a specific user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User statistics
        """
        try:
            user = self.find_user_by_id(user_id)
            if not user:
                return {}
            
            borrowing_history = user.get("borrowing_history", [])
            
            stats = {
                "user_id": user_id,
                "name": user.get("name"),
                "membership_type": user.get("membership", {}).get("type"),
                "total_borrowings": len(borrowing_history),
                "currently_borrowed": len(self.get_currently_borrowed_books(user_id)),
                "books_returned": len([r for r in borrowing_history if r.get("returned_date")]),
                "average_rating_given": 0,
                "favorite_genres": user.get("preferences", {}).get("favorite_genres", []),
                "reading_frequency": user.get("preferences", {}).get("reading_frequency")
            }
            
            # Calculate average rating given by user
            ratings = [r.get("rating") for r in borrowing_history if r.get("rating")]
            if ratings:
                stats["average_rating_given"] = round(sum(ratings) / len(ratings), 2)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting user statistics: {e}")
            return {}
