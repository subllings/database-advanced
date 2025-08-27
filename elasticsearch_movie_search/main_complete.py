#!/usr/bin/env python3
"""
Complete Movie Search Engine - Main Application Entry Point

This is the complete implementation of the Movie Search Engine with Elasticsearch.
Features include:
- Full-text search across titles and descriptions
- Multi-field filtering (genre, year, rating, director, etc.)
- Sorting by various criteria (rating, popularity, year)
- Advanced features: autocomplete, "more like this", aggregations
- Comprehensive statistics and analytics
- Interactive command-line interface

Requirements:
- Elasticsearch running on localhost:9200
- Python 3.12+ with required packages
- Movie data indexed in Elasticsearch

Usage:
    python main.py
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.elasticsearch_client import ElasticsearchClient
from src.data_indexer_fixed import MovieDataIndexer
from src.movie_search_engine_complete import MovieSearchEngine
from src.search_interface_complete import MovieSearchInterface


def check_elasticsearch_connection():
    """Check if Elasticsearch is running and accessible."""
    es_client = ElasticsearchClient()
    
    if not es_client.test_connection():
        print("ERROR: Cannot connect to Elasticsearch!")
        print("Please ensure Elasticsearch is running on localhost:9200")
        print("\nTo start Elasticsearch:")
        print("1. Run: ./start-elasticsearch.sh")
        print("2. Wait for startup (30-60 seconds)")
        print("3. Run this script again")
        return False
    
    return True


def setup_initial_data():
    """Set up initial movie data if needed."""
    es_client = ElasticsearchClient()
    data_indexer = MovieDataIndexer(es_client)
    
    try:
        # Check if index exists and has data
        count_response = es_client.client.count(index=es_client.index_name)
        doc_count = count_response.get('count', 0)
        
        if doc_count == 0:
            print("No movie data found. Setting up sample data...")
            print("Creating movie index...")
            
            # Index sample movies
            indexed_count = data_indexer.index_sample_movies()
            print(f"Successfully indexed {indexed_count} sample movies.")
            return True
        else:
            print(f"Found {doc_count} movies in database.")
            return True
            
    except Exception as e:
        print(f"Error setting up data: {e}")
        print("Will attempt to create index and data...")
        
        try:
            indexed_count = data_indexer.index_sample_movies()
            print(f"Successfully created index and indexed {indexed_count} movies.")
            return True
        except Exception as setup_error:
            print(f"Failed to setup initial data: {setup_error}")
            return False


def main():
    """Main application entry point."""
    print("Starting Complete Movie Search Engine...")
    print("=" * 50)
    
    # Check Elasticsearch connection
    if not check_elasticsearch_connection():
        sys.exit(1)
    
    print("Connected to Elasticsearch successfully!")
    
    # Setup initial data if needed
    if not setup_initial_data():
        print("WARNING: Could not setup initial movie data.")
        print("Some features may not work correctly.")
        print()
    
    # Start the interactive interface
    try:
        print("Starting interactive movie search interface...")
        interface = MovieSearchInterface()
        interface.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check your Elasticsearch connection and try again.")
    finally:
        print("Movie Search Engine terminated.")


if __name__ == "__main__":
    main()
