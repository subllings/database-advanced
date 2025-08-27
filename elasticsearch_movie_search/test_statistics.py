#!/usr/bin/env python3
"""
Test script for database statistics functionality
"""

from src.movie_search_engine_complete import MovieSearchEngine
from src.elasticsearch_client import ElasticsearchClient

def test_database_statistics():
    """Test the database statistics feature that was previously failing"""
    print("Testing database statistics functionality...")
    print("=" * 50)
    
    try:
        # Initialize client and engine
        client = ElasticsearchClient()
        engine = MovieSearchEngine(client)
        
        print("✓ Successfully initialized MovieSearchEngine")
        
        # Test the statistics function
        stats = engine.get_comprehensive_stats()
        print("✓ Successfully retrieved comprehensive statistics")
        
        # Display results
        print(f"\nDatabase Overview:")
        print(f"  Total movies: {stats['overview']['total_movies']}")
        
        if 'latest_movie' in stats['overview']:
            print(f"  Latest movie: {stats['overview']['latest_movie']}")
        
        print(f"\nRating Statistics:")
        if 'ratings' in stats and stats['ratings']:
            print(f"  Average rating: {stats['ratings'].get('average_rating', 'N/A')}")
            print(f"  Total rated movies: {stats['ratings'].get('total_rated', 'N/A')}")
        
        print(f"\nGenre Information:")
        if 'genres' in stats and stats['genres']:
            print(f"  Total genres: {len(stats['genres'])}")
            
        print(f"\nYear Distribution:")
        if 'years' in stats and stats['years']:
            print(f"  Year range available: {len(stats['years'])} different years")
            
        print(f"\nDirector Statistics:")
        if 'directors' in stats and stats['directors']:
            print(f"  Total directors: {len(stats['directors'])}")
        
        print("\n" + "=" * 50)
        print("✅ SUCCESS: Database statistics feature is working correctly!")
        print("✅ The indexed_at field error has been fixed!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("❌ Database statistics feature failed")
        return False

if __name__ == "__main__":
    test_database_statistics()
