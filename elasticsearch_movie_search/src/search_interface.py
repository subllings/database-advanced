"""
Interactive search interface for the movie search engine.

This module provides a command-line interface for testing and
demonstrating the movie search engine capabilities.
"""

import json
from typing import Dict, Any
from .movie_search_engine import MovieSearchEngine


class MovieSearchInterface:
    """
    Interactive command-line interface for movie search.
    
    Provides an easy-to-use interface for testing all search
    functionality including basic search, filtering, aggregations,
    and similarity search.
    """
    
    def __init__(self):
        """Initialize the search interface."""
        self.search_engine = MovieSearchEngine()
        self.running = True
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "="*60)
        print("MOVIE SEARCH ENGINE")
        print("="*60)
        print("1. Basic Search")
        print("2. Advanced Search with Filters")
        print("3. Find Similar Movies")
        print("4. Autocomplete Test")
        print("5. Movie Statistics")
        print("6. Browse by Genre")
        print("7. Top Rated Movies")
        print("8. Movies by Year")
        print("9. Get Movie Details")
        print("10. Exit")
        print("="*60)
    
    def get_user_input(self, prompt: str) -> str:
        """
        Get user input with prompt.
        
        Args:
            prompt: Input prompt message
            
        Returns:
            User input string
        """
        return input(f"\n{prompt}: ").strip()
    
    def display_movies(self, results: Dict[str, Any], title: str = "Search Results") -> None:
        """
        Display movie search results in a formatted way.
        
        Args:
            results: Search results dictionary
            title: Title for the results section
        """
        if "error" in results:
            print(f"\nError: {results['error']}")
            return
        
        movies = results.get("results", [])
        total = results.get("total", 0)
        took = results.get("took", 0)
        
        print(f"\n{title}")
        print("-" * 60)
        print(f"Found {total} movies (took {took}ms)")
        print("-" * 60)
        
        if not movies:
            print("No movies found.")
            return
        
        for i, movie in enumerate(movies, 1):
            print(f"\n{i}. {movie.get('title', 'Unknown Title')}")
            print(f"   📅 Year: {movie.get('release_year', 'N/A')}")
            print(f"   ⭐ Rating: {movie.get('rating', 'N/A')}/10")
            print(f"   🎭 Genres: {', '.join(movie.get('genres', []))}")
            print(f"   Director: {movie.get('director', 'Unknown')}")
            
            # Show description (truncated)
            description = movie.get('description', 'No description available')
            if len(description) > 100:
                description = description[:100] + "..."
            print(f"   📝 {description}")
            
            # Show highlights if available
            if 'highlights' in movie:
                highlights = movie['highlights']
                if 'title' in highlights:
                    print(f"   Title match: {' '.join(highlights['title'])}")
                if 'description' in highlights:
                    print(f"   Description match: {' '.join(highlights['description'])}")
    
    def display_statistics(self, stats: Dict[str, Any]) -> None:
        """
        Display movie database statistics.
        
        Args:
            stats: Statistics dictionary from the search engine
        """
        if "error" in stats:
            print(f"\nError: {stats['error']}")
            return
        
        print("\nMOVIE DATABASE STATISTICS")
        print("-" * 60)
        print(f"Total Movies: {stats.get('total_movies', 0)}")
        print(f"⭐ Average Rating: {stats.get('avg_rating', 0)}")
        
        # Top genres
        genres = stats.get('genres', [])[:5]
        if genres:
            print(f"\n🎭 Top Genres:")
            for genre in genres:
                print(f"   - {genre['genre']}: {genre['count']} movies")
        
        # Top directors
        directors = stats.get('top_directors', [])[:5]
        if directors:
            print("\nTop Directors:")
            for director in directors:
                print(f"   - {director['director']}: {director['movies']} movies")
        
        # Box office stats
        box_office = stats.get('box_office_stats', {})
        if box_office:
            print(f"\n💰 Box Office Statistics:")
            print(f"   - Total: ${box_office.get('sum', 0):,}")
            print(f"   - Average: ${box_office.get('avg', 0):,.0f}")
            print(f"   - Highest: ${box_office.get('max', 0):,}")
    
    def basic_search(self) -> None:
        """Handle basic search functionality."""
        query = self.get_user_input("Enter search query (title, description, actors)")
        
        if not query:
            print("Please enter a search query.")
            return
        
        print(f"\nSearching for: '{query}'...")
        results = self.search_engine.search_movies(query=query, size=5)
        self.display_movies(results, f"Search Results for '{query}'")
    
    def advanced_search(self) -> None:
        """Handle advanced search with filters."""
        print("\nAdvanced Search - Enter filters (press Enter to skip):")
        
        query = self.get_user_input("Search query") or None
        genre = self.get_user_input("Genre (Action, Drama, Comedy, etc.)") or None
        
        # Year range
        min_year_str = self.get_user_input("Minimum year")
        min_year = int(min_year_str) if min_year_str.isdigit() else None
        
        max_year_str = self.get_user_input("Maximum year")
        max_year = int(max_year_str) if max_year_str.isdigit() else None
        
        # Rating range
        min_rating_str = self.get_user_input("Minimum rating (0-10)")
        min_rating = float(min_rating_str) if min_rating_str.replace('.', '').isdigit() else None
        
        # Sort options
        print("\nSort options: relevance, rating, release_year, title")
        sort_by = self.get_user_input("Sort by") or "relevance"
        sort_order = self.get_user_input("Sort order (asc/desc)") or "desc"
        
        print("\nSearching with filters...")
        results = self.search_engine.search_movies(
            query=query,
            genre=genre,
            min_year=min_year,
            max_year=max_year,
            min_rating=min_rating,
            sort_by=sort_by,
            sort_order=sort_order,
            size=5
        )
        
        self.display_movies(results, "Advanced Search Results")
    
    def find_similar_movies(self) -> None:
        """Handle similar movies search."""
        movie_id = self.get_user_input("Enter movie ID (1-15)")
        
        if not movie_id.isdigit():
            print("Please enter a valid movie ID.")
            return
        
        print(f"\nFinding movies similar to movie ID {movie_id}...")
        
        # First show the reference movie
        reference_movie = self.search_engine.get_movie_by_id(movie_id)
        if "error" not in reference_movie:
            print(f"\n📍 Reference Movie:")
            print(f"   🎬 {reference_movie.get('title', 'Unknown')}")
            print(f"   🎭 Genres: {', '.join(reference_movie.get('genres', []))}")
        
        # Find similar movies
        results = self.search_engine.find_similar_movies(movie_id, size=5)
        self.display_movies(results, "Similar Movies")
    
    def autocomplete_test(self) -> None:
        """Test autocomplete functionality."""
        query = self.get_user_input("Enter partial movie title")
        
        if not query:
            print("❌ Please enter a partial title.")
            return
        
        print(f"\n💡 Autocomplete suggestions for '{query}':")
        suggestions = self.search_engine.autocomplete_movies(query, size=10)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
        else:
            print("   No suggestions found.")
    
    def browse_by_genre(self) -> None:
        """Browse movies by genre."""
        print("\n🎭 Popular genres: Action, Adventure, Animation, Comedy, Crime, Drama, Fantasy, Sci-Fi, Thriller")
        genre = self.get_user_input("Enter genre to browse")
        
        if not genre:
            print("❌ Please enter a genre.")
            return
        
        print(f"\n🎭 Browsing {genre} movies...")
        results = self.search_engine.search_movies(genre=genre, sort_by="rating", size=10)
        self.display_movies(results, f"{genre} Movies")
    
    def top_rated_movies(self) -> None:
        """Show top rated movies."""
        print("\n🏆 Finding top rated movies...")
        results = self.search_engine.search_movies(
            min_rating=8.0,
            sort_by="rating",
            sort_order="desc",
            size=10
        )
        self.display_movies(results, "Top Rated Movies (8.0+)")
    
    def movies_by_year(self) -> None:
        """Browse movies by year."""
        year_str = self.get_user_input("Enter year (e.g., 2019)")
        
        if not year_str.isdigit():
            print("❌ Please enter a valid year.")
            return
        
        year = int(year_str)
        print(f"\n📅 Finding movies from {year}...")
        results = self.search_engine.search_movies(
            min_year=year,
            max_year=year,
            sort_by="rating",
            sort_order="desc",
            size=10
        )
        self.display_movies(results, f"Movies from {year}")
    
    def get_movie_details(self) -> None:
        """Get detailed information about a specific movie."""
        movie_id = self.get_user_input("Enter movie ID (1-15)")
        
        if not movie_id.isdigit():
            print("❌ Please enter a valid movie ID.")
            return
        
        print(f"\n🎬 Getting details for movie ID {movie_id}...")
        movie = self.search_engine.get_movie_by_id(movie_id)
        
        if "error" in movie:
            print(f"❌ {movie['error']}")
            return
        
        print(f"\n📽️ MOVIE DETAILS")
        print("-" * 60)
        print(f"🎬 Title: {movie.get('title', 'Unknown')}")
        print(f"📅 Year: {movie.get('release_year', 'N/A')}")
        print(f"⭐ Rating: {movie.get('rating', 'N/A')}/10")
        print(f"🎭 Genres: {', '.join(movie.get('genres', []))}")
        print(f"🎬 Director: {movie.get('director', 'Unknown')}")
        print(f"🎭 Actors: {', '.join(movie.get('actors', []))}")
        print(f"⏱️ Duration: {movie.get('duration_minutes', 'N/A')} minutes")
        print(f"💰 Box Office: ${movie.get('box_office', 0):,}")
        print(f"\n📝 Description:")
        print(f"   {movie.get('description', 'No description available')}")
    
    def show_statistics(self) -> None:
        """Show database statistics."""
        print("\n📊 Loading database statistics...")
        stats = self.search_engine.get_movie_statistics()
        self.display_statistics(stats)
    
    def run(self) -> None:
        """Run the interactive search interface."""
        print("🎬 Welcome to the Movie Search Engine!")
        print("This interface allows you to test all search capabilities.")
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_input("Choose an option (1-10)")
                
                if choice == "1":
                    self.basic_search()
                elif choice == "2":
                    self.advanced_search()
                elif choice == "3":
                    self.find_similar_movies()
                elif choice == "4":
                    self.autocomplete_test()
                elif choice == "5":
                    self.show_statistics()
                elif choice == "6":
                    self.browse_by_genre()
                elif choice == "7":
                    self.top_rated_movies()
                elif choice == "8":
                    self.movies_by_year()
                elif choice == "9":
                    self.get_movie_details()
                elif choice == "10":
                    print("\n👋 Thank you for using the Movie Search Engine!")
                    self.running = False
                else:
                    print("\n❌ Invalid choice. Please enter a number between 1-10.")
                
                if self.running:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """
    Main function to run the interactive search interface.
    """
    try:
        interface = MovieSearchInterface()
        interface.run()
    except Exception as e:
        print(f"❌ Failed to start search interface: {e}")
        print("Make sure Elasticsearch is running and the movie data is indexed.")


if __name__ == "__main__":
    main()
