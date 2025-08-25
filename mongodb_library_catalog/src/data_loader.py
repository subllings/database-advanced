"""
Data Loader Module

This module handles loading sample data into the MongoDB library catalog.
It creates comprehensive book, user, and borrowing history collections.
"""

import json
import logging
from datetime import datetime, timedelta
from bson import ObjectId
import random


class DataLoader:
    """Data loader for MongoDB library catalog."""
    
    def __init__(self, mongo_client):
        """
        Initialize data loader.
        
        Args:
            mongo_client: MongoDBClient instance
        """
        self.mongo_client = mongo_client
        self.db = mongo_client.get_database()
        self.logger = logging.getLogger(__name__)
    
    def needs_initial_setup(self):
        """
        Check if initial data setup is needed.
        
        Returns:
            bool: True if setup needed, False otherwise
        """
        try:
            books_collection = self.db.books
            books_count = books_collection.count_documents({})
            return books_count < 100  # Need at least 100 books as per requirements
        except Exception as e:
            self.logger.error(f"Error checking setup status: {e}")
            return True
    
    def generate_books_data(self):
        """
        Generate comprehensive book data.
        
        Returns:
            list: List of book documents
        """
        books = [
            {
                "title": "The Hobbit",
                "author": {
                    "name": "J.R.R. Tolkien",
                    "birth_year": 1892,
                    "nationality": "British"
                },
                "isbn": "978-0547928227",
                "genres": ["Fantasy", "Adventure"],
                "publication": {
                    "year": 1937,
                    "publisher": "George Allen & Unwin",
                    "edition": "1st"
                },
                "ratings": {
                    "average": 4.27,
                    "count": 3021,
                    "distribution": [156, 289, 445, 1203, 928]
                },
                "description": "A fantasy novel about the quest of home-loving Hobbit Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon.",
                "pages": 310,
                "language": "English",
                "available_copies": 5,
                "total_copies": 8
            },
            {
                "title": "Pride and Prejudice",
                "author": {
                    "name": "Jane Austen",
                    "birth_year": 1775,
                    "nationality": "British"
                },
                "isbn": "978-0141439518",
                "genres": ["Romance", "Classic"],
                "publication": {
                    "year": 1813,
                    "publisher": "T. Egerton",
                    "edition": "1st"
                },
                "ratings": {
                    "average": 4.26,
                    "count": 4521,
                    "distribution": [89, 234, 567, 1234, 2397]
                },
                "description": "A romantic novel of manners following Elizabeth Bennet and her complex relationship with the proud Mr. Darcy.",
                "pages": 432,
                "language": "English",
                "available_copies": 7,
                "total_copies": 10
            },
            {
                "title": "To Kill a Mockingbird",
                "author": {
                    "name": "Harper Lee",
                    "birth_year": 1926,
                    "nationality": "American"
                },
                "isbn": "978-0060935467",
                "genres": ["Classic", "Drama"],
                "publication": {
                    "year": 1960,
                    "publisher": "J.B. Lippincott & Co.",
                    "edition": "1st"
                },
                "ratings": {
                    "average": 4.28,
                    "count": 5234,
                    "distribution": [123, 345, 678, 1567, 2521]
                },
                "description": "A gripping tale of racial injustice and childhood innocence in the American South.",
                "pages": 376,
                "language": "English",
                "available_copies": 6,
                "total_copies": 12
            },
            {
                "title": "1984",
                "author": {
                    "name": "George Orwell",
                    "birth_year": 1903,
                    "nationality": "British"
                },
                "isbn": "978-0451524935",
                "genres": ["Dystopian", "Science Fiction"],
                "publication": {
                    "year": 1949,
                    "publisher": "Secker & Warburg",
                    "edition": "1st"
                },
                "ratings": {
                    "average": 4.19,
                    "count": 6789,
                    "distribution": [234, 456, 789, 2134, 3176]
                },
                "description": "A dystopian social science fiction novel about totalitarian control and surveillance.",
                "pages": 328,
                "language": "English",
                "available_copies": 4,
                "total_copies": 15
            },
            {
                "title": "The Great Gatsby",
                "author": {
                    "name": "F. Scott Fitzgerald",
                    "birth_year": 1896,
                    "nationality": "American"
                },
                "isbn": "978-0743273565",
                "genres": ["Classic", "Drama"],
                "publication": {
                    "year": 1925,
                    "publisher": "Charles Scribner's Sons",
                    "edition": "1st"
                },
                "ratings": {
                    "average": 3.93,
                    "count": 4567,
                    "distribution": [345, 567, 890, 1234, 1531]
                },
                "description": "A classic novel about the Jazz Age and the American Dream in the Roaring Twenties.",
                "pages": 180,
                "language": "English",
                "available_copies": 8,
                "total_copies": 20
            }
        ]
        
        # Generate additional books to reach 100+ requirement
        additional_authors = [
            {"name": "Agatha Christie", "birth_year": 1890, "nationality": "British"},
            {"name": "Stephen King", "birth_year": 1947, "nationality": "American"},
            {"name": "Isaac Asimov", "birth_year": 1920, "nationality": "American"},
            {"name": "Virginia Woolf", "birth_year": 1882, "nationality": "British"},
            {"name": "Gabriel García Márquez", "birth_year": 1927, "nationality": "Colombian"},
            {"name": "Toni Morrison", "birth_year": 1931, "nationality": "American"},
            {"name": "William Shakespeare", "birth_year": 1564, "nationality": "British"},
            {"name": "Leo Tolstoy", "birth_year": 1828, "nationality": "Russian"},
            {"name": "Ernest Hemingway", "birth_year": 1899, "nationality": "American"},
            {"name": "Maya Angelou", "birth_year": 1928, "nationality": "American"}
        ]
        
        genres_list = [
            ["Mystery", "Crime"], ["Horror", "Thriller"], ["Science Fiction", "Technology"],
            ["Literary Fiction", "Drama"], ["Magic Realism", "Literary Fiction"],
            ["Historical Fiction", "Drama"], ["Drama", "Poetry"], ["Historical Fiction", "Classic"],
            ["Adventure", "War"], ["Biography", "Poetry"]
        ]
        
        book_titles = [
            "Murder on the Orient Express", "The Shining", "Foundation",
            "Mrs. Dalloway", "One Hundred Years of Solitude", "Beloved",
            "Hamlet", "War and Peace", "The Old Man and the Sea",
            "I Know Why the Caged Bird Sings"
        ]
        
        # Add 95 more books to reach 100+
        for i in range(95):
            author_index = i % len(additional_authors)
            genre_index = i % len(genres_list)
            
            # Create varied book data
            book = {
                "title": f"{book_titles[i % len(book_titles)]} - Volume {i // 10 + 1}" if i >= 10 else book_titles[i % len(book_titles)],
                "author": additional_authors[author_index],
                "isbn": f"978-{random.randint(1000000000, 9999999999)}",
                "genres": genres_list[genre_index],
                "publication": {
                    "year": random.randint(1800, 2023),
                    "publisher": random.choice(["Penguin Books", "HarperCollins", "Random House", "Macmillan", "Simon & Schuster"]),
                    "edition": random.choice(["1st", "2nd", "3rd", "Revised"])
                },
                "ratings": {
                    "average": round(random.uniform(3.0, 5.0), 2),
                    "count": random.randint(100, 10000),
                    "distribution": [random.randint(10, 500) for _ in range(5)]
                },
                "description": f"An engaging {genres_list[genre_index][0].lower()} novel by {additional_authors[author_index]['name']}.",
                "pages": random.randint(150, 800),
                "language": random.choice(["English", "Spanish", "French", "German", "Russian"]),
                "available_copies": random.randint(1, 10),
                "total_copies": random.randint(5, 25)
            }
            books.append(book)
        
        # Add timestamps
        current_time = datetime.utcnow()
        for book in books:
            book["created_at"] = current_time
            book["updated_at"] = current_time
        
        return books
    
    def generate_users_data(self):
        """
        Generate user data with borrowing history.
        
        Returns:
            list: List of user documents
        """
        users = []
        first_names = ["Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry", "Iris", "Jack"]
        last_names = ["Johnson", "Smith", "Brown", "Davis", "Wilson", "Miller", "Moore", "Taylor", "Anderson", "Thomas"]
        
        for i in range(50):  # Generate 50 users
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            user = {
                "user_id": f"U{str(i+1).zfill(3)}",
                "name": f"{first_name} {last_name}",
                "email": f"{first_name.lower()}.{last_name.lower()}{i}@email.com",
                "membership": {
                    "type": random.choice(["basic", "premium", "student"]),
                    "start_date": datetime.utcnow() - timedelta(days=random.randint(30, 365)),
                    "end_date": datetime.utcnow() + timedelta(days=random.randint(30, 365))
                },
                "preferences": {
                    "favorite_genres": random.sample(["Fantasy", "Mystery", "Romance", "Science Fiction", "Classic", "Horror"], k=random.randint(1, 3)),
                    "reading_frequency": random.choice(["daily", "weekly", "monthly", "occasionally"])
                },
                "borrowing_history": [],
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
            }
            
            users.append(user)
        
        return users
    
    def generate_borrowing_history(self, books_collection, users_collection):
        """
        Generate borrowing history and update user records.
        
        Args:
            books_collection: MongoDB books collection
            users_collection: MongoDB users collection
        """
        try:
            # Get all book and user IDs
            books = list(books_collection.find({}, {"_id": 1}))
            users = list(users_collection.find({}, {"_id": 1, "user_id": 1}))
            
            # Generate borrowing records
            for user in users:
                num_borrowings = random.randint(1, 8)
                borrowing_history = []
                
                for _ in range(num_borrowings):
                    book = random.choice(books)
                    borrowed_date = datetime.utcnow() - timedelta(days=random.randint(1, 365))
                    due_date = borrowed_date + timedelta(days=14)
                    
                    # Some books are returned, some are still borrowed
                    if random.random() < 0.8:  # 80% are returned
                        returned_date = borrowed_date + timedelta(days=random.randint(1, 20))
                        rating = random.randint(1, 5)
                    else:
                        returned_date = None
                        rating = None
                    
                    borrowing_record = {
                        "book_id": book["_id"],
                        "borrowed_date": borrowed_date,
                        "due_date": due_date,
                        "returned_date": returned_date,
                        "rating": rating
                    }
                    
                    borrowing_history.append(borrowing_record)
                
                # Update user with borrowing history
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"borrowing_history": borrowing_history}}
                )
            
            self.logger.info("Borrowing history generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating borrowing history: {e}")
    
    def load_books(self):
        """
        Load book data into MongoDB.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            books_collection = self.db.books
            
            # Drop existing collection if it exists
            books_collection.drop()
            
            # Generate and insert book data
            books_data = self.generate_books_data()
            result = books_collection.insert_many(books_data)
            
            self.logger.info(f"Inserted {len(result.inserted_ids)} books")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading books: {e}")
            return False
    
    def load_users(self):
        """
        Load user data into MongoDB.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            users_collection = self.db.users
            
            # Drop existing collection if it exists
            users_collection.drop()
            
            # Generate and insert user data
            users_data = self.generate_users_data()
            result = users_collection.insert_many(users_data)
            
            self.logger.info(f"Inserted {len(result.inserted_ids)} users")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading users: {e}")
            return False
    
    def load_all_data(self):
        """
        Load all sample data into MongoDB.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load books
            if not self.load_books():
                return False
            
            # Load users
            if not self.load_users():
                return False
            
            # Generate borrowing history
            books_collection = self.db.books
            users_collection = self.db.users
            self.generate_borrowing_history(books_collection, users_collection)
            
            # Create indexes for performance
            self.mongo_client.create_indexes()
            
            self.logger.info("All sample data loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return False
