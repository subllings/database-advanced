"""
Simple search interface for movie search engine
"""

import sys
from typing import Dict, Any, List, Optional
from src.movie_search_engine_simple import MovieSearchEngine


class MovieSearchInterface:
    """Simple interactive search interface."""

    def __init__(self, search_engine: Optional[MovieSearchEngine] = None):
        """Initialize the search interface."""
        self.search_engine = search_engine or MovieSearchEngine()

    def start_interactive_search(self):
        """Start the interactive search session."""
        print("Interactive Movie Search")
        print("Type 'help' for commands, 'quit' to exit")
        print()
        
        while True:
            try:
                user_input = input("Search> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                    
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                    
                # Handle special commands
                if user_input.startswith('/'):
                    self.handle_command(user_input)
                else:
                    # Regular search
                    self.perform_search(user_input)
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def show_help(self):
        """Show help information."""
        print("\nAvailable commands:")
        print("  <search term>     - Search for movies")
        print("  /genres           - Show all genres")
        print("  /top              - Show top rated movies")
        print("  /stats            - Show database statistics")
        print("  help              - Show this help")
        print("  quit, exit, q     - Exit the program")
        print()

    def handle_command(self, command: str):
        """Handle special commands."""
        cmd = command.lower().strip()
        
        if cmd == '/genres':
            self.show_genres()
        elif cmd == '/top':
            self.show_top_movies()
        elif cmd == '/stats':
            self.show_statistics()
        else:
            print(f"Unknown command: {command}")

    def perform_search(self, query: str):
        """Perform a movie search and display results."""
        print(f"\nSearching for: '{query}'")
        print("-" * 50)
        
        try:
            results = self.search_engine.search_movies(query, size=5)
            self.display_search_results(results)
            
        except Exception as e:
            print(f"Search failed: {e}")

    def display_search_results(self, results: Dict[str, Any]):
        """Display search results."""
        if not results or 'hits' not in results:
            print("No results found")
            return
            
        hits = results['hits']['hits']
        total = results['hits']['total']['value']
        
        if not hits:
            print("No movies found")
            return
            
        print(f"Found {total} movies (showing top {len(hits)}):")
        print()
        
        for i, hit in enumerate(hits, 1):
            movie = hit['_source']
            score = hit['_score']
            
            print(f"{i}. {movie.get('title', 'Unknown')} ({movie.get('year', 'N/A')})")
            print(f"   Score: {score:.2f}")
            print(f"   Director: {movie.get('director', 'Unknown')}")
            print(f"   Rating: {movie.get('rating', 'N/A')}")
            print(f"   Genres: {', '.join(movie.get('genres', []))}")
            print()

    def show_genres(self):
        """Show available genres."""
        print("\nAvailable genres:")
        print("-" * 30)
        
        try:
            genre_counts = self.search_engine.get_genre_aggregation()
            
            if genre_counts:
                sorted_genres = sorted(genre_counts.items(), 
                                     key=lambda x: x[1], reverse=True)
                
                for genre, count in sorted_genres:
                    print(f"  {genre}: {count} movies")
            else:
                print("No genre information available")
                
        except Exception as e:
            print(f"Error getting genres: {e}")
        
        print()

    def show_top_movies(self):
        """Show top rated movies."""
        print("\nTop Rated Movies:")
        print("-" * 30)
        
        try:
            results = self.search_engine.get_top_rated_movies(min_rating=8.0, size=5)
            self.display_search_results(results)
            
        except Exception as e:
            print(f"Error getting top movies: {e}")

    def show_statistics(self):
        """Show database statistics."""
        print("\nDatabase Statistics:")
        print("-" * 30)
        
        try:
            rating_stats = self.search_engine.get_rating_statistics()
            if rating_stats:
                print(f"Total movies: {rating_stats.get('count', 0)}")
                print(f"Average rating: {rating_stats.get('avg', 0):.2f}")
                print(f"Highest rating: {rating_stats.get('max', 0):.2f}")
                print(f"Lowest rating: {rating_stats.get('min', 0):.2f}")
            
            genre_counts = self.search_engine.get_genre_aggregation()
            if genre_counts:
                print(f"Total genres: {len(genre_counts)}")
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
        
        print()
