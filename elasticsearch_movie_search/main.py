#!/usr/bin/env python3
"""
Elasticsearch Movie Search Demo Application

Interactive demonstration of movie search capabilities using Elasticsearch,
including text search, filters, and analytics.
"""

import sys
import os
from typing import Dict, Any
from src.elasticsearch_client import ElasticsearchClient
from src.data_indexer_fixed import MovieDataIndexer
from src.movie_search_engine_simple import MovieSearchEngine
from src.search_interface_simple import MovieSearchInterface

def print_header():
    """Print application header"""
    print("=" * 60)
    print("ELASTICSEARCH MOVIE SEARCH DEMO")
    print("=" * 60)
    print()

def print_section_header(title: str):
    """Print section header"""
    print(f"\n{'-' * 50}")
    print(f" {title}")
    print(f"{'-' * 50}")

def check_elasticsearch_connection(client: ElasticsearchClient) -> bool:
    """
    Check if Elasticsearch is available and print connection status
    
    Args:
        client: Elasticsearch client instance
        
    Returns:
        True if connection is successful, False otherwise
    """
    print_section_header("ELASTICSEARCH CONNECTION")
    
    try:
        if client.test_connection():
            # Get cluster info
            cluster_info = client.get_cluster_info()
            if cluster_info:
                print(f"Cluster Name: {cluster_info.get('cluster_name', 'Unknown')}")
                print(f"Version: {cluster_info.get('version', 'Unknown')}")
                print(f"Status: {cluster_info.get('status', 'Unknown')}")
                print(f"Nodes: {cluster_info.get('number_of_nodes', 0)}")
            return True
        else:
            print("ERROR: Could not connect to Elasticsearch")
            print("Please ensure Elasticsearch is running on localhost:9200")
            return False
            
    except Exception as e:
        print(f"ERROR: Connection failed - {e}")
        print("Please ensure Elasticsearch is running on localhost:9200")
        return False

def setup_movie_index(indexer: MovieDataIndexer) -> bool:
    """
    Set up the movie index with sample data
    
    Args:
        indexer: Movie data indexer instance
        
    Returns:
        True if setup is successful, False otherwise
    """
    print_section_header("MOVIE INDEX SETUP")
    
    try:
        # Check if index already exists and has data
        index_info = indexer.get_index_info()
        if index_info and index_info.get('document_count', 0) > 0:
            print(f"Movie index already exists with {index_info['document_count']} movies")
            return True
        
        # Create index and load sample data
        print("Creating movie index...")
        if indexer.setup_index():
            print("Loading sample movie data...")
            success, count = indexer.index_sample_movies()
            if success:
                print(f"Successfully indexed {count} movies")
                return True
            else:
                print("ERROR: Failed to index sample movies")
                return False
        else:
            print("ERROR: Failed to create movie index")
            return False
            
    except Exception as e:
        print(f"ERROR: Index setup failed - {e}")
        return False

def run_search_demo(search_engine):
    """
    Run interactive search demonstrations
    
    Args:
        search_engine: Movie search engine instance
    """
    print_section_header("SEARCH DEMONSTRATIONS")
    
    # Demo searches
    demo_queries = [
        "action adventure",
        "romantic comedy", 
        "science fiction",
        "thriller mystery"
    ]
    
    for query in demo_queries:
        print(f"\nSearching for: '{query}'")
        print("-" * 30)
        
        try:
            results = search_engine.search_movies(query, size=3)
            if results and 'hits' in results:
                movies = results['hits']['hits']
                if movies:
                    for i, movie in enumerate(movies, 1):
                        source = movie['_source']
                        score = movie['_score']
                        print(f"{i}. {source.get('title', 'Unknown')} ({source.get('year', 'N/A')})")
                        print(f"   Score: {score:.2f}")
                        print(f"   Genre: {', '.join(source.get('genres', []))}")
                        if source.get('description'):
                            desc = source['description'][:100] + "..." if len(source['description']) > 100 else source['description']
                            print(f"   Description: {desc}")
                        print()
                else:
                    print("No movies found for this search")
            else:
                print("Search returned no results")
                
        except Exception as e:
            print(f"ERROR: Search failed - {e}")

