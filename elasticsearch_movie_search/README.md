# Movie Search Engine with Elasticsearch

## Overview
This project implements a movie search engine using Elasticsearch. It demonstrates full-text search, filtering, aggregations, and analytics capabilities.

## Features

### Must-have Features
- Index movies with title, description, genre, release year, rating
- Search by title or keywords in description
- Filter by genre or year
- Sort by rating or popularity

### Nice-to-have Features
- "Similar movies" with `more_like_this`
- Autocomplete on movie titles
- Aggregations and statistics

## Prerequisites

1. **Docker** - for running Elasticsearch
   - Download from: https://www.docker.com/get-started
   - Make sure Docker is running

2. **Python 3.8+** - for the application
   - Download from: https://www.python.org/downloads/

3. **Git Bash** (Windows) or Terminal (Linux/Mac)

## Quick Start

### Step 1: Setup Environment
```bash
# Navigate to the project directory
cd /path/to/elasticsearch_movie_search

# Setup Python environment and dependencies
./setup-env.sh
```

### Step 2: Start Elasticsearch
```bash
# Start Elasticsearch and Kibana using Docker
./start-elasticsearch.sh
```

### Step 3: Run the Application
```bash
# Run the movie search engine
./run-movie-search.sh
```

## Manual Setup (Alternative)

If you prefer manual setup:

1. **Start Elasticsearch**
   ```bash
   docker-compose up -d
   ```

2. **Setup Python Environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Git Bash on Windows
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## Available Scripts

- `setup-env.sh` - Sets up Python virtual environment and installs dependencies
- `start-elasticsearch.sh` - Starts Elasticsearch and Kibana containers
- `stop-elasticsearch.sh` - Stops all containers
- `run-movie-search.sh` - Runs the complete application

## Testing

### Quick Connection Test
```bash
python test_basic.py --connection-only
```

### Full Functionality Test
```bash
python test_basic.py
```

### Advanced Features Demo
```bash
python demo_advanced.py
```

## Project Structure

```
elasticsearch_movie_search/
├── main.py                    # Main entry point
├── demo_advanced.py           # Advanced features demo
├── test_basic.py             # Basic functionality tests
├── requirements.txt          # Python dependencies
├── .env                      # Configuration
├── docker-compose.yml        # Docker configuration
├── README.md                 # This documentation
├── setup-env.sh             # Environment setup script
├── start-elasticsearch.sh    # Start Elasticsearch script
├── stop-elasticsearch.sh     # Stop Elasticsearch script
├── run-movie-search.sh      # Run application script
├── src/
│   ├── elasticsearch_client.py   # ES connection management
│   ├── data_indexer.py          # Data indexing
│   ├── movie_search_engine.py   # Core search logic
│   └── search_interface.py      # Interactive UI
└── data/
    └── movies.json              # Sample dataset (created automatically)
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

This project uses a curated dataset of 15 popular movies with:
- **title**: Movie title
- **description**: Plot summary
- **genres**: List of genres
- **release_year**: Year of release
- **rating**: IMDb rating (1-10)
- **director**: Director name
- **actors**: Main actors
- **duration_minutes**: Movie duration
- **box_office**: Box office earnings

## API Examples

The search engine simulates these common movie search API patterns:

1. **Search**: `/search?q={query}&genre={genre}&year={year}`
2. **Filter**: `/movies?genre={genre}&min_rating={rating}`
3. **Similar**: `/movies/{id}/similar`
4. **Stats**: `/movies/stats`

## Troubleshooting

### Elasticsearch not starting?
```bash
# Check if Docker is running
docker info

# Check container status
docker-compose ps

# View logs
docker-compose logs elasticsearch
```

### Import errors?
```bash
# Make sure virtual environment is activated
source .venv/Scripts/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Connection refused?
```bash
# Test Elasticsearch connection
curl http://localhost:9200

# Test with the connection script
python test_basic.py --connection-only
```

## Clean Code Practices

- Meaningful variable names
- Comprehensive docstrings
- Reusable functions
- Configuration management
- Error handling
- Type hints

## Performance

- **Index size**: ~15 movies, <1MB
- **Search speed**: <50ms typical response time
- **Aggregations**: Real-time statistics and analytics
- **Scalability**: Ready for thousands of movies

## Services URLs

Once everything is running:
- **Elasticsearch**: http://localhost:9200
- **Kibana** (optional): http://localhost:5601

## Next Steps

After setup, you can:
1. Use the interactive search interface
2. Explore the sample dataset
3. Test different search queries
4. View aggregation statistics
5. Try similarity search features

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

- Meaningful variable names
- Comprehensive docstrings
- Reusable functions
- Configuration management
- Error handling
- Type hints
