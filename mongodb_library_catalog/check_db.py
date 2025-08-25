#!/usr/bin/env python3
"""
Test script to check if books are in the MongoDB database
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from mongodb_client import MongoDBClient
from book_manager import BookManager
from data_loader import DataLoader

def check_database():
    """Check the MongoDB database status and book data."""
    
    print("=" * 60)
    print("     MONGODB LIBRARY CATALOG - DATABASE CHECK")
    print("=" * 60)
    
    # Initialize MongoDB client
    client = MongoDBClient()
    
    if not client.connect():
        print("ERROR: Failed to connect to MongoDB")
        print("Please ensure MongoDB is running using: ./scripts/start-mongodb.sh")
        return False
    
    print("SUCCESS: Connected to MongoDB")
    
    # Check collections
    collections = client.list_collections()
    print(f"\nCollections available: {collections}")
    
    if not collections:
        print("WARNING: No collections found. Database is empty.")
        return setup_database(client)
    
    # Check books collection
    books_collection = client.get_collection("books")
    book_count = books_collection.count_documents({})
    
    if book_count == 0:
        print("WARNING: Books collection exists but is empty.")
        return setup_database(client)
    
    print(f"\nFound {book_count} books in the database")
    
    # Get book statistics
    book_manager = BookManager(client)
    stats = book_manager.get_book_statistics()
    
    print("\nBook Statistics:")
    print("-" * 40)
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Show sample books
    print("\nSample Books:")
    print("-" * 80)
    books = book_manager.find_all_books(limit=5)
    
    for i, book in enumerate(books, 1):
        title = book.get("title", "N/A")
        author = book.get("author", {}).get("name", "N/A")
        genres = book.get("genres", [])
        genre_str = ", ".join(genres[:2]) if genres else "N/A"
        rating = book.get("ratings", {}).get("average", 0)
        available = book.get("available_copies", 0)
        total = book.get("total_copies", 0)
        
        print(f"{i:2}. {title:<30} by {author:<20}")
        print(f"    Genre: {genre_str:<20} Rating: {rating:.2f} Copies: {available}/{total}")
        print()
    
    # Check users collection
    users_collection = client.get_collection("users")
    user_count = users_collection.count_documents({})
    print(f"Found {user_count} users in the database")
    
    client.close()
    return True

def setup_database(client):
    """Setup the database with sample data."""
    print("\nSetting up database with sample data...")
    
    data_loader = DataLoader(client)
    
    if data_loader.load_all_data():
        print("SUCCESS: Sample data loaded successfully")
        
        # Verify the setup
        books_collection = client.get_collection("books")
        book_count = books_collection.count_documents({})
        print(f"{book_count} books have been loaded into the database")
        
        return True
    else:
        print("ERROR: Failed to load sample data")
        return False

if __name__ == "__main__":
    try:
        success = check_database()
        if success:
            print("\nSUCCESS: Database check completed successfully")
        else:
            print("\nERROR: Database check failed")
    except Exception as e:
        print(f"\nERROR: Error during database check: {e}")
