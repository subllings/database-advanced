# MongoDB Library Catalog

A comprehensive library catalog system built with MongoDB and Python, demonstrating NoSQL document database capabilities.

## Project Overview

This project implements a library catalog system using MongoDB to store, query, and analyze book data. It demonstrates key NoSQL concepts including document modeling, flexible schemas, nested fields, and powerful aggregation pipelines.

## Features

### Must-Have (Core Requirements)
- [x] Books collection with 100+ documents
- [x] Basic queries (filtering, nested fields, range queries)
- [x] Aggregation pipeline (average, count, group by)
- [x] Document updates

### Nice-to-Have (Advanced Features)
- [x] Multiple collections (books, users, authors)
- [x] Complex cross-collection queries
- [x] Advanced aggregations
- [x] Error handling and logging
- [x] Interactive interface
- [x] Data visualization capabilities

## Project Structure

```
mongodb_library_catalog/
├── src/
│   ├── mongodb_client.py      # MongoDB connection management
│   ├── data_loader.py         # Data loading and seeding
│   ├── book_manager.py        # Book operations and queries
│   ├── user_manager.py        # User management and borrowing
│   ├── analytics.py           # Aggregations and analytics
│   └── interface.py           # Interactive command-line interface
├── data/
│   ├── books.json            # Sample book data
│   ├── users.json            # Sample user data
│   └── borrowing_history.json # Sample borrowing records
├── scripts/
│   ├── setup-env.sh          # Environment setup
│   ├── start-mongodb.sh      # Start MongoDB with Docker
│   ├── stop-mongodb.sh       # Stop MongoDB
│   └── run-catalog.sh        # Run the library catalog application
├── requirements.txt          # Python dependencies
├── main.py                  # Main application entry point
├── docker-compose.yml       # MongoDB Docker configuration
└── README.md               # This file
```

## Quick Start

### 1. Setup Environment
```bash
chmod +x scripts/*.sh
./scripts/setup-env.sh
```

### 2. Start MongoDB
```bash
./scripts/start-mongodb.sh
```

### 3. Run the Application
```bash
./scripts/run-catalog.sh
```

## MongoDB Setup

### Using Docker (Recommended)
```bash
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

### Using Docker Compose
```bash
docker-compose up -d
```

## Data Model

### Books Collection
```json
{
  "_id": ObjectId("..."),
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
  "description": "A fantasy novel about the quest of home-loving Hobbit...",
  "pages": 310,
  "language": "English",
  "available_copies": 5,
  "total_copies": 8,
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### Users Collection
```json
{
  "_id": ObjectId("..."),
  "user_id": "U001",
  "name": "Alice Johnson",
  "email": "alice.johnson@email.com",
  "membership": {
    "type": "premium",
    "start_date": ISODate("2023-01-15T00:00:00Z"),
    "end_date": ISODate("2024-01-15T00:00:00Z")
  },
  "preferences": {
    "favorite_genres": ["Mystery", "Thriller"],
    "reading_frequency": "weekly"
  },
  "borrowing_history": [
    {
      "book_id": ObjectId("..."),
      "borrowed_date": ISODate("2024-01-10T00:00:00Z"),
      "due_date": ISODate("2024-01-24T00:00:00Z"),
      "returned_date": ISODate("2024-01-20T00:00:00Z"),
      "rating": 4
    }
  ],
  "created_at": ISODate("2023-01-15T10:30:00Z")
}
```

## Key Features Demonstrated

### 1. Document Modeling
- Embedded documents (author info within books)
- Arrays for multi-valued fields (genres, ratings)
- Nested objects for complex data (publication details)

### 2. Query Operations
- **Basic Queries**: Find books by genre, author, year
- **Range Queries**: Books published between years
- **Nested Field Queries**: Search within embedded documents
- **Array Queries**: Find books with specific genres

### 3. Aggregation Pipeline
- **Grouping**: Books per genre, authors per nationality
- **Calculations**: Average ratings, total pages per genre
- **Sorting**: Most popular books, most prolific authors
- **Complex Pipelines**: Multi-stage aggregations

### 4. Update Operations
- **Add Ratings**: Update book rating arrays
- **Modify Availability**: Update copy counts
- **User Updates**: Add borrowing history
- **Bulk Updates**: Update multiple documents

## Usage Examples

### Basic Queries
```python
# Find all fantasy books
fantasy_books = book_manager.find_books_by_genre("Fantasy")

# Find books by specific author
tolkien_books = book_manager.find_books_by_author("J.R.R. Tolkien")

# Find highly rated books
top_books = book_manager.find_highly_rated_books(rating_threshold=4.5)
```

### Aggregation Examples
```python
# Average rating per genre
genre_ratings = analytics.average_rating_per_genre()

# Most prolific authors
top_authors = analytics.most_prolific_authors(limit=10)

# Books published per decade
decade_stats = analytics.books_per_decade()
```

### Update Examples
```python
# Add a new rating to a book
book_manager.add_rating("The Hobbit", 5)

# Borrow a book
user_manager.borrow_book("U001", book_id)

# Return a book with rating
user_manager.return_book("U001", book_id, rating=4)
```

## Technologies Used

- **MongoDB 6.0**: NoSQL document database
- **Python 3.12**: Programming language
- **PyMongo**: MongoDB Python driver
- **Pandas**: Data manipulation and analysis
- **Docker**: Containerization for MongoDB
- **JSON**: Data format for sample datasets

## Learning Objectives Achieved

- ✅ **NoSQL Document Structures**: Flexible schemas, nested fields
- ✅ **Data Loading**: From open datasets to MongoDB collections
- ✅ **Query Operations**: Filters, ranges, nested field queries
- ✅ **Aggregation Pipeline**: Counts, averages, grouping
- ✅ **Document Updates**: Dynamic modifications
- ✅ **Cross-Collection Operations**: Joins and references
- ✅ **Performance Considerations**: Indexing strategies

## Sample Queries and Results

The application includes a comprehensive set of sample queries demonstrating:

1. **Simple Filtering**: Books by genre, author, year
2. **Complex Conditions**: Multiple criteria, ranges
3. **Nested Queries**: Searching embedded documents
4. **Array Operations**: Finding books with specific genres
5. **Aggregations**: Statistical analysis and grouping
6. **Updates**: Adding ratings, managing inventory

## Development Notes

This project demonstrates production-ready practices:
- Clean code organization with modular components
- Comprehensive error handling and logging
- Interactive user interface for testing
- Docker-based development environment
- Clear documentation and examples

## Next Steps

Potential enhancements for advanced learning:
- Implement text search with MongoDB Atlas Search
- Add geographic data for library branches
- Implement recommendation system based on borrowing patterns
- Add real-time notifications for due dates
- Integrate with external book APIs (Google Books, OpenLibrary)

---

**Built as part of the BeCode Database Advanced curriculum**
