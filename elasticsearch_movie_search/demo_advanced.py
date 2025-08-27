"""
Advanced features demonstration for the Movie Search Engine.

This script demonstrates the more advanced features including
vector similarity, autocomplete, complex aggregations, and
custom scoring.
"""

from src.movie_search_engine import MovieSearchEngine
from src.elasticsearch_client import ElasticsearchClient


def demonstrate_autocomplete():
"""Demonstrate the autocomplete functionality."""
print("\n🔤 AUTOCOMPLETE DEMONSTRATION")
print("=" * 50)

engine = MovieSearchEngine()

test_queries = ["bat", "lor", "toy", "mat"]

for query in test_queries:
print(f"\nTip: Autocomplete for '{query}':")
suggestions = engine.autocomplete_movies(query, size=5)

if suggestions:
for i, suggestion in enumerate(suggestions, 1):
print(f" {i}. {suggestion}")
else:
print(" No suggestions found")


def demonstrate_similarity_search():
"""Demonstrate the similarity search functionality."""
print("\nSIMILARITY SEARCH DEMONSTRATION")
print("=" * 50)

engine = MovieSearchEngine()

# Test with different movie IDs
test_movies = [1, 5, 8] # Dark Knight, Matrix, Spider-Verse

for movie_id in test_movies:
print(f"\nTitle: Finding movies similar to movie ID {movie_id}:")

# Get reference movie
reference = engine.get_movie_by_id(movie_id)
if "error" not in reference:
print(f" Reference: {reference['title']} ({reference['release_year']})")
print(f" Genres: Genres: {', '.join(reference['genres'])}")

# Find similar movies
similar_results = engine.find_similar_movies(movie_id, size=3)

if similar_results.get('results'):
print(f" Similar movies:")
for movie in similar_results['results']:
print(f" - {movie['title']} - Score: {movie.get('score', 0):.2f}")
else:
print(" No similar movies found")


def demonstrate_advanced_aggregations():
"""Demonstrate advanced aggregation queries."""
print("\nADVANCED AGGREGATIONS DEMONSTRATION")
print("=" * 50)

engine = MovieSearchEngine()

# Get comprehensive statistics
stats = engine.get_movie_statistics()

if "error" in stats:
print(f"ERROR: Error getting statistics: {stats['error']}")
return

print(f"Database Overview:")
print(f" - Total Movies: {stats.get('total_movies', 0)}")
print(f" - Average Rating: {stats.get('avg_rating', 0)}")

# Genre distribution
genres = stats.get('genres', [])
print(f"\nGenres: Genre Distribution:")
for genre in genres[:8]:
percentage = (genre['count'] / stats.get('total_movies', 1)) * 100
print(f" - {genre['genre']}: {genre['count']} movies ({percentage:.1f}%)")

