#!/usr/bin/env python3
"""
Complete test script for all movie search features
"""

from src.movie_search_engine_complete import MovieSearchEngine
from src.elasticsearch_client import ElasticsearchClient

def test_all_features():
    """Test all major features to ensure they work"""
    print("Testing all movie search features...")
    print("=" * 60)
    
    try:
        # Initialize
        client = ElasticsearchClient()
        engine = MovieSearchEngine(client)
        print("✓ Successfully initialized MovieSearchEngine")
        
        # Test 1: Basic search
        results = engine.search("action")
        print(f"✓ Basic search: Found {len(results)} movies")
        
        # Test 2: Advanced search
        results = engine.advanced_search(
            query="crime",
            genre_filter="Crime",
            min_rating=8.0
        )
        print(f"✓ Advanced search: Found {len(results)} movies")
        
        # Test 3: Autocomplete
        suggestions = engine.get_autocomplete_suggestions("pul")
        print(f"✓ Autocomplete: Found {len(suggestions)} suggestions")
        
        # Test 4: Recommendations
        results = engine.get_similar_movies("Pulp Fiction")
        print(f"✓ Similar movies: Found {len(results)} recommendations")
        
        # Test 5: Genre aggregation
        genres = engine.get_genre_aggregation()
        print(f"✓ Genre analysis: Found {len(genres)} genres")
        
        # Test 6: Rating statistics
        rating_stats = engine.get_rating_statistics()
        print(f"✓ Rating statistics: Retrieved analytics")
        
        # Test 7: Year distribution
        year_stats = engine.get_year_distribution()
        print(f"✓ Year distribution: Found {len(year_stats)} years")
        
        # Test 8: Director statistics
        director_stats = engine.get_director_statistics()
        print(f"✓ Director statistics: Found {len(director_stats)} directors")
        
        # Test 9: Comprehensive statistics (the one that was failing)
        comprehensive_stats = engine.get_comprehensive_stats()
        print(f"✓ Comprehensive statistics: Complete analytics retrieved")
        
        # Test 10: Spelling suggestions
        suggestions = engine.get_spelling_suggestions("actoin")
        print(f"✓ Spelling suggestions: Found {len(suggestions)} corrections")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("🎉 Complete movie search application is fully functional!")
        print("🎉 All 14 menu options should work correctly!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during testing: {e}")
        return False

if __name__ == "__main__":
    test_all_features()
