"""
Interactive Interface Module

This module provides an interactive command-line interface for the MongoDB Library Catalog.
It allows users to explore all the features through a user-friendly menu system.
"""

import logging
from datetime import datetime
from bson import ObjectId

from book_manager import BookManager
from user_manager import UserManager
from analytics import Analytics


class LibraryInterface:
    """Interactive interface for the library catalog system."""
    
    def __init__(self, mongo_client):
        """
        Initialize the interface.
        
        Args:
            mongo_client: MongoDBClient instance
        """
        self.mongo_client = mongo_client
        self.book_manager = BookManager(mongo_client)
        self.user_manager = UserManager(mongo_client)
        self.analytics = Analytics(mongo_client)
        self.logger = logging.getLogger(__name__)
    
    def display_main_menu(self):
        """Display the main menu options."""
        print("\n" + "=" * 60)
        print("           MONGODB LIBRARY CATALOG - MAIN MENU")
        print("=" * 60)
        print("1.  Browse and Search Books")
        print("2.  Book Management Operations")
        print("3.  User Management")
        print("4.  Analytics and Reports")
        print("5.  Database Information")
        print("6.  Demo - Quick Tour")
        print("0.  Exit")
        print("=" * 60)
    
    def display_books_menu(self):
        """Display the books submenu."""
        print("\n" + "-" * 50)
        print("              BOOKS MENU")
        print("-" * 50)
        print("1.  View All Books")
        print("2.  Search by Title")
        print("3.  Search by Author")
        print("4.  Search by Genre")
        print("5.  Search by Year Range")
        print("6.  Find Highly Rated Books")
        print("7.  Find Available Books")
        print("8.  Advanced Search")
        print("0.  Back to Main Menu")
        print("-" * 50)
    
    def display_management_menu(self):
        """Display the management submenu."""
        print("\n" + "-" * 50)
        print("           MANAGEMENT MENU")
        print("-" * 50)
        print("1.  Add Rating to Book")
        print("2.  Update Book Availability")
        print("3.  Borrow Book")
        print("4.  Return Book")
        print("5.  View Book Statistics")
        print("0.  Back to Main Menu")
        print("-" * 50)
    
    def display_users_menu(self):
        """Display the users submenu."""
        print("\n" + "-" * 50)
        print("              USERS MENU")
        print("-" * 50)
        print("1.  View All Users")
        print("2.  Find User by ID")
        print("3.  Find Users by Membership")
        print("4.  View User Borrowing History")
        print("5.  View Currently Borrowed Books")
        print("6.  View Overdue Books")
        print("7.  Get User Recommendations")
        print("8.  User Statistics")
        print("0.  Back to Main Menu")
        print("-" * 50)
    
    def display_analytics_menu(self):
        """Display the analytics submenu."""
        print("\n" + "-" * 50)
        print("           ANALYTICS MENU")
        print("-" * 50)
        print("1.  Books per Genre")
        print("2.  Average Rating per Genre")
        print("3.  Books per Decade")
        print("4.  Most Prolific Authors")
        print("5.  Authors by Nationality")
        print("6.  Top Rated Books")
        print("7.  Language Distribution")
        print("8.  Publisher Statistics")
        print("9.  User Analytics")
        print("10. Borrowing Analytics")
        print("11. Comprehensive Report")
        print("0.  Back to Main Menu")
        print("-" * 50)
    
    def display_books(self, books, title="Books", limit=10):
        """
        Display a list of books in a formatted table.
        
        Args:
            books (list): List of book documents
            title (str): Title for the display
            limit (int): Maximum number of books to display
        """
        if not books:
            print(f"\nNo {title.lower()} found.")
            return
        
        print(f"\n{title} ({len(books)} found)")
        print("-" * 100)
        print(f"{'Title':<30} {'Author':<20} {'Genre':<15} {'Year':<6} {'Rating':<8} {'Copies':<8}")
        print("-" * 100)
        
        for i, book in enumerate(books[:limit]):
            title_str = book.get("title", "N/A")[:28]
            author_str = book.get("author", {}).get("name", "N/A")[:18]
            genres = book.get("genres", [])
            genre_str = genres[0] if genres else "N/A"
            year = book.get("publication", {}).get("year", "N/A")
            rating = book.get("ratings", {}).get("average", 0)
            available = book.get("available_copies", 0)
            total = book.get("total_copies", 0)
            
            print(f"{title_str:<30} {author_str:<20} {genre_str:<15} {year:<6} {rating:<8.2f} {available}/{total:<6}")
        
        if len(books) > limit:
            print(f"\n... and {len(books) - limit} more books.")
    
    def display_users(self, users, title="Users", limit=10):
        """
        Display a list of users in a formatted table.
        
        Args:
            users (list): List of user documents
            title (str): Title for the display
            limit (int): Maximum number of users to display
        """
        if not users:
            print(f"\nNo {title.lower()} found.")
            return
        
        print(f"\n{title} ({len(users)} found)")
        print("-" * 80)
        print(f"{'User ID':<8} {'Name':<20} {'Email':<25} {'Membership':<12} {'Books':<8}")
        print("-" * 80)
        
        for i, user in enumerate(users[:limit]):
            user_id = user.get("user_id", "N/A")
            name = user.get("name", "N/A")[:18]
            email = user.get("email", "N/A")[:23]
            membership = user.get("membership", {}).get("type", "N/A")
            book_count = len(user.get("borrowing_history", []))
            
            print(f"{user_id:<8} {name:<20} {email:<25} {membership:<12} {book_count:<8}")
        
        if len(users) > limit:
            print(f"\n... and {len(users) - limit} more users.")
    
    def get_user_input(self, prompt, input_type=str, required=True):
        """
        Get user input with validation.
        
        Args:
            prompt (str): Input prompt
            input_type: Expected input type (str, int, float)
            required (bool): Whether input is required
            
        Returns:
            User input of specified type or None
        """
        while True:
            try:
                user_input = input(f"{prompt}: ").strip()
                
                if not user_input and not required:
                    return None
                
                if not user_input and required:
                    print("This field is required. Please enter a value.")
                    continue
                
                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input
                    
            except ValueError:
                print(f"Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None
    
    def handle_books_menu(self):
        """Handle the books menu operations."""
        while True:
            self.display_books_menu()
            choice = self.get_user_input("Enter your choice", int, required=False)
            
            if choice == 0 or choice is None:
                break
            elif choice == 1:
                books = self.book_manager.find_all_books(limit=20)
                self.display_books(books, "All Books", 20)
            elif choice == 2:
                title = self.get_user_input("Enter book title to search")
                if title:
                    books = self.book_manager.find_books_by_title(title)
                    self.display_books(books, f"Books matching '{title}'")
            elif choice == 3:
                author = self.get_user_input("Enter author name to search")
                if author:
                    books = self.book_manager.find_books_by_author(author)
                    self.display_books(books, f"Books by '{author}'")
            elif choice == 4:
                genre = self.get_user_input("Enter genre to search")
                if genre:
                    books = self.book_manager.find_books_by_genre(genre)
                    self.display_books(books, f"Books in genre '{genre}'")
            elif choice == 5:
                start_year = self.get_user_input("Enter start year", int)
                end_year = self.get_user_input("Enter end year", int)
                if start_year and end_year:
                    books = self.book_manager.find_books_by_year_range(start_year, end_year)
                    self.display_books(books, f"Books from {start_year} to {end_year}")
            elif choice == 6:
                threshold = self.get_user_input("Enter minimum rating (default: 4.0)", float, required=False)
                threshold = threshold if threshold is not None else 4.0
                books = self.book_manager.find_highly_rated_books(threshold)
                self.display_books(books, f"Books rated {threshold}+")
            elif choice == 7:
                books = self.book_manager.find_available_books()
                self.display_books(books, "Available Books")
            elif choice == 8:
                self.handle_advanced_search()
            else:
                print("Invalid choice. Please try again.")
    
    def handle_advanced_search(self):
        """Handle advanced book search."""
        print("\nAdvanced Search - Enter filters (leave empty to skip):")
        
        filters = {}
        
        title = self.get_user_input("Title contains", required=False)
        if title:
            filters["title"] = title
        
        author = self.get_user_input("Author contains", required=False)
        if author:
            filters["author"] = author
        
        genre = self.get_user_input("Genre contains", required=False)
        if genre:
            filters["genre"] = genre
        
        min_year = self.get_user_input("Minimum year", int, required=False)
        if min_year:
            filters["min_year"] = min_year
        
        max_year = self.get_user_input("Maximum year", int, required=False)
        if max_year:
            filters["max_year"] = max_year
        
        min_rating = self.get_user_input("Minimum rating", float, required=False)
        if min_rating:
            filters["min_rating"] = min_rating
        
        available_only = self.get_user_input("Available only? (y/n)", required=False)
        if available_only and available_only.lower() == 'y':
            filters["available_only"] = True
        
        if filters:
            books = self.book_manager.search_books_advanced(filters)
            self.display_books(books, "Advanced Search Results")
        else:
            print("No filters specified.")
    
    def handle_management_menu(self):
        """Handle the management menu operations."""
        while True:
            self.display_management_menu()
            choice = self.get_user_input("Enter your choice", int, required=False)
            
            if choice == 0 or choice is None:
                break
            elif choice == 1:
                self.handle_add_rating()
            elif choice == 2:
                self.handle_update_availability()
            elif choice == 3:
                self.handle_borrow_book()
            elif choice == 4:
                self.handle_return_book()
            elif choice == 5:
                stats = self.book_manager.get_book_statistics()
                print("\nBook Collection Statistics:")
                print("-" * 40)
                for key, value in stats.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
            else:
                print("Invalid choice. Please try again.")
    
    def handle_add_rating(self):
        """Handle adding a rating to a book."""
        # First, let user search for a book
        title = self.get_user_input("Enter book title to rate")
        if not title:
            return
        
        books = self.book_manager.find_books_by_title(title)
        if not books:
            print("No books found with that title.")
            return
        
        if len(books) == 1:
            book = books[0]
        else:
            print("\nMultiple books found:")
            for i, book in enumerate(books):
                print(f"{i+1}. {book.get('title')} by {book.get('author', {}).get('name')}")
            
            choice = self.get_user_input("Select book number", int)
            if 1 <= choice <= len(books):
                book = books[choice-1]
            else:
                print("Invalid selection.")
                return
        
        rating = self.get_user_input("Enter rating (1-5)", int)
        if 1 <= rating <= 5:
            if self.book_manager.add_rating(book["_id"], rating):
                print(f"Rating {rating} added successfully!")
            else:
                print("Failed to add rating.")
        else:
            print("Rating must be between 1 and 5.")
    
    def handle_update_availability(self):
        """Handle updating book availability."""
        title = self.get_user_input("Enter book title to update")
        if not title:
            return
        
        books = self.book_manager.find_books_by_title(title, exact_match=True)
        if not books:
            print("Book not found.")
            return
        
        book = books[0]
        current_available = book.get("available_copies", 0)
        current_total = book.get("total_copies", 0)
        
        print(f"\nCurrent availability: {current_available}/{current_total}")
        
        new_available = self.get_user_input("New available copies", int, required=False)
        new_total = self.get_user_input("New total copies", int, required=False)
        
        if new_available is not None or new_total is not None:
            if self.book_manager.update_availability(book["_id"], new_available, new_total):
                print("Availability updated successfully!")
            else:
                print("Failed to update availability.")
    
    def handle_borrow_book(self):
        """Handle borrowing a book."""
        user_id = self.get_user_input("Enter user ID")
        if not user_id:
            return
        
        user = self.user_manager.find_user_by_id(user_id)
        if not user:
            print("User not found.")
            return
        
        title = self.get_user_input("Enter book title to borrow")
        if not title:
            return
        
        books = self.book_manager.find_books_by_title(title)
        if not books:
            print("Book not found.")
            return
        
        if len(books) == 1:
            book = books[0]
        else:
            print("\nMultiple books found:")
            for i, book in enumerate(books):
                print(f"{i+1}. {book.get('title')} by {book.get('author', {}).get('name')}")
            
            choice = self.get_user_input("Select book number", int)
            if 1 <= choice <= len(books):
                book = books[choice-1]
            else:
                print("Invalid selection.")
                return
        
        if self.user_manager.borrow_book(user_id, book["_id"]):
            print(f"Book '{book.get('title')}' borrowed successfully!")
        else:
            print("Failed to borrow book.")
    
    def handle_return_book(self):
        """Handle returning a book."""
        user_id = self.get_user_input("Enter user ID")
        if not user_id:
            return
        
        currently_borrowed = self.user_manager.get_currently_borrowed_books(user_id)
        if not currently_borrowed:
            print("User has no books currently borrowed.")
            return
        
        print("\nCurrently borrowed books:")
        for i, record in enumerate(currently_borrowed):
            book_details = record.get("book_details", {})
            print(f"{i+1}. {book_details.get('title')} by {book_details.get('author')}")
        
        choice = self.get_user_input("Select book number to return", int)
        if 1 <= choice <= len(currently_borrowed):
            record = currently_borrowed[choice-1]
            book_id = record.get("book_id")
            
            rating = self.get_user_input("Rate this book (1-5, optional)", int, required=False)
            
            if self.user_manager.return_book(user_id, book_id, rating):
                print("Book returned successfully!")
            else:
                print("Failed to return book.")
        else:
            print("Invalid selection.")
    
    def handle_users_menu(self):
        """Handle the users menu operations."""
        while True:
            self.display_users_menu()
            choice = self.get_user_input("Enter your choice", int, required=False)
            
            if choice == 0 or choice is None:
                break
            elif choice == 1:
                users = self.user_manager.find_all_users(limit=20)
                self.display_users(users, "All Users", 20)
            elif choice == 2:
                user_id = self.get_user_input("Enter user ID")
                if user_id:
                    user = self.user_manager.find_user_by_id(user_id)
                    if user:
                        print("\nUser Details:")
                        print(f"ID: {user.get('user_id')}")
                        print(f"Name: {user.get('name')}")
                        print(f"Email: {user.get('email')}")
                        print(f"Membership: {user.get('membership', {}).get('type')}")
                        print(f"Borrowing History: {len(user.get('borrowing_history', []))} records")
                    else:
                        print("User not found.")
            elif choice == 3:
                membership = self.get_user_input("Enter membership type (basic/premium/student)")
                if membership:
                    users = self.user_manager.find_users_by_membership(membership)
                    self.display_users(users, f"Users with {membership} membership")
            elif choice == 4:
                user_id = self.get_user_input("Enter user ID")
                if user_id:
                    history = self.user_manager.get_user_borrowing_history(user_id)
                    if history:
                        print(f"\nBorrowing History for {user_id}:")
                        print("-" * 80)
                        for record in history[:10]:
                            book_details = record.get("book_details", {})
                            borrowed = record.get("borrowed_date", "").strftime("%Y-%m-%d") if record.get("borrowed_date") else "N/A"
                            returned = record.get("returned_date", "")
                            returned_str = returned.strftime("%Y-%m-%d") if returned else "Not returned"
                            rating = record.get("rating", "No rating")
                            print(f"{book_details.get('title', 'N/A'):<30} {borrowed:<12} {returned_str:<15} {rating}")
                    else:
                        print("No borrowing history found.")
            elif choice == 5:
                user_id = self.get_user_input("Enter user ID")
                if user_id:
                    borrowed = self.user_manager.get_currently_borrowed_books(user_id)
                    if borrowed:
                        print(f"\nCurrently Borrowed Books for {user_id}:")
                        print("-" * 60)
                        for record in borrowed:
                            book_details = record.get("book_details", {})
                            due_date = record.get("due_date", "").strftime("%Y-%m-%d") if record.get("due_date") else "N/A"
                            print(f"{book_details.get('title', 'N/A'):<30} Due: {due_date}")
                    else:
                        print("No books currently borrowed.")
            elif choice == 6:
                overdue = self.user_manager.get_overdue_books()
                if overdue:
                    print("\nOverdue Books:")
                    print("-" * 80)
                    print(f"{'User':<10} {'Book':<30} {'Due Date':<12} {'Days Overdue':<12}")
                    print("-" * 80)
                    for record in overdue[:10]:
                        user_id = record.get("user_id", "N/A")
                        title = record.get("book_title", "N/A")[:28]
                        due_date = record.get("due_date", "").strftime("%Y-%m-%d") if record.get("due_date") else "N/A"
                        days_overdue = record.get("days_overdue", 0)
                        print(f"{user_id:<10} {title:<30} {due_date:<12} {days_overdue:<12}")
                else:
                    print("No overdue books found.")
            elif choice == 7:
                user_id = self.get_user_input("Enter user ID")
                if user_id:
                    recommendations = self.user_manager.get_user_recommendations(user_id)
                    if recommendations:
                        print(f"\nRecommendations for {user_id}:")
                        print("-" * 60)
                        for rec in recommendations:
                            print(f"{rec.get('title')} by {rec.get('author')} (Rating: {rec.get('average_rating')})")
                    else:
                        print("No recommendations available.")
            elif choice == 8:
                user_id = self.get_user_input("Enter user ID")
                if user_id:
                    stats = self.user_manager.get_user_statistics(user_id)
                    if stats:
                        print(f"\nStatistics for {user_id}:")
                        print("-" * 40)
                        for key, value in stats.items():
                            if key != "user_id":
                                print(f"{key.replace('_', ' ').title()}: {value}")
                    else:
                        print("User not found or no statistics available.")
            else:
                print("Invalid choice. Please try again.")
    
    def handle_analytics_menu(self):
        """Handle the analytics menu operations."""
        while True:
            self.display_analytics_menu()
            choice = self.get_user_input("Enter your choice", int, required=False)
            
            if choice == 0 or choice is None:
                break
            elif choice == 1:
                results = self.analytics.get_books_per_genre()
                print("\nBooks per Genre:")
                print("-" * 30)
                for item in results[:10]:
                    print(f"{item['_id']}: {item['count']} books")
            elif choice == 2:
                results = self.analytics.get_average_rating_per_genre()
                print("\nAverage Rating per Genre:")
                print("-" * 50)
                for item in results[:10]:
                    print(f"{item['genre']}: {item['average_rating']} ({item['book_count']} books)")
            elif choice == 3:
                results = self.analytics.get_books_per_decade()
                print("\nBooks per Decade:")
                print("-" * 40)
                for item in results:
                    print(f"{item['decade']}s: {item['count']} books (avg rating: {item['average_rating']})")
            elif choice == 4:
                results = self.analytics.get_most_prolific_authors()
                print("\nMost Prolific Authors:")
                print("-" * 60)
                for item in results:
                    print(f"{item['author']}: {item['book_count']} books (avg rating: {item['average_rating']})")
            elif choice == 5:
                results = self.analytics.get_authors_by_nationality()
                print("\nAuthors by Nationality:")
                print("-" * 50)
                for item in results:
                    print(f"{item['nationality']}: {item['author_count']} authors, {item['book_count']} books")
            elif choice == 6:
                results = self.analytics.get_top_rated_books()
                print("\nTop Rated Books:")
                print("-" * 70)
                for item in results:
                    print(f"{item['title']} by {item['author']}: {item['average_rating']} ({item['rating_count']} ratings)")
            elif choice == 7:
                results = self.analytics.get_language_distribution()
                print("\nBooks by Language:")
                print("-" * 40)
                for item in results:
                    print(f"{item['language']}: {item['count']} books (avg rating: {item['average_rating']})")
            elif choice == 8:
                results = self.analytics.get_publisher_statistics()
                print("\nPublisher Statistics:")
                print("-" * 60)
                for item in results:
                    print(f"{item['publisher']}: {item['book_count']} books (avg rating: {item['average_rating']})")
            elif choice == 9:
                results = self.analytics.get_user_statistics()
                print("\nUser Analytics:")
                print("-" * 40)
                print(f"Total Users: {results.get('total_users', 0)}")
                print("\nMembership Distribution:")
                for item in results.get('membership_distribution', []):
                    print(f"  {item['_id']}: {item['count']} users")
                print("\nReading Frequency:")
                for item in results.get('reading_frequency_distribution', []):
                    print(f"  {item['_id']}: {item['count']} users")
            elif choice == 10:
                results = self.analytics.get_borrowing_analytics()
                print("\nBorrowing Analytics:")
                print("-" * 40)
                print(f"Total Borrowings: {results.get('total_borrowings', 0)}")
                print(f"Returned Books: {results.get('returned_books', 0)}")
                print(f"Current Borrowings: {results.get('current_borrowings', 0)}")
                print(f"Average User Rating: {results.get('average_rating', 0)}")
                
                most_borrowed = results.get('most_borrowed_books', [])
                if most_borrowed:
                    print("\nMost Borrowed Books:")
                    for book in most_borrowed[:5]:
                        print(f"  {book['title']}: {book['borrow_count']} times")
            elif choice == 11:
                print("\nGenerating comprehensive report...")
                report = self.analytics.get_comprehensive_report()
                print("Comprehensive report generated successfully!")
                print("(Report contains detailed analytics - would be saved to file in production)")
            else:
                print("Invalid choice. Please try again.")
    
    def show_database_info(self):
        """Show database connection and collection information."""
        status = self.mongo_client.get_connection_status()
        
        print("\nDatabase Connection Information:")
        print("-" * 50)
        
        if status["connected"]:
            print(f"Status: Connected")
            print(f"Host: {status['host']}:{status['port']}")
            print(f"Database: {status['database']}")
            print(f"Collections: {status['total_collections']}")
            print(f"Data Size: {status['data_size']} bytes")
            print(f"Storage Size: {status['storage_size']} bytes")
            
            print("\nCollections:")
            for collection in status['collections']:
                count = self.mongo_client.get_collection(collection).count_documents({})
                print(f"  {collection}: {count} documents")
        else:
            print(f"Status: Disconnected")
            print(f"Message: {status['message']}")
    
    def demo_quick_tour(self):
        """Provide a quick demonstration of key features."""
        print("\n" + "=" * 60)
        print("           MONGODB LIBRARY CATALOG - QUICK TOUR")
        print("=" * 60)
        
        # 1. Show some books
        print("\n1. Sample Books in the Catalog:")
        books = self.book_manager.find_all_books(limit=5)
        self.display_books(books, "Sample Books", 5)
        
        # 2. Show genre statistics
        print("\n2. Books by Genre (Top 5):")
        genres = self.analytics.get_books_per_genre()
        for i, genre in enumerate(genres[:5]):
            print(f"   {genre['_id']}: {genre['count']} books")
        
        # 3. Show top authors
        print("\n3. Most Prolific Authors (Top 5):")
        authors = self.analytics.get_most_prolific_authors(5)
        for author in authors:
            print(f"   {author['author']}: {author['book_count']} books")
        
        # 4. Show some users
        print("\n4. Sample Users:")
        users = self.user_manager.find_all_users(limit=3)
        self.display_users(users, "Sample Users", 3)
        
        # 5. Show basic statistics
        book_stats = self.book_manager.get_book_statistics()
        print("\n5. Collection Statistics:")
        print(f"   Total Books: {book_stats.get('total_books', 0)}")
        print(f"   Available Books: {book_stats.get('available_books', 0)}")
        print(f"   Average Rating: {book_stats.get('average_rating', 0)}")
        
        print("\n" + "=" * 60)
        print("This demo showcases the key features of the MongoDB Library Catalog:")
        print("- Document-based data storage with flexible schemas")
        print("- Complex queries with nested fields and arrays")
        print("- Powerful aggregation pipelines for analytics")
        print("- Real-world library operations (borrow/return)")
        print("- User management and personalized recommendations")
        print("=" * 60)
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the interactive interface."""
        print("\nWelcome to the MongoDB Library Catalog Interactive Interface!")
        print("This system demonstrates NoSQL database capabilities with a real-world library scenario.")
        
        while True:
            try:
                self.display_main_menu()
                choice = self.get_user_input("Enter your choice", int, required=False)
                
                if choice == 0 or choice is None:
                    print("\nThank you for using MongoDB Library Catalog!")
                    break
                elif choice == 1:
                    self.handle_books_menu()
                elif choice == 2:
                    self.handle_management_menu()
                elif choice == 3:
                    self.handle_users_menu()
                elif choice == 4:
                    self.handle_analytics_menu()
                elif choice == 5:
                    self.show_database_info()
                elif choice == 6:
                    self.demo_quick_tour()
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting MongoDB Library Catalog...")
                break
            except Exception as e:
                self.logger.error(f"Error in interface: {e}")
                print(f"An error occurred: {e}")
                print("Please try again or contact support.")
