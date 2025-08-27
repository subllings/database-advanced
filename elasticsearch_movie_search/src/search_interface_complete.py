"""
Complete Interactive Search Interface for Movie Database.

This module provides a comprehensive command-line interface for searching and exploring
the movie database with all required features including:
- Interactive movie search with filters
- Autocomplete functionality  
- "More like this" recommendations
- Genre browsing and statistics
- Advanced analytics and aggregations
"""

import os
import sys
from typing import Dict, List, Any, Optional
from src.elasticsearch_client import ElasticsearchClient
from src.movie_search_engine_complete import MovieSearchEngine
from src.data_indexer_fixed import MovieDataIndexer


class MovieSearchInterface:
    """
    Complete interactive interface for movie search engine.
    
    Provides comprehensive search functionality including:
    - Full-text search with advanced filtering
    - Autocomplete suggestions
    - Similar movie recommendations  
    - Genre-based browsing
    - Rating and year-based filtering
    - Comprehensive statistics and analytics
    """

    def __init__(self):
        """Initialize the search interface with all components."""
        self.es_client = ElasticsearchClient()
        self.search_engine = MovieSearchEngine(self.es_client)
        self.data_indexer = MovieDataIndexer(self.es_client)
        self.current_results = []
        self.last_query = ""
        
    def display_banner(self):
        """Display application banner and information."""
        print("=" * 80)
        print("MOVIE SEARCH ENGINE - Complete Database System")
        print("=" * 80)
        print("Features: Full-text search | Filters | Sorting | Autocomplete | Recommendations")
        print("Database: Elasticsearch with comprehensive movie metadata")
        print("-" * 80)

    def display_menu(self):
        """Display the main menu options."""
        print("\nMAIN MENU:")
        print("1.  Search movies (full-text with filters)")
        print("2.  Browse by genre")
        print("3.  Browse top-rated movies") 
        print("4.  Browse recent movies")
        print("5.  Search by director")
        print("6.  Autocomplete search")
        print("7.  Get movie recommendations (similar movies)")
        print("8.  Advanced search with year/rating filters")
        print("9.  Database statistics and analytics")
        print("10. Genre statistics")
        print("11. Rating analysis")
        print("12. Director analysis")
        print("13. Refresh/reindex sample data")
        print("14. Test database connection")
        print("0.  Exit")
        print("-" * 50)

    def format_movie_result(self, movie: Dict[str, Any], show_score: bool = True) -> str:
        """
        Format a movie result for display.
        
        Args:
            movie: Movie document from Elasticsearch
            show_score: Whether to show relevance score
            
        Returns:
            Formatted movie string
        """
        source = movie.get('_source', movie.get('source', movie))
        
        title = source.get('title', 'Unknown Title')
        year = source.get('year', 'Unknown')
        rating = source.get('rating', 0)
        genres = source.get('genres', [])
        director = source.get('director', 'Unknown Director')
        description = source.get('description', 'No description available')
        
        # Truncate description for display
        if len(description) > 100:
            description = description[:97] + "..."
        
        formatted = f"Title: {title} ({year})\n"
        formatted += f"Rating: {rating}/10 | Director: {director}\n"
        formatted += f"Genres: {', '.join(genres) if genres else 'None'}\n"
        formatted += f"Plot: {description}\n"
        
        if show_score and '_score' in movie:
            formatted += f"Relevance Score: {movie['_score']:.2f}\n"
            
        return formatted

    def display_search_results(self, results: Dict[str, Any], title: str = "Search Results"):
        """
        Display search results in a formatted way.
        
        Args:
            results: Search results from Elasticsearch
            title: Title for the results section
        """
        hits = results.get('hits', {}).get('hits', [])
        total = results.get('hits', {}).get('total', {}).get('value', 0)
        
        print(f"\n{title}")
        print("=" * len(title))
        
        if total == 0:
            print("No movies found.")
            return
            
        print(f"Found {total} movies total, showing {len(hits)} results:\n")
        
        for i, movie in enumerate(hits, 1):
            print(f"[{i}] {self.format_movie_result(movie)}")
            print("-" * 50)
            
        # Store results for potential follow-up actions
        self.current_results = hits

    def search_movies_interactive(self):
        """Interactive movie search with comprehensive filtering."""
        print("\nFULL-TEXT MOVIE SEARCH")
        print("=" * 30)
        
        query = input("Enter search query (title, description, director): ").strip()
        
        # Build filters interactively
        filters = {}
        
        genre_filter = input("Filter by genre (leave empty for all): ").strip()
        if genre_filter:
            filters['genres'] = [genre_filter]
            
        year_from = input("Minimum year (leave empty for all): ").strip()
        if year_from.isdigit():
            filters['year_from'] = int(year_from)
            
        year_to = input("Maximum year (leave empty for all): ").strip()
        if year_to.isdigit():
            filters['year_to'] = int(year_to)
            
        rating_from = input("Minimum rating (0-10, leave empty for all): ").strip()
        if rating_from.replace('.', '').isdigit():
            filters['rating_from'] = float(rating_from)
            
        rating_to = input("Maximum rating (0-10, leave empty for all): ").strip()
        if rating_to.replace('.', '').isdigit():
            filters['rating_to'] = float(rating_to)
            
        director_filter = input("Filter by director (leave empty for all): ").strip()
        if director_filter:
            filters['director'] = director_filter
            
        # Sorting options
        print("\nSorting options: relevance, rating, year, title, popularity")
        sort_by = input("Sort by (default: relevance): ").strip().lower()
        if sort_by not in ['relevance', 'rating', 'year', 'title', 'popularity']:
            sort_by = None
            
        sort_order = "desc"
        if sort_by:
            order_input = input("Sort order (asc/desc, default: desc): ").strip().lower()
            if order_input in ['asc', 'desc']:
                sort_order = order_input
        
        # Get number of results
        size_input = input("Number of results (default: 10): ").strip()
        size = 10
        if size_input.isdigit():
            size = min(int(size_input), 50)  # Cap at 50
        
        print("\nSearching...")
        results = self.search_engine.search_movies(
            query=query,
            filters=filters if filters else None,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        self.display_search_results(results, f"Search Results for: '{query}'")
        self.last_query = query
        
        # Show search metadata
        metadata = results.get('search_metadata', {})
        if metadata:
            print(f"\nSearch took: {metadata.get('search_time_ms', 0)}ms")
            if metadata.get('filters_applied'):
                print(f"Filters applied: {metadata['filters_applied']}")

    def browse_by_genre(self):
        """Browse movies by genre with statistics."""
        print("\nBROWSE BY GENRE")
        print("=" * 20)
        
        # First show available genres
        genre_stats = self.search_engine.get_genre_aggregation()
        if genre_stats:
            print("Available genres:")
            for genre, stats in sorted(genre_stats.items()):
                print(f"  {genre}: {stats['count']} movies (avg rating: {stats['avg_rating']})")
        
        genre = input("\nEnter genre to browse: ").strip()
        if not genre:
            return
            
        size_input = input("Number of results (default: 20): ").strip()
        size = 20
        if size_input.isdigit():
            size = min(int(size_input), 50)
            
        sort_options = input("Sort by (rating/year/title, default: rating): ").strip().lower()
        if sort_options not in ['rating', 'year', 'title']:
            sort_options = 'rating'
        
        results = self.search_engine.get_movies_by_genre(genre, size, sort_options)
        self.display_search_results(results, f"Movies in genre: {genre.title()}")

    def browse_top_rated(self):
        """Browse top-rated movies."""
        print("\nTOP-RATED MOVIES")
        print("=" * 20)
        
        min_rating_input = input("Minimum rating (default: 8.0): ").strip()
        min_rating = 8.0
        if min_rating_input.replace('.', '').isdigit():
            min_rating = float(min_rating_input)
            
        size_input = input("Number of results (default: 20): ").strip()
        size = 20
        if size_input.isdigit():
            size = min(int(size_input), 50)
        
        results = self.search_engine.get_top_rated_movies(min_rating, size)
        self.display_search_results(results, f"Top-Rated Movies (Rating >= {min_rating})")

    def browse_recent_movies(self):
        """Browse recent movies."""
        print("\nRECENT MOVIES")
        print("=" * 15)
        
        year_input = input("Starting year (default: 2020): ").strip()
        year_from = 2020
        if year_input.isdigit():
            year_from = int(year_input)
            
        size_input = input("Number of results (default: 20): ").strip()
        size = 20
        if size_input.isdigit():
            size = min(int(size_input), 50)
        
        results = self.search_engine.get_recent_movies(year_from, size)
        self.display_search_results(results, f"Recent Movies (From {year_from})")

    def search_by_director(self):
        """Search movies by director."""
        print("\nSEARCH BY DIRECTOR")
        print("=" * 20)
        
        director = input("Enter director name: ").strip()
        if not director:
            return
            
        size_input = input("Number of results (default: 20): ").strip()
        size = 20
        if size_input.isdigit():
            size = min(int(size_input), 50)
        
        results = self.search_engine.get_movies_by_director(director, size)
        self.display_search_results(results, f"Movies by: {director}")

    def autocomplete_search(self):
        """Interactive autocomplete search."""
        print("\nAUTOCOMPLETE SEARCH")
        print("=" * 20)
        print("Type partial movie titles to get suggestions...")
        
        while True:
            partial_title = input("\nEnter partial title (or 'back' to return): ").strip()
            if partial_title.lower() == 'back' or not partial_title:
                break
                
            suggestions = self.search_engine.get_movie_autocomplete(partial_title, 10)
            
            if suggestions:
                print(f"\nSuggestions for '{partial_title}':")
                for i, suggestion in enumerate(suggestions, 1):
                    title = suggestion['title']
                    year = suggestion.get('year', 'Unknown')
                    rating = suggestion.get('rating', 0)
                    genres = ', '.join(suggestion.get('genres', [])[:3])  # Show first 3 genres
                    print(f"  [{i}] {title} ({year}) - Rating: {rating}/10")
                    if genres:
                        print(f"      Genres: {genres}")
                        
                # Option to select a movie for details
                choice = input("\nSelect movie number for full details (or press Enter to continue): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
                    selected = suggestions[int(choice) - 1]
                    movie_details = self.search_engine.get_movie_by_id(selected['id'])
                    if movie_details:
                        print(f"\nFull details for: {selected['title']}")
                        print("-" * 40)
                        print(self.format_movie_result(movie_details, False))
            else:
                print(f"No suggestions found for '{partial_title}'")

    def get_similar_movies(self):
        """Get similar movie recommendations."""
        print("\nSIMILAR MOVIE RECOMMENDATIONS")
        print("=" * 35)
        
        if not self.current_results:
            print("No previous search results available.")
            print("Please perform a search first to get movie recommendations.")
            return
            
        print("Select a movie from your last search results:")
        for i, movie in enumerate(self.current_results, 1):
            title = movie['_source'].get('title', 'Unknown')
            year = movie['_source'].get('year', 'Unknown')
            print(f"  [{i}] {title} ({year})")
            
        choice = input(f"\nSelect movie number (1-{len(self.current_results)}): ").strip()
        
        if not choice.isdigit() or not (1 <= int(choice) <= len(self.current_results)):
            print("Invalid selection.")
            return
            
        selected_movie = self.current_results[int(choice) - 1]
        movie_id = selected_movie['_id']
        movie_title = selected_movie['_source'].get('title', 'Unknown')
        
        print(f"\nFinding movies similar to: {movie_title}")
        
        similar_results = self.search_engine.get_similar_movies(movie_id, 5)
        
        if similar_results.get('hits', {}).get('hits'):
            print(f"\nMovies similar to '{movie_title}':")
            print("=" * (20 + len(movie_title)))
            
            for i, movie in enumerate(similar_results['hits']['hits'], 1):
                print(f"[{i}] {self.format_movie_result(movie)}")
                print("-" * 50)
        else:
            print(f"No similar movies found for '{movie_title}'.")

    def advanced_search(self):
        """Advanced search with comprehensive filters."""
        print("\nADVANCED SEARCH")
        print("=" * 17)
        
        query = input("Search query (optional): ").strip()
        
        print("\nYear range:")
        year_from = input("  From year: ").strip()
        year_to = input("  To year: ").strip()
        
        print("\nRating range:")
        rating_from = input("  Minimum rating (0-10): ").strip()
        rating_to = input("  Maximum rating (0-10): ").strip()
        
        print("\nOther filters:")
        genres = input("  Genres (comma-separated): ").strip()
        director = input("  Director: ").strip()
        
        # Build filters
        filters = {}
        if year_from.isdigit():
            filters['year_from'] = int(year_from)
        if year_to.isdigit():
            filters['year_to'] = int(year_to)
        if rating_from.replace('.', '').isdigit():
            filters['rating_from'] = float(rating_from)
        if rating_to.replace('.', '').isdigit():
            filters['rating_to'] = float(rating_to)
        if genres:
            filters['genres'] = [g.strip() for g in genres.split(',')]
        if director:
            filters['director'] = director
            
        size_input = input("\nNumber of results (default: 15): ").strip()
        size = 15
        if size_input.isdigit():
            size = min(int(size_input), 50)
        
        results = self.search_engine.search_movies(
            query=query,
            filters=filters if filters else None,
            size=size
        )
        
        self.display_search_results(results, "Advanced Search Results")

    def show_database_statistics(self):
        """Display comprehensive database statistics."""
        print("\nDATABASE STATISTICS & ANALYTICS")
        print("=" * 35)
        
        print("Retrieving comprehensive statistics...")
        stats = self.search_engine.get_comprehensive_stats()
        
        if not stats:
            print("Unable to retrieve statistics.")
            return
            
        # Overview
        overview = stats.get('overview', {})
        if overview:
            print(f"\nOVERVIEW:")
            print(f"  Total Movies: {overview.get('total_movies', 0)}")
            
        # Rating Statistics
        rating_stats = stats.get('ratings', {})
        if rating_stats:
            basic_stats = rating_stats.get('basic_stats', {})
            print(f"\nRATING STATISTICS:")
            print(f"  Total Rated Movies: {basic_stats.get('count', 0)}")
            print(f"  Average Rating: {basic_stats.get('avg', 0)}/10")
            print(f"  Highest Rating: {basic_stats.get('max', 0)}/10")
            print(f"  Lowest Rating: {basic_stats.get('min', 0)}/10")
            
        # Top Genres
        genres = stats.get('genres', {})
        if genres:
            print(f"\nTOP GENRES:")
            sorted_genres = sorted(genres.items(), key=lambda x: x[1]['count'], reverse=True)
            for genre, genre_stats in sorted_genres[:10]:
                print(f"  {genre}: {genre_stats['count']} movies (avg: {genre_stats['avg_rating']}/10)")
                
        # Year Distribution
        years = stats.get('years', {}).get('year_distribution', [])
        if years:
            print(f"\nYEAR DISTRIBUTION (Recent):")
            recent_years = sorted(years, key=lambda x: x['year'], reverse=True)[:10]
            for year_data in recent_years:
                print(f"  {year_data['year']}: {year_data['movie_count']} movies (avg: {year_data['avg_rating']}/10)")

    def show_genre_statistics(self):
        """Display detailed genre statistics."""
        print("\nGENRE ANALYSIS")
        print("=" * 15)
        
        genre_stats = self.search_engine.get_genre_aggregation()
        
        if not genre_stats:
            print("No genre statistics available.")
            return
            
        print(f"Found {len(genre_stats)} genres:\n")
        
        sorted_genres = sorted(genre_stats.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for genre, stats in sorted_genres:
            print(f"Genre: {genre}")
            print(f"  Movies: {stats['count']}")
            print(f"  Average Rating: {stats['avg_rating']}/10")
            print(f"  Average Year: {stats['avg_year']}")
            print("-" * 30)

    def show_rating_analysis(self):
        """Display detailed rating analysis."""
        print("\nRATING ANALYSIS")
        print("=" * 17)
        
        rating_stats = self.search_engine.get_rating_statistics()
        
        if not rating_stats:
            print("No rating statistics available.")
            return
            
        basic_stats = rating_stats.get('basic_stats', {})
        print("BASIC STATISTICS:")
        print(f"  Total Movies: {basic_stats.get('count', 0)}")
        print(f"  Average Rating: {basic_stats.get('avg', 0)}/10")
        print(f"  Median Rating: {basic_stats.get('avg', 0)}/10")  # Approximate
        print(f"  Highest Rating: {basic_stats.get('max', 0)}/10")
        print(f"  Lowest Rating: {basic_stats.get('min', 0)}/10")
        
        histogram = rating_stats.get('histogram', [])
        if histogram:
            print("\nRATING DISTRIBUTION:")
            for bucket in histogram:
                rating = bucket['rating']
                count = bucket['count']
                bar = "█" * min(count, 50)  # Visual bar
                print(f"  {rating:3.0f}: {count:3d} movies {bar}")

    def show_director_analysis(self):
        """Display director analysis and statistics."""
        print("\nDIRECTOR ANALYSIS")
        print("=" * 18)
        
        min_movies_input = input("Minimum movies per director (default: 2): ").strip()
        min_movies = 2
        if min_movies_input.isdigit():
            min_movies = int(min_movies_input)
            
        director_stats = self.search_engine.get_director_statistics(min_movies)
        
        if not director_stats:
            print(f"No directors found with {min_movies}+ movies.")
            return
            
        print(f"\nDirectors with {min_movies}+ movies:\n")
        
        sorted_directors = sorted(director_stats.items(), key=lambda x: x[1]['avg_rating'], reverse=True)
        
        for director, stats in sorted_directors[:20]:  # Top 20
            print(f"Director: {director}")
            print(f"  Movies: {stats['movie_count']}")
            print(f"  Average Rating: {stats['avg_rating']}/10")
            print(f"  Total Box Office: ${stats['total_box_office']:,.0f}")
            
            top_movies = stats.get('top_movies', [])
            if top_movies:
                print("  Top Movies:")
                for movie in top_movies[:3]:  # Top 3
                    print(f"    - {movie['title']} ({movie['year']}) - {movie['rating']}/10")
            print("-" * 40)

    def refresh_data(self):
        """Refresh/reindex sample movie data."""
        print("\nREFRESHING SAMPLE DATA")
        print("=" * 25)
        
        confirm = input("This will reindex all sample movie data. Continue? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return
            
        print("Refreshing movie index...")
        success = self.data_indexer.create_index()
        
        if success:
            print("Creating sample movie data...")
            indexed_count = self.data_indexer.index_sample_movies()
            print(f"Successfully indexed {indexed_count} movies.")
        else:
            print("Failed to refresh data.")

    def test_connection(self):
        """Test database connection and display info."""
        print("\nTESTING DATABASE CONNECTION")
        print("=" * 30)
        
        if self.es_client.test_connection():
            print("Successfully connected to Elasticsearch")
            
            # Get cluster info
            info = self.es_client.get_cluster_info()
            if info:
                print(f"  Cluster Name: {info.get('cluster_name', 'Unknown')}")
                print(f"  Version: {info.get('version', {}).get('number', 'Unknown')}")
                
            # Check index
            if self.es_client.index_exists():
                print(f"Index '{self.es_client.index_name}' exists")
                
                # Get document count
                try:
                    count_response = self.es_client.client.count(index=self.es_client.index_name)
                    doc_count = count_response.get('count', 0)
                    print(f"  Document Count: {doc_count} movies")
                except Exception as e:
                    print(f"  Could not get document count: {e}")
            else:
                print(f"Index '{self.es_client.index_name}' does not exist")
                print("  Run option 13 to create and populate the index")
                
        else:
            print("Failed to connect to Elasticsearch")
            print("  Make sure Elasticsearch is running on localhost:9200")

    def run(self):
        """Main application loop."""
        self.display_banner()
        
        # Test connection on startup
        if not self.es_client.test_connection():
            print("WARNING: Cannot connect to Elasticsearch!")
            print("Make sure Elasticsearch is running before using the search features.")
            print()
        
        while True:
            try:
                self.display_menu()
                choice = input("Select option (0-14): ").strip()
                
                if choice == '0':
                    print("\nThank you for using Movie Search Engine!")
                    break
                elif choice == '1':
                    self.search_movies_interactive()
                elif choice == '2':
                    self.browse_by_genre()
                elif choice == '3':
                    self.browse_top_rated()
                elif choice == '4':
                    self.browse_recent_movies()
                elif choice == '5':
                    self.search_by_director()
                elif choice == '6':
                    self.autocomplete_search()
                elif choice == '7':
                    self.get_similar_movies()
                elif choice == '8':
                    self.advanced_search()
                elif choice == '9':
                    self.show_database_statistics()
                elif choice == '10':
                    self.show_genre_statistics()
                elif choice == '11':
                    self.show_rating_analysis()
                elif choice == '12':
                    self.show_director_analysis()
                elif choice == '13':
                    self.refresh_data()
                elif choice == '14':
                    self.test_connection()
                else:
                    print("Invalid option. Please select 0-14.")
                    
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting Movie Search Engine...")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                print("Please try again.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    interface = MovieSearchInterface()
    interface.run()
