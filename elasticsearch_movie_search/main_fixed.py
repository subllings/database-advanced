#!/usr/bin/env python3
"""
Main entry point for the Movie Search Engine project.

This script coordinates the entire movie search engine setup and demonstration,
including data indexing and search interface initialization.
"""

import sys
import time
from src.elasticsearch_client import ElasticsearchClient
from src.data_indexer import MovieDataIndexer
from src.movie_search_engine import MovieSearchEngine
from src.search_interface import MovieSearchInterface


def check_elasticsearch_connection() -> bool:
    """
    Check if Elasticsearch is available and ready.
    
    Returns:
        True if Elasticsearch is accessible, False otherwise
    """
    try:
        client = ElasticsearchClient()
        health = client.health_check()
        
        if 'error' in health:
            print(f"Elasticsearch health check failed: {health['error']}")
            return False
            
        print(f"Connected to Elasticsearch at {client.host}:{client.port}")
        print(f"Elasticsearch is healthy: {health.get('status', 'unknown')} cluster")
        return True
        
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {e}")
        print("\nTroubleshooting:")
        print("   1. Make sure Docker Desktop is running")
        print("   2. Start Elasticsearch: ./start-elasticsearch.sh")
        print("   3. Verify it's running: curl http://localhost:9200")
        return False


def setup_movie_database() -> bool:
    """
    Set up the movie database by indexing sample data.
    
    Returns:
        True if setup successful, False otherwise
    """
    try:
        print("\nSetting up movie database...")
        
        # Initialize indexer
        indexer = MovieDataIndexer()
        
        # Check if index already exists with data
        if indexer.es_client.index_exists():
            stats = indexer.get_index_stats()
            if stats.get('document_count', 0) > 0:
                print(f"Movie database already exists with {stats['document_count']} movies")
                return True
        
        # Create sample data and index it
        print("Creating sample movie data...")
        movies = indexer.create_sample_movies()
        
        print("Saving data to file...")
        indexer.save_sample_data(movies)
        
        print("Indexing movies into Elasticsearch...")
        success = indexer.index_movies(movies)
        
        if success:
            # Show final statistics
            stats = indexer.get_index_stats()
            print("\nDatabase Setup Complete!")
            print(f"   - Movies indexed: {stats.get('document_count', 0)}")
            print(f"   - Index size: {stats.get('index_size_mb', 0)} MB")
            return True
        else:
            print("Failed to index movies")
            return False
            
    except Exception as e:
        print(f"Database setup failed: {e}")
        print("\nDatabase setup failed. Please check the logs and try again.")
        return False


def run_quick_demo() -> None:
    """Run a quick demonstration of search capabilities."""
    try:
        print("\nRunning Quick Demo...")
        engine = MovieSearchEngine()
        
        # Demo searches
        demos = [
            {
                "title": "Search for Batman movies",
                "params": {"query": "Batman", "size": 3}
            },
            {
                "title": "Action movies from 2000+", 
                "params": {"filters": {"genres": ["Action"], "year_range": {"from": 2000}}, "size": 3}
            },
            {
                "title": "Top rated movies",
                "params": {"sort": [{"rating": {"order": "desc"}}], "size": 3}
            }
        ]
        
        for demo in demos:
            print(f"\n{demo['title']}:")
            print("-" * 40)
            
            results = engine.search_movies(**demo['params'])
            
            if results.get('results'):
                for movie in results['results']:
                    print(f"   - {movie['title']} ({movie['release_year']}) - Rating: {movie['rating']}")
            else:
                print("   No results found")
        
        # Show database statistics
        stats = engine.get_movie_statistics()
        
        print("\nDatabase Statistics:")
        print("-" * 40)
        if 'error' not in stats:
            print(f"   - Total movies: {stats.get('total_movies', 0)}")
            print(f"   - Average rating: {stats.get('avg_rating', 0)}")
            print(f"   - Top genres: {', '.join([g['genre'] for g in stats.get('genres', [])[:3]])}")
        
        print("\nDemo complete! Ready for interactive search.")
        
    except Exception as e:
        print(f"Demo failed: {e}")


def main():
    """Main application entry point."""
    print("ELASTICSEARCH MOVIE SEARCH ENGINE")
    print("=" * 50)
    print("A comprehensive movie search and analytics system")
    print("featuring full-text search, filtering, and aggregations.")
    print("=" * 50)
    
    # Step 1: Check Elasticsearch connection
    print("\nStep 1: Checking Elasticsearch connection...")
    if not check_elasticsearch_connection():
        print("\nCannot proceed without Elasticsearch. Exiting...")
        sys.exit(1)
    
    # Step 2: Setup database
    print("\nStep 2: Setting up movie database...")
    if not setup_movie_database():
        print("\nDatabase setup failed. Exiting...")
        sys.exit(1)
    
    # Step 3: Run quick demo
    print("\nStep 3: Running quick demonstration...")
    run_quick_demo()
    
    # Step 4: Interactive menu
    while True:
        print("\nWhat would you like to do next?")
        print("1. Start Interactive Search Interface")
        print("2. View Project Documentation")
        print("3. Run Custom Search Tests")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\nStarting Interactive Search Interface...")
            interface = MovieSearchInterface()
            interface.run()
        
        elif choice == "2":
            print("\nProject Documentation:")
            print("=" * 40)
            print("README.md - Complete project documentation")
            print("src/movie_search_engine.py - Core search functionality")
            print("src/search_interface.py - Interactive interface")
            print("data/movies.json - Sample movie dataset")
            print("\nUse the interactive interface (option 1) to explore all features!")
        
        elif choice == "3":
            print("\nRunning Custom Search Tests...")
            engine = MovieSearchEngine()
            
            # Test various search scenarios
            test_queries = [
                "Christopher Nolan",
                "space adventure", 
                "comedy 1990s",
                "high rating action"
            ]
            
            for query in test_queries:
                print(f"\nTesting: '{query}'")
                results = engine.search_movies(query=query, size=3)
                
                if results.get('results'):
                    for movie in results['results']:
                        score_info = f" (Score: {movie.get('score', 0):.2f})" if 'score' in movie else ""
                        print(f"   - {movie['title']} ({movie['release_year']}){score_info}")
                else:
                    print("   No results found")
        
        elif choice == "4":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice. Exiting...")
            break


if __name__ == "__main__":
    main()
