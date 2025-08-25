# 🎬 Movie Search Engine with Elasticsearch

## Overview
This project implements a movie search engine using Elasticsearch. It demonstrates full-text search, filtering, aggregations, and analytics capabilities.

## Features

### Must-have Features ✅
- Index movies with title, description, genre, release year, rating
- Search by title or keywords in description
- Filter by genre or year
- Sort by rating or popularity

### Nice-to-have Features 🌟
- "Similar movies" with `more_like_this`
- Autocomplete on movie titles
- Aggregations and statistics

## Prerequisites

1. **Elasticsearch** running locally (port 9200)
   - Download from: https://www.elastic.co/downloads/elasticsearch
   - Start with: `bin/elasticsearch` (Linux/Mac) or `bin\elasticsearch.bat` (Windows)

2. **Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

1. **Start Elasticsearch**
   ```bash
   # Make sure Elasticsearch is running on localhost:9200
   curl http://localhost:9200
   ```

2. **Setup the project**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Download and index sample movie data
   python src/data_indexer.py
   ```

3. **Run the search engine**
   ```bash
   python src/movie_search_engine.py
   ```

## Project Structure

```
elasticsearch_movie_search/
├── src/
│   ├── elasticsearch_client.py  # ES connection and config
│   ├── data_indexer.py         # Download and index movie data
│   ├── movie_search_engine.py  # Main search functionality
│   └── search_interface.py     # Interactive search interface
├── data/
│   └── movies.json            # Sample movie dataset
├── requirements.txt
└── README.md
```

## Usage Examples

### Basic Search
```python
from src.movie_search_engine import MovieSearchEngine

engine = MovieSearchEngine()

# Search by title
results = engine.search_movies("Batman")

# Search with filters
results = engine.search_movies(
    query="action", 
    genre="Action", 
    min_year=2000,
    sort_by="rating"
)
```

### Aggregations
```python
# Get statistics
stats = engine.get_movie_statistics()
print(f"Average rating: {stats['avg_rating']}")
print(f"Movies by genre: {stats['genres']}")
```

## Dataset

This project uses a curated dataset of popular movies with the following fields:
- **title**: Movie title
- **description**: Plot summary
- **genres**: List of genres
- **release_year**: Year of release
- **rating**: IMDb rating (1-10)
- **director**: Director name
- **actors**: Main actors

## API Endpoints Simulated

The search engine simulates these common movie search API patterns:

1. **Search**: `/search?q={query}&genre={genre}&year={year}`
2. **Filter**: `/movies?genre={genre}&min_rating={rating}`
3. **Similar**: `/movies/{id}/similar`
4. **Stats**: `/movies/stats`

## Clean Code Practices

- ✅ Meaningful variable names
- ✅ Comprehensive docstrings
- ✅ Reusable functions
- ✅ Configuration management
- ✅ Error handling
- ✅ Type hints