def run_filter_demo(search_engine):
    """
    Run filter demonstrations
    
    Args:
        search_engine: Movie search engine instance
    """
    print_section_header("FILTER DEMONSTRATIONS")
    
    # Demo filters
    filter_demos = [
        {
            'title': 'Movies from 2020 onwards',
            'filters': {'year_from': 2020}
        },
        {
            'title': 'Action movies',
            'filters': {'genres': ['Action']}
        },
        {
            'title': 'High-rated movies (8.0+)',
            'filters': {'rating_from': 8.0}
        }
    ]
    
    for demo in filter_demos:
        print(f"\nFilter: {demo['title']}")
        print("-" * 30)
        
        try:
            results = search_engine.search_movies("", filters=demo['filters'], size=3)
            if results and 'hits' in results:
                movies = results['hits']['hits']
                if movies:
                    for i, movie in enumerate(movies, 1):
                        source = movie['_source']
                        print(f"{i}. {source.get('title', 'Unknown')} ({source.get('year', 'N/A')})")
                        print(f"   Genre: {', '.join(source.get('genres', []))}")
                        print(f"   Rating: {source.get('rating', 'N/A')}")
                        print()
                else:
                    print("No movies found matching these filters")
            else:
                print("Filter returned no results")
                
        except Exception as e:
            print(f"ERROR: Filter search failed - {e}")

def show_index_statistics(indexer):
    """
    Show index statistics and information
    
    Args:
        indexer: Movie data indexer instance
    """
    print_section_header("INDEX STATISTICS")
    
    try:
        index_info = indexer.get_index_info()
        if index_info and 'error' not in index_info:
            print(f"Index Name: {index_info.get('index_name', 'Unknown')}")
            print(f"Total Movies: {index_info.get('document_count', 0)}")
            print(f"Storage Size: {index_info.get('store_size', 0)} bytes")
            
            # Show mapping info if available
            mapping = index_info.get('mapping', {})
            if mapping and 'properties' in mapping:
                print(f"Fields: {len(mapping['properties'])}")
                print("Available fields:", ", ".join(mapping['properties'].keys()))
        else:
            print("Could not retrieve index information")
            
    except Exception as e:
        print(f"ERROR: Failed to get index statistics - {e}")

def main():
    """Main application entry point"""
    print_header()
    
    try:
        # Initialize Elasticsearch client
        print("Initializing Elasticsearch connection...")
        client = ElasticsearchClient()
        
        # Check connection
        if not check_elasticsearch_connection(client):
            print("\nPlease start Elasticsearch and try again.")
            sys.exit(1)
        
        # Initialize components
        indexer = MovieDataIndexer(client)
        search_engine = MovieSearchEngine(client)
        
        # Setup movie index
        if not setup_movie_index(indexer):
            print("\nFailed to setup movie index. Exiting.")
            sys.exit(1)
        
        # Show index statistics
        show_index_statistics(indexer)
        
        # Run demonstrations
        run_search_demo(search_engine)
        run_filter_demo(search_engine)
        
        # Offer interactive search
        print_section_header("INTERACTIVE SEARCH")
        print("Starting interactive search interface...")
        print("Type 'quit' or 'exit' to end the session")
        print()
        
        # Start interactive interface
        interface = MovieSearchInterface(search_engine)
        interface.start_interactive_search()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nERROR: Application failed - {e}")
        sys.exit(1)
    finally:
        print("\nDemo completed. Thank you for using Elasticsearch Movie Search!")

if __name__ == "__main__":
    main()
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
        
        print(f"Elasticsearch is healthy: {health['status']} cluster")
        return True
        
    except Exception as e:
        print(f"Cannot connect to Elasticsearch: {e}")
        print("\nMake sure Elasticsearch is running:")
        print("   1. Download from: https://www.elastic.co/downloads/elasticsearch")
        print("   2. Start with: bin/elasticsearch (Linux/Mac) or bin\\elasticsearch.bat (Windows)")
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
            print("Failed to index movie data")
            return False
            
    except Exception as e:
        print(f"Database setup failed: {e}")
        return False