# Movies by year
years = stats.get('movies_by_year', [])
if years:
print(f"\nYear: Movies by Decade:")
decade_counts = {}
for year_data in years:
decade = (int(year_data['year']) // 10) * 10
decade_counts[decade] = decade_counts.get(decade, 0) + year_data['count']

for decade in sorted(decade_counts.keys()):
print(f" - {decade}s: {decade_counts[decade]} movies")

# Top directors
directors = stats.get('top_directors', [])
print(f"\nTitle: Most Prolific Directors:")
for director in directors[:5]:
print(f" - {director['director']}: {director['movies']} movies")

# Box office analysis
box_office = stats.get('box_office_stats', {})
if box_office:
print(f"\nBox Office: Box Office Analysis:")
print(f" - Total Revenue: ${box_office.get('sum', 0):,.0f}")
print(f" - Average per Movie: ${box_office.get('avg', 0):,.0f}")
print(f" - Highest Grossing: ${box_office.get('max', 0):,.0f}")
print(f" - Lowest Grossing: ${box_office.get('min', 0):,.0f}")


def demonstrate_complex_search_scenarios():
"""Demonstrate complex search scenarios with multiple filters."""
print("\nCOMPLEX SEARCH SCENARIOS")
print("=" * 50)

engine = MovieSearchEngine()

scenarios = [
{
"name": "High-rated Action Movies from 2000s",
"params": {
"genre": "Action",
"min_year": 2000,
"max_year": 2009,
"min_rating": 8.0,
"sort_by": "rating",
"size": 5
}
},
{
"name": "Christopher Nolan Movies",
"params": {
"director": "Christopher Nolan",
"sort_by": "release_year",
"size": 5
}
},
{
"name": "Recent Animated Movies",
"params": {
"query": "animated",
"min_year": 2010,
"sort_by": "release_year",
"sort_order": "desc",
"size": 3
}
},
{
"name": "Epic Fantasy Adventures",
"params": {
"query": "adventure fantasy",
"min_rating": 8.0,
"sort_by": "rating",
"size": 3
}
}
]

for scenario in scenarios:
print(f"\n{scenario['name']}:")
print("-" * 40)

results = engine.search_movies(**scenario['params'])

if results.get('results'):
for movie in results['results']:
score_info = f" (Score: {movie.get('score', 0):.2f})" if movie.get('score') else ""
print(f" - {movie['title']} ({movie['release_year']}) - Rating:{movie['rating']}{score_info}")
print(f" Genres: {', '.join(movie['genres'])}")
else:
print(" No results found")


def demonstrate_advanced_search_features():
"""Demonstrate advanced search features with custom parameters."""
print("\n⚡ ADVANCED SEARCH FEATURES")
print("=" * 50)

engine = MovieSearchEngine()

# Test advanced search with custom boosting
advanced_params = {
"query": "space",
"genres": ["Sci-Fi", "Action"],
"year_range": {"min": 1990, "max": 2020},
"rating_range": {"min": 7.0, "max": 10.0},
"sort": [{"rating": {"order": "desc"}}],
"size": 5
}

print("Advanced Search: Space Sci-Fi/Action movies (1990-2020, 7.0+ rating)")
print("-" * 60)

results = engine.advanced_search(advanced_params)

if results.get('results'):
for movie in results['results']:
print(f" - {movie['title']} ({movie['release_year']})")
print(f" Rating: Rating: {movie['rating']}")
print(f" Genres: Genres: {', '.join(movie['genres'])}")
print(f" Description: {movie['description'][:100]}...")
print()
else:
print(" No results found")


def run_performance_tests():
"""Run basic performance tests on search operations."""
print("\n⚡ PERFORMANCE TESTING")
print("=" * 50)

engine = MovieSearchEngine()

import time

# Test different search operations
tests = [
("Basic text search", lambda: engine.search_movies(query="action", size=10)),
("Filtered search", lambda: engine.search_movies(genre="Action", min_year=2000, size=10)),
("Complex search", lambda: engine.search_movies(query="batman", genre="Action", min_rating=8.0, size=10)),
("Statistics aggregation", lambda: engine.get_movie_statistics()),
("Similarity search", lambda: engine.find_similar_movies(1, size=5)),
("Autocomplete", lambda: engine.autocomplete_movies("bat", size=10))
]

print("🏃 Running performance tests...")

for test_name, test_func in tests:
start_time = time.time()
result = test_func()
end_time = time.time()

execution_time = (end_time - start_time) * 1000 # Convert to ms

if isinstance(result, dict) and 'took' in result:
es_time = result['took']
print(f" - {test_name}: {execution_time:.1f}ms total, {es_time}ms ES query")
else:
print(f" - {test_name}: {execution_time:.1f}ms")


def main():
"""Run all advanced demonstrations."""
print("Title: ELASTICSEARCH MOVIE SEARCH ENGINE")
print("🌟 ADVANCED FEATURES DEMONSTRATION")
print("=" * 60)
print("This demo showcases the advanced capabilities of the search engine")
print("including autocomplete, similarity search, and complex aggregations.")
print("=" * 60)

try:
# Check if we can connect to Elasticsearch
client = ElasticsearchClient()
if not client.index_exists():
print("ERROR: Movie index not found. Please run 'python main.py' first to set up the database.")
return

print("SUCCESS: Connected to Elasticsearch and found movie index")

# Run all demonstrations
demonstrate_autocomplete()
demonstrate_similarity_search()
demonstrate_advanced_aggregations()
demonstrate_complex_search_scenarios()
demonstrate_advanced_search_features()
run_performance_tests()

print("\n🎉 Advanced features demonstration complete!")
print("\nTip: Next steps:")
print(" - Run 'python main.py' for the interactive interface")
print(" - Explore the source code in src/ directory")
print(" - Try your own custom search queries")

except Exception as e:
print(f"ERROR: Demo failed: {e}")
print("Make sure Elasticsearch is running and the movie data is indexed.")


if __name__ == "__main__":
main()
