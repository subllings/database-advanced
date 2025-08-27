#!/usr/bin/env python3
"""
Complete Elasticsearch Movie Search Application
Single file with all functionality - NO ICONS
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError


class ElasticsearchClient:
    """Simple Elasticsearch client wrapper"""
    
    def __init__(self, host='localhost', port=9200):
        self.host = host
        self.port = port
        self.client = Elasticsearch([f'http://{host}:{port}'])
    
    def test_connection(self) -> bool:
        """Test connection to Elasticsearch"""
        try:
            return self.client.ping()
        except Exception:
            return False


class MovieSearchEngine:
    """Complete movie search engine with all features"""
    
    def __init__(self, client: ElasticsearchClient):
        self.client = client.client
        self.index_name = 'movies'
        self.setup_index()
        self.load_sample_data()
    
    def setup_index(self):
        """Create index with proper mapping"""
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "standard"},
                    "description": {"type": "text", "analyzer": "standard"},
                    "genres": {"type": "keyword"},
                    "director": {"type": "keyword"},
                    "actors": {"type": "keyword"},
                    "release_year": {"type": "integer"},
                    "rating": {"type": "float"},
                    "duration_minutes": {"type": "integer"},
                    "box_office": {"type": "long"}
                }
            }
        }
        
        try:
            if not self.client.indices.exists(index=self.index_name):
                self.client.indices.create(index=self.index_name, mappings=mapping["mappings"])
                print(f"Created index: {self.index_name}")
            else:
                print(f"Index {self.index_name} already exists")
        except Exception as e:
            print(f"Error creating index: {e}")
    
    def load_sample_data(self):
        """Load sample movie data"""
        movies = [
            {
                "title": "The Shawshank Redemption",
                "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "genres": ["Drama"],
                "director": "Frank Darabont",
                "actors": ["Tim Robbins", "Morgan Freeman"],
                "release_year": 1994,
                "rating": 9.3,
                "duration_minutes": 142,
                "box_office": 16000000
            },
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological and physical tests.",
                "genres": ["Action", "Crime", "Drama"],
                "director": "Christopher Nolan",
                "actors": ["Christian Bale", "Heath Ledger"],
                "release_year": 2008,
                "rating": 9.0,
                "duration_minutes": 152,
                "box_office": 1004558444
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                "genres": ["Action", "Sci-Fi", "Thriller"],
                "director": "Christopher Nolan",
                "actors": ["Leonardo DiCaprio", "Marion Cotillard"],
                "release_year": 2010,
                "rating": 8.8,
                "duration_minutes": 148,
                "box_office": 829895144
            },
            {
                "title": "Pulp Fiction",
                "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "genres": ["Crime", "Drama"],
                "director": "Quentin Tarantino",
                "actors": ["John Travolta", "Uma Thurman"],
                "release_year": 1994,
                "rating": 8.9,
                "duration_minutes": 154,
                "box_office": 214179088
            },
            {
                "title": "The Matrix",
                "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
                "genres": ["Action", "Sci-Fi"],
                "director": "Lana Wachowski",
                "actors": ["Keanu Reeves", "Laurence Fishburne"],
                "release_year": 1999,
                "rating": 8.7,
                "duration_minutes": 136,
                "box_office": 467222824
            }
        ]
        
        # Check if data already exists
        try:
            count = self.client.count(index=self.index_name)['count']
            if count > 0:
                print(f"Index already has {count} movies")
                return
        except Exception:
            pass
        
        # Index the movies
        for i, movie in enumerate(movies):
            try:
                self.client.index(index=self.index_name, id=str(i+1), document=movie)
            except Exception as e:
                print(f"Error indexing movie {movie['title']}: {e}")
        
        print(f"Indexed {len(movies)} movies")
    
    def search_movies(self, query: str, size: int = 10) -> List[Dict]:
        """Search movies by text query"""
        if not query.strip():
            return []
        
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "description", "genres", "director", "actors"]
                }
            },
            "size": size,
            "sort": [{"_score": {"order": "desc"}}]
        }
        
        try:
            response = self.client.search(index=self.index_name, query=search_body["query"], size=size, sort=search_body["sort"])
            results = []
            for hit in response['hits']['hits']:
                movie = hit['_source']
                movie['score'] = hit['_score']
                results.append(movie)
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def filter_movies(self, genre: Optional[str] = None, min_year: Optional[int] = None, max_year: Optional[int] = None, min_rating: Optional[float] = None) -> List[Dict]:
        """Filter movies by criteria"""
        filters = []
        
        if genre:
            filters.append({"term": {"genres": genre}})
        if min_year:
            filters.append({"range": {"release_year": {"gte": min_year}}})
        if max_year:
            filters.append({"range": {"release_year": {"lte": max_year}}})
        if min_rating:
            filters.append({"range": {"rating": {"gte": min_rating}}})
        
        if not filters:
            return []
        
        search_body = {
            "bool": {
                "filter": filters
            }
        }
        
        try:
            response = self.client.search(index=self.index_name, query=search_body, sort=[{"rating": {"order": "desc"}}])
            return [hit['_source'] for hit in response['hits']['hits']]
        except Exception as e:
            print(f"Filter error: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            # Total count
            total = self.client.count(index=self.index_name)['count']
            
            # Genre aggregation
            genre_response = self.client.search(
                index=self.index_name, 
                aggs={"genres": {"terms": {"field": "genres", "size": 10}}},
                size=0
            )
            genres = [(bucket['key'], bucket['doc_count']) 
                     for bucket in genre_response['aggregations']['genres']['buckets']]
            
            # Rating stats
            rating_response = self.client.search(
                index=self.index_name,
                aggs={"rating_stats": {"stats": {"field": "rating"}}},
                size=0
            )
            rating_stats = rating_response['aggregations']['rating_stats']
            
            return {
                'total_movies': total,
                'genres': genres,
                'rating_stats': {
                    'min': rating_stats['min'],
                    'max': rating_stats['max'],
                    'avg': round(rating_stats['avg'], 2) if rating_stats['avg'] else 0
                }
            }
        except Exception as e:
            print(f"Statistics error: {e}")
            return {}


def print_movies(movies: List[Dict], title: str = "Search Results"):
    """Print movie results"""
    print(f"\n{title}")
    print("-" * 50)
    
    if not movies:
        print("No movies found")
        return
    
    for i, movie in enumerate(movies, 1):
        score_text = f" (Score: {movie['score']:.2f})" if 'score' in movie else ""
        print(f"{i}. {movie['title']} ({movie['release_year']}){score_text}")
        print(f"   Director: {movie['director']}")
        print(f"   Rating: {movie['rating']}")
        print(f"   Genres: {', '.join(movie['genres'])}")
        if len(movie['description']) > 80:
            print(f"   Description: {movie['description'][:80]}...")
        else:
            print(f"   Description: {movie['description']}")
        print()


def print_statistics(stats: Dict[str, Any]):
    """Print database statistics"""
    print("\nDatabase Statistics")
    print("-" * 50)
    
    if not stats:
        print("No statistics available")
        return
    
    print(f"Total Movies: {stats.get('total_movies', 0)}")
    
    if 'rating_stats' in stats:
        rating = stats['rating_stats']
        print(f"Rating Range: {rating.get('min', 0)} - {rating.get('max', 0)}")
        print(f"Average Rating: {rating.get('avg', 0)}")
    
    if 'genres' in stats and stats['genres']:
        print("\nGenre Distribution:")
        for genre, count in stats['genres']:
            print(f"  {genre}: {count} movies")


def main():
    """Main application"""
    print("=" * 60)
    print("ELASTICSEARCH MOVIE SEARCH")
    print("=" * 60)
    
    # Initialize
    client = ElasticsearchClient()
    if not client.test_connection():
        print("ERROR: Cannot connect to Elasticsearch at localhost:9200")
        print("Please make sure Elasticsearch is running")
        return
    
    print("Connected to Elasticsearch successfully")
    
    # Initialize search engine
    engine = MovieSearchEngine(client)
    
    # Interactive menu
    while True:
        print("\n" + "=" * 40)
        print("MOVIE SEARCH MENU")
        print("=" * 40)
        print("1. Search movies by text")
        print("2. Filter by genre")
        print("3. Filter by year range")
        print("4. Filter by rating")
        print("5. Show all movies")
        print("6. Database statistics")
        print("7. Quit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            query = input("Enter search terms: ").strip()
            if query:
                results = engine.search_movies(query)
                print_movies(results, f"Search Results for '{query}'")
        
        elif choice == '2':
            genre = input("Enter genre (Action, Drama, Sci-Fi, Crime, Thriller): ").strip()
            if genre:
                results = engine.filter_movies(genre=genre)
                print_movies(results, f"Movies in genre '{genre}'")
        
        elif choice == '3':
            try:
                min_year = int(input("Enter minimum year: "))
                max_year = int(input("Enter maximum year: "))
                results = engine.filter_movies(min_year=min_year, max_year=max_year)
                print_movies(results, f"Movies from {min_year} to {max_year}")
            except ValueError:
                print("Please enter valid years")
        
        elif choice == '4':
            try:
                min_rating = float(input("Enter minimum rating (0-10): "))
                results = engine.filter_movies(min_rating=min_rating)
                print_movies(results, f"Movies with rating >= {min_rating}")
            except ValueError:
                print("Please enter a valid rating")
        
        elif choice == '5':
            # Get all movies
            all_movies = engine.filter_movies()  # No filters = all movies
            if not all_movies:
                # Fallback: search for all
                try:
                    response = engine.client.search(index=engine.index_name, query={"match_all": {}}, size=100)
                    all_movies = [hit['_source'] for hit in response['hits']['hits']]
                except Exception as e:
                    print(f"Error getting all movies: {e}")
                    all_movies = []
            print_movies(all_movies, "All Movies")
        
        elif choice == '6':
            stats = engine.get_statistics()
            print_statistics(stats)
        
        elif choice == '7':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
