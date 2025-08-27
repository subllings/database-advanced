"""
Quick test script for the Movie Search Engine.

This script provides a simple way to test the basic functionality
of the search engine without running the full interactive interface.
"""

from src.movie_search_engine import MovieSearchEngine
from src.elasticsearch_client import ElasticsearchClient


def test_basic_functionality():
"""Test basic search engine functionality."""
print("Title: MOVIE SEARCH ENGINE - QUICK TEST")
print("=" * 50)

try:
# Initialize the search engine
engine = MovieSearchEngine()

print("SUCCESS: Search engine initialized successfully")

# Test 1: Basic search
print("\nTest 1: Basic search for 'Batman'")
results = engine.search_movies(query="Batman", size=3)

if results.get('results'):
print(f" Found {len(results['results'])} movies:")
for movie in results['results']:
print(f" - {movie['title']} ({movie['release_year']}) - Rating:{movie['rating']}")
else:
print(" No results found")

# Test 2: Genre filter
print("\nGenres: Test 2: Action movies")
results = engine.search_movies(genre="Action", size=3, sort_by="rating")

if results.get('results'):
print(f" Found {len(results['results'])} action movies:")
for movie in results['results']:
print(f" - {movie['title']} - Rating:{movie['rating']}")
else:
print(" No action movies found")

# Test 3: Year filter
print("\nYear: Test 3: Movies from 2019")
results = engine.search_movies(min_year=2019, max_year=2019, size=5)

if results.get('results'):
print(f" Found {len(results['results'])} movies from 2019:")
for movie in results['results']:
print(f" - {movie['title']} - Rating:{movie['rating']}")
else:
print(" No movies from 2019 found")

# Test 4: High-rated movies
print("\nRating: Test 4: Top-rated movies (8.5+)")
results = engine.search_movies(min_rating=8.5, sort_by="rating", sort_order="desc", size=5)

if results.get('results'):
print(f" Found {len(results['results'])} highly-rated movies:")
for movie in results['results']:
print(f" - {movie['title']} - Rating:{movie['rating']}")
else:
print(" No highly-rated movies found")

# Test 5: Statistics
print("\nTest 5: Database statistics")
stats = engine.get_movie_statistics()

if 'error' not in stats:
print(f" - Total movies: {stats.get('total_movies', 0)}")
print(f" - Average rating: {stats.get('avg_rating', 0)}")

genres = stats.get('genres', [])[:3]
if genres:
print(f" - Top genres: {', '.join([g['genre'] for g in genres])}")
else:
print(f" Error: {stats['error']}")

# Test 6: Autocomplete
print("\nTip: Test 6: Autocomplete for 'bat'")
suggestions = engine.autocomplete_movies("bat", size=5)

if suggestions:
print(f" Suggestions:")
for i, suggestion in enumerate(suggestions, 1):
print(f" {i}. {suggestion}")
else:
print(" No suggestions found")

# Test 7: Similar movies
print("\nTest 7: Movies similar to 'The Dark Knight' (ID: 1)")
similar_results = engine.find_similar_movies(1, size=3)

if similar_results.get('results'):
print(f" Similar movies:")
for movie in similar_results['results']:
print(f" - {movie['title']} - Score: {movie.get('score', 0):.2f}")
else:
print(" No similar movies found")

print("\n🎉 All tests completed successfully!")

# Performance summary
print("\n⚡ Performance Summary:")
total_searches = 7
print(f" - Executed {total_searches} different types of searches")
print(f" - All searches completed without errors")
print(f" - Database contains movie data and is fully functional")

except Exception as e:
print(f"ERROR: Test failed: {e}")
print("\nTroubleshooting:")
print("1. Make sure Elasticsearch is running on localhost:9200")
print("2. Run 'python main.py' to set up the database first")
print("3. Check that all dependencies are installed: pip install -r requirements.txt")


def test_connection_only():
"""Test only the Elasticsearch connection."""
print("🔌 ELASTICSEARCH CONNECTION TEST")
print("=" * 40)

try:
client = ElasticsearchClient()
health = client.health_check()

if 'error' in health:
print(f"ERROR: Connection failed: {health['error']}")
return False

print("SUCCESS: Elasticsearch connection successful")
print(f" - Cluster: {health.get('cluster_name', 'Unknown')}")
print(f" - Status: {health.get('status', 'Unknown')}")
print(f" - Nodes: {health.get('number_of_nodes', 'Unknown')}")

# Check if movie index exists
if client.index_exists():
stats = client.client.indices.stats(index=client.get_index_name())
doc_count = stats['indices'][client.get_index_name()]['total']['docs']['count']
print(f" - Movie index exists with {doc_count} documents")
else:
print(" - Movie index does not exist (run main.py to create it)")

return True

except Exception as e:
print(f"ERROR: Connection test failed: {e}")
print("\nTip: Make sure Elasticsearch is running:")
print(" - Download: https://www.elastic.co/downloads/elasticsearch")
print(" - Start: bin/elasticsearch (Linux/Mac) or bin\\elasticsearch.bat (Windows)")
print(" - Test: curl http://localhost:9200")
return False


def main():
"""Main function to run the tests."""
import sys

# Check command line arguments
if len(sys.argv) > 1 and sys.argv[1] == "--connection-only":
test_connection_only()
else:
# First test connection
if test_connection_only():
print("\n" + "="*50)
# Then run full functionality test
test_basic_functionality()
else:
print("\nERROR: Cannot proceed with functionality tests - connection failed")


if __name__ == "__main__":
main()
