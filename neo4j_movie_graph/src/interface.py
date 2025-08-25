"""
Interactive Interface Module

This module provides an interactive command-line interface for the Neo4j movie graph database.
"""

import logging
import os
from neo4j_client import Neo4jClient
from data_loader import DataLoader
from movie_manager import MovieManager
from person_manager import PersonManager
from graph_analytics import GraphAnalytics


class MovieGraphInterface:
    """Interactive command-line interface for the movie graph database."""
    
    def __init__(self):
        """Initialize the interface."""
        self.client = None
        self.data_loader = None
        self.movie_manager = None
        self.person_manager = None
        self.graph_analytics = None
        self.logger = logging.getLogger(__name__)
        
    def connect_to_database(self):
        """Connect to Neo4j database."""
        print("\n" + "="*60)
        print("  NEO4J MOVIE GRAPH DATABASE")
        print("="*60)
        
        # Get connection details
        uri = input("Enter Neo4j URI (default: bolt://localhost:7687): ").strip() or "bolt://localhost:7687"
        username = input("Enter username (default: neo4j): ").strip() or "neo4j"
        password = input("Enter password (default: password123): ").strip() or "password123"
        
        print("\nConnecting to Neo4j...")
        
        # Initialize client
        self.client = Neo4jClient(uri, username, password)
        
        if self.client.connect():
            print("✓ Successfully connected to Neo4j!")
            
            # Initialize managers
            self.data_loader = DataLoader(self.client)
            self.movie_manager = MovieManager(self.client)
            self.person_manager = PersonManager(self.client)
            self.graph_analytics = GraphAnalytics(self.client)
            
            # Create indexes and constraints
            print("Setting up database indexes and constraints...")
            self.client.create_indexes()
            self.client.create_constraints()
            
            return True
        else:
            print("✗ Failed to connect to Neo4j. Please check your connection details.")
            return False
    
    def display_main_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("  MAIN MENU")
        print("="*60)
        print("1.  Database Management")
        print("2.  Movie Operations")
        print("3.  Person Operations")
        print("4.  Graph Analytics")
        print("5.  Search Operations")
        print("6.  Data Import/Export")
        print("7.  Database Information")
        print("0.  Exit")
        print("="*60)
    
    def display_database_menu(self):
        """Display database management menu."""
        print("\n" + "-"*40)
        print("  DATABASE MANAGEMENT")
        print("-"*40)
        print("1. Load sample data")
        print("2. Clear all data")
        print("3. Show database statistics")
        print("0. Back to main menu")
        print("-"*40)
    
    def display_movie_menu(self):
        """Display movie operations menu."""
        print("\n" + "-"*40)
        print("  MOVIE OPERATIONS")
        print("-"*40)
        print("1. Add new movie")
        print("2. Search movies")
        print("3. Get movie details")
        print("4. Movies by year")
        print("5. Movies by rating range")
        print("6. Movies by genre")
        print("7. Top rated movies")
        print("8. Similar movies")
        print("0. Back to main menu")
        print("-"*40)
    
    def display_person_menu(self):
        """Display person operations menu."""
        print("\n" + "-"*40)
        print("  PERSON OPERATIONS")
        print("-"*40)
        print("1. Add new person")
        print("2. Search people")
        print("3. Get person details")
        print("4. Person's movies as actor")
        print("5. Person's movies as director")
        print("6. Most prolific actors")
        print("7. Most prolific directors")
        print("8. People by nationality")
        print("0. Back to main menu")
        print("-"*40)
    
    def display_analytics_menu(self):
        """Display graph analytics menu."""
        print("\n" + "-"*40)
        print("  GRAPH ANALYTICS")
        print("-"*40)
        print("1. Graph statistics")
        print("2. Shortest path between people")
        print("3. Collaboration network")
        print("4. Most connected people")
        print("5. Genre analysis")
        print("6. Movie recommendations")
        print("7. Actor similarity")
        print("8. Temporal analysis")
        print("9. Influential movies")
        print("0. Back to main menu")
        print("-"*40)
    
    def handle_database_management(self):
        """Handle database management operations."""
        while True:
            self.display_database_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                print("\nLoading sample data...")
                if self.data_loader.load_sample_data():
                    print("✓ Sample data loaded successfully!")
                else:
                    print("✗ Failed to load sample data.")
            
            elif choice == "2":
                confirm = input("\nAre you sure you want to clear all data? (y/N): ").strip().lower()
                if confirm == 'y':
                    if self.client.clear_database():
                        print("✓ Database cleared successfully!")
                    else:
                        print("✗ Failed to clear database.")
            
            elif choice == "3":
                db_info = self.client.get_database_info()
                self.display_database_info(db_info)
            
            elif choice == "0":
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def handle_movie_operations(self):
        """Handle movie operations."""
        while True:
            self.display_movie_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.add_movie_interactive()
            
            elif choice == "2":
                search_term = input("Enter search term: ").strip()
                if search_term:
                    movies = self.movie_manager.search_movies(search_term)
                    self.display_movies_list(movies, f"Search results for '{search_term}'")
            
            elif choice == "3":
                title = input("Enter movie title: ").strip()
                if title:
                    self.display_movie_details(title)
            
            elif choice == "4":
                try:
                    year = int(input("Enter year: ").strip())
                    movies = self.movie_manager.get_movies_by_year(year)
                    self.display_movies_list(movies, f"Movies from {year}")
                except ValueError:
                    print("Invalid year format.")
            
            elif choice == "5":
                try:
                    min_rating = float(input("Enter minimum rating: ").strip())
                    max_rating_input = input("Enter maximum rating (press Enter for 10.0): ").strip()
                    max_rating = float(max_rating_input) if max_rating_input else 10.0
                    movies = self.movie_manager.get_movies_by_rating_range(min_rating, max_rating)
                    self.display_movies_list(movies, f"Movies rated {min_rating}-{max_rating}")
                except ValueError:
                    print("Invalid rating format.")
            
            elif choice == "6":
                genre = input("Enter genre: ").strip()
                if genre:
                    movies = self.movie_manager.get_movies_by_genre(genre)
                    self.display_movies_list(movies, f"Movies in '{genre}' genre")
            
            elif choice == "7":
                try:
                    limit = int(input("Enter number of movies (default 10): ").strip() or "10")
                    movies = self.movie_manager.get_top_rated_movies(limit)
                    self.display_movies_list(movies, f"Top {limit} rated movies")
                except ValueError:
                    print("Invalid number format.")
            
            elif choice == "8":
                title = input("Enter movie title: ").strip()
                if title:
                    similar = self.movie_manager.get_similar_movies(title)
                    self.display_movies_list(similar, f"Movies similar to '{title}'")
            
            elif choice == "0":
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def handle_person_operations(self):
        """Handle person operations."""
        while True:
            self.display_person_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.add_person_interactive()
            
            elif choice == "2":
                search_term = input("Enter search term: ").strip()
                if search_term:
                    people = self.person_manager.search_people(search_term)
                    self.display_people_list(people, f"Search results for '{search_term}'")
            
            elif choice == "3":
                name = input("Enter person name: ").strip()
                if name:
                    self.display_person_details(name)
            
            elif choice == "4":
                name = input("Enter actor name: ").strip()
                if name:
                    movies = self.person_manager.get_person_movies_as_actor(name)
                    self.display_actor_movies(movies, name)
            
            elif choice == "5":
                name = input("Enter director name: ").strip()
                if name:
                    movies = self.person_manager.get_person_movies_as_director(name)
                    self.display_director_movies(movies, name)
            
            elif choice == "6":
                try:
                    limit = int(input("Enter number of actors (default 10): ").strip() or "10")
                    actors = self.person_manager.get_most_prolific_actors(limit)
                    self.display_prolific_people(actors, f"Top {limit} most prolific actors")
                except ValueError:
                    print("Invalid number format.")
            
            elif choice == "7":
                try:
                    limit = int(input("Enter number of directors (default 10): ").strip() or "10")
                    directors = self.person_manager.get_most_prolific_directors(limit)
                    self.display_prolific_people(directors, f"Top {limit} most prolific directors")
                except ValueError:
                    print("Invalid number format.")
            
            elif choice == "8":
                nationality = input("Enter nationality: ").strip()
                if nationality:
                    print(f"\nActors from {nationality}:")
                    actors = self.person_manager.get_actors_by_nationality(nationality)
                    self.display_prolific_people(actors, f"Actors from {nationality}")
                    
                    print(f"\nDirectors from {nationality}:")
                    directors = self.person_manager.get_directors_by_nationality(nationality)
                    self.display_prolific_people(directors, f"Directors from {nationality}")
            
            elif choice == "0":
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def handle_graph_analytics(self):
        """Handle graph analytics operations."""
        while True:
            self.display_analytics_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                stats = self.graph_analytics.get_graph_statistics()
                self.display_graph_statistics(stats)
            
            elif choice == "2":
                person1 = input("Enter first person name: ").strip()
                person2 = input("Enter second person name: ").strip()
                if person1 and person2:
                    path_info = self.graph_analytics.get_shortest_path(person1, person2)
                    self.display_shortest_path(path_info, person1, person2)
            
            elif choice == "3":
                name = input("Enter person name: ").strip()
                if name:
                    try:
                        depth = int(input("Enter network depth (default 2): ").strip() or "2")
                        network = self.graph_analytics.get_collaboration_network(name, depth)
                        self.display_collaboration_network(network)
                    except ValueError:
                        print("Invalid depth format.")
            
            elif choice == "4":
                try:
                    limit = int(input("Enter number of people (default 10): ").strip() or "10")
                    connected = self.graph_analytics.get_most_connected_people(limit)
                    self.display_connected_people(connected)
                except ValueError:
                    print("Invalid number format.")
            
            elif choice == "5":
                analysis = self.graph_analytics.get_genre_analysis()
                self.display_genre_analysis(analysis)
            
            elif choice == "6":
                name = input("Enter person name: ").strip()
                if name:
                    recommendations = self.graph_analytics.get_movie_recommendations(name)
                    self.display_recommendations(recommendations, name)
            
            elif choice == "7":
                name = input("Enter actor name: ").strip()
                if name:
                    similar = self.graph_analytics.get_actor_similarity(name)
                    self.display_actor_similarity(similar, name)
            
            elif choice == "8":
                analysis = self.graph_analytics.get_temporal_analysis()
                self.display_temporal_analysis(analysis)
            
            elif choice == "9":
                try:
                    limit = int(input("Enter number of movies (default 10): ").strip() or "10")
                    influential = self.graph_analytics.get_influential_movies(limit)
                    self.display_influential_movies(influential)
                except ValueError:
                    print("Invalid number format.")
            
            elif choice == "0":
                break
            
            else:
                print("Invalid choice. Please try again.")
    
    def add_movie_interactive(self):
        """Interactive movie addition."""
        print("\n--- Add New Movie ---")
        title = input("Title: ").strip()
        if not title:
            print("Title is required.")
            return
        
        try:
            year = int(input("Year: ").strip())
            rating_input = input("Rating (optional): ").strip()
            rating = float(rating_input) if rating_input else None
            duration_input = input("Duration in minutes (optional): ").strip()
            duration = int(duration_input) if duration_input else None
            plot = input("Plot (optional): ").strip() or None
            poster_url = input("Poster URL (optional): ").strip() or None
            
            if self.movie_manager.add_movie(title, year, rating, duration, plot, poster_url):
                print(f"✓ Movie '{title}' added successfully!")
            else:
                print("✗ Failed to add movie.")
                
        except ValueError:
            print("Invalid input format.")
    
    def add_person_interactive(self):
        """Interactive person addition."""
        print("\n--- Add New Person ---")
        name = input("Name: ").strip()
        if not name:
            print("Name is required.")
            return
        
        try:
            birth_year_input = input("Birth year (optional): ").strip()
            birth_year = int(birth_year_input) if birth_year_input else None
            nationality = input("Nationality (optional): ").strip() or None
            biography = input("Biography (optional): ").strip() or None
            
            if self.person_manager.add_person(name, birth_year, nationality, biography):
                print(f"✓ Person '{name}' added successfully!")
            else:
                print("✗ Failed to add person.")
                
        except ValueError:
            print("Invalid input format.")
    
    def display_database_info(self, db_info):
        """Display database information."""
        print("\n" + "="*50)
        print("  DATABASE INFORMATION")
        print("="*50)
        
        if db_info.get("connected"):
            print(f"URI: {db_info['uri']}")
            print(f"Total Nodes: {db_info['total_nodes']}")
            print(f"Total Relationships: {db_info['total_relationships']}")
            
            print("\nNode Counts:")
            for label, count in db_info.get("node_counts", {}).items():
                print(f"  {label}: {count}")
            
            print("\nRelationship Counts:")
            for rel_type, count in db_info.get("relationship_counts", {}).items():
                print(f"  {rel_type}: {count}")
        else:
            print(f"Connection Error: {db_info.get('message', 'Unknown error')}")
    
    def display_movies_list(self, movies, title):
        """Display a list of movies."""
        print(f"\n{title}")
        print("-" * len(title))
        
        if not movies:
            print("No movies found.")
            return
        
        for i, movie in enumerate(movies, 1):
            rating = f" ({movie['rating']}/10)" if movie.get('rating') else ""
            duration = f" - {movie['duration']}min" if movie.get('duration') else ""
            print(f"{i:2d}. {movie['title']} ({movie['year']}){rating}{duration}")
    
    def display_movie_details(self, title):
        """Display detailed movie information."""
        movie = self.movie_manager.get_movie_by_title(title)
        if not movie:
            print(f"Movie '{title}' not found.")
            return
        
        print(f"\n=== {movie['title']} ===")
        print(f"Year: {movie['year']}")
        if movie.get('rating'):
            print(f"Rating: {movie['rating']}/10")
        if movie.get('duration'):
            print(f"Duration: {movie['duration']} minutes")
        if movie.get('plot'):
            print(f"Plot: {movie['plot']}")
        
        # Get cast
        cast = self.movie_manager.get_movie_cast(title)
        if cast:
            print("\nCast:")
            for actor in cast:
                character = f" as {actor['character']}" if actor.get('character') else ""
                print(f"  • {actor['actor']}{character}")
        
        # Get directors
        directors = self.movie_manager.get_movie_directors(title)
        if directors:
            print("\nDirectors:")
            for director in directors:
                print(f"  • {director['director']}")
        
        # Get genres
        genres = self.movie_manager.get_movie_genres(title)
        if genres:
            genre_list = [g['genre'] for g in genres]
            print(f"\nGenres: {', '.join(genre_list)}")
    
    def display_people_list(self, people, title):
        """Display a list of people."""
        print(f"\n{title}")
        print("-" * len(title))
        
        if not people:
            print("No people found.")
            return
        
        for i, person in enumerate(people, 1):
            birth_year = f" ({person['birth_year']})" if person.get('birth_year') else ""
            nationality = f" - {person['nationality']}" if person.get('nationality') else ""
            print(f"{i:2d}. {person['name']}{birth_year}{nationality}")
    
    def display_person_details(self, name):
        """Display detailed person information."""
        person = self.person_manager.get_person_by_name(name)
        if not person:
            print(f"Person '{name}' not found.")
            return
        
        print(f"\n=== {person['name']} ===")
        if person.get('birth_year'):
            print(f"Birth Year: {person['birth_year']}")
        if person.get('nationality'):
            print(f"Nationality: {person['nationality']}")
        if person.get('biography'):
            print(f"Biography: {person['biography']}")
        
        # Get movies as actor
        actor_movies = self.person_manager.get_person_movies_as_actor(name)
        if actor_movies:
            print("\nMovies as Actor:")
            for movie in actor_movies:
                character = f" as {movie['character']}" if movie.get('character') else ""
                rating = f" ({movie['rating']}/10)" if movie.get('rating') else ""
                print(f"  • {movie['title']} ({movie['year']}){character}{rating}")
        
        # Get movies as director
        director_movies = self.person_manager.get_person_movies_as_director(name)
        if director_movies:
            print("\nMovies as Director:")
            for movie in director_movies:
                rating = f" ({movie['rating']}/10)" if movie.get('rating') else ""
                print(f"  • {movie['title']} ({movie['year']}){rating}")
        
        # Get collaborators
        collaborators = self.person_manager.get_person_collaborators(name, 5)
        if collaborators:
            print("\nFrequent Collaborators:")
            for collab in collaborators:
                print(f"  • {collab['collaborator']} ({collab['collaborations']} collaborations)")
    
    def display_actor_movies(self, movies, actor_name):
        """Display movies for an actor."""
        print(f"\n{actor_name} - Movies as Actor")
        print("-" * (len(actor_name) + 20))
        
        if not movies:
            print("No movies found.")
            return
        
        for movie in movies:
            character = f" as {movie['character']}" if movie.get('character') else ""
            rating = f" ({movie['rating']}/10)" if movie.get('rating') else ""
            print(f"  • {movie['title']} ({movie['year']}){character}{rating}")
    
    def display_director_movies(self, movies, director_name):
        """Display movies for a director."""
        print(f"\n{director_name} - Movies as Director")
        print("-" * (len(director_name) + 22))
        
        if not movies:
            print("No movies found.")
            return
        
        for movie in movies:
            rating = f" ({movie['rating']}/10)" if movie.get('rating') else ""
            print(f"  • {movie['title']} ({movie['year']}){rating}")
    
    def display_prolific_people(self, people, title):
        """Display prolific people list."""
        print(f"\n{title}")
        print("-" * len(title))
        
        if not people:
            print("No people found.")
            return
        
        for i, person in enumerate(people, 1):
            birth_year = f" ({person['birth_year']})" if person.get('birth_year') else ""
            nationality = f" - {person['nationality']}" if person.get('nationality') else ""
            movie_count = person.get('movie_count', 0)
            print(f"{i:2d}. {person['name']}{birth_year}{nationality} - {movie_count} movies")
    
    def display_graph_statistics(self, stats):
        """Display graph statistics."""
        print("\n" + "="*50)
        print("  GRAPH STATISTICS")
        print("="*50)
        
        print(f"Total Nodes: {stats.get('total_nodes', 0)}")
        print(f"Total Relationships: {stats.get('total_relationships', 0)}")
        
        if 'node_counts' in stats:
            print("\nNode Counts:")
            for label, count in stats['node_counts'].items():
                print(f"  {label}: {count}")
        
        if 'relationship_counts' in stats:
            print("\nRelationship Counts:")
            for rel_type, count in stats['relationship_counts'].items():
                print(f"  {rel_type}: {count}")
        
        if 'movie_person_density' in stats:
            print(f"\nGraph Density (Movies-People): {stats['movie_person_density']:.4f}")
    
    def display_shortest_path(self, path_info, person1, person2):
        """Display shortest path information."""
        print(f"\nShortest Path: {person1} → {person2}")
        print("-" * 40)
        
        if path_info.get('path_exists'):
            degrees = path_info.get('degrees_of_separation', 0)
            print(f"Path exists: Yes")
            print(f"Degrees of separation: {degrees}")
            print(f"Path length: {path_info.get('path_length', 0)} steps")
        else:
            print("No path exists between these people.")
    
    def display_collaboration_network(self, network):
        """Display collaboration network."""
        if not network:
            print("No network data available.")
            return
        
        center = network.get('center_person', 'Unknown')
        size = network.get('network_size', 0)
        
        print(f"\nCollaboration Network for {center}")
        print("-" * (25 + len(center)))
        print(f"Network size: {size} people")
        
        collaborators = network.get('collaborators', [])
        if collaborators:
            print("\nCollaborators by degree:")
            current_degree = None
            for collab in collaborators:
                degree = collab.get('degrees', 0)
                if degree != current_degree:
                    current_degree = degree
                    print(f"\n  {degree} degree{'s' if degree != 1 else ''}:")
                
                birth_year = f" ({collab['birth_year']})" if collab.get('birth_year') else ""
                nationality = f" - {collab['nationality']}" if collab.get('nationality') else ""
                print(f"    • {collab['name']}{birth_year}{nationality}")
    
    def display_connected_people(self, people):
        """Display most connected people."""
        print("\nMost Connected People")
        print("-" * 25)
        
        if not people:
            print("No data available.")
            return
        
        for i, person in enumerate(people, 1):
            birth_year = f" ({person['birth_year']})" if person.get('birth_year') else ""
            nationality = f" - {person['nationality']}" if person.get('nationality') else ""
            movie_conn = person.get('movie_connections', 0)
            person_conn = person.get('person_connections', 0)
            total_conn = person.get('total_connections', 0)
            print(f"{i:2d}. {person['name']}{birth_year}{nationality}")
            print(f"     Movies: {movie_conn}, People: {person_conn}, Total: {total_conn}")
    
    def display_genre_analysis(self, analysis):
        """Display genre analysis."""
        print("\nGenre Analysis")
        print("-" * 15)
        
        popularity = analysis.get('genre_popularity', [])
        if popularity:
            print("\nGenre Popularity:")
            for genre in popularity:
                avg_rating = f" (avg: {genre['avg_rating']:.1f})" if genre.get('avg_rating') else ""
                print(f"  • {genre['genre']}: {genre['movie_count']} movies{avg_rating}")
        
        cooccurrence = analysis.get('genre_cooccurrence', [])
        if cooccurrence:
            print("\nGenre Co-occurrence:")
            for pair in cooccurrence[:10]:  # Show top 10
                print(f"  • {pair['genre1']} + {pair['genre2']}: {pair['cooccurrence']} movies")
    
    def display_recommendations(self, recommendations, person_name):
        """Display movie recommendations."""
        print(f"\nMovie Recommendations for {person_name}")
        print("-" * (30 + len(person_name)))
        
        if not recommendations:
            print("No recommendations available.")
            return
        
        for i, rec in enumerate(recommendations, 1):
            rating = f" ({rec['rating']}/10)" if rec.get('rating') else ""
            strength = rec.get('recommendation_strength', 0)
            print(f"{i}. {rec['title']} ({rec['year']}){rating}")
            print(f"   Recommendation strength: {strength}")
            if rec.get('plot'):
                plot = rec['plot'][:100] + "..." if len(rec['plot']) > 100 else rec['plot']
                print(f"   Plot: {plot}")
    
    def display_actor_similarity(self, similar_actors, actor_name):
        """Display similar actors."""
        print(f"\nActors Similar to {actor_name}")
        print("-" * (20 + len(actor_name)))
        
        if not similar_actors:
            print("No similar actors found.")
            return
        
        for i, actor in enumerate(similar_actors, 1):
            birth_year = f" ({actor['birth_year']})" if actor.get('birth_year') else ""
            nationality = f" - {actor['nationality']}" if actor.get('nationality') else ""
            shared_genres = actor.get('shared_genres', 0)
            shared_movies = actor.get('shared_movies', 0)
            similarity = actor.get('similarity_score', 0)
            print(f"{i}. {actor['actor']}{birth_year}{nationality}")
            print(f"   Shared genres: {shared_genres}, Shared movies: {shared_movies}")
            print(f"   Similarity score: {similarity}")
    
    def display_temporal_analysis(self, analysis):
        """Display temporal analysis."""
        print("\nTemporal Analysis")
        print("-" * 17)
        
        movies_per_year = analysis.get('movies_per_year', [])
        if movies_per_year:
            print("\nMovies per year (recent years):")
            for year_data in movies_per_year[-10:]:  # Show last 10 years
                avg_rating = f" (avg: {year_data['avg_rating']:.1f})" if year_data.get('avg_rating') else ""
                print(f"  {year_data['year']}: {year_data['movie_count']} movies{avg_rating}")
        
        careers = analysis.get('longest_careers', [])
        if careers:
            print("\nLongest careers:")
            for career in careers:
                span = career['career_span']
                print(f"  • {career['person']}: {career['career_start']}-{career['career_end']} ({span} years)")
    
    def display_influential_movies(self, movies):
        """Display influential movies."""
        print("\nMost Influential Movies")
        print("-" * 23)
        
        if not movies:
            print("No data available.")
            return
        
        for i, movie in enumerate(movies, 1):
            rating = f" ({movie['rating']}/10)" if movie.get('rating') else ""
            cast_size = movie.get('cast_size', 0)
            connected = movie.get('connected_movies', 0)
            influence = movie.get('influence_score', 0)
            print(f"{i:2d}. {movie['title']} ({movie['year']}){rating}")
            print(f"     Cast size: {cast_size}, Connected movies: {connected}")
            print(f"     Influence score: {influence}")
    
    def run(self):
        """Run the interactive interface."""
        if not self.connect_to_database():
            return
        
        try:
            while True:
                self.display_main_menu()
                choice = input("\nEnter your choice: ").strip()
                
                if choice == "1":
                    self.handle_database_management()
                elif choice == "2":
                    self.handle_movie_operations()
                elif choice == "3":
                    self.handle_person_operations()
                elif choice == "4":
                    self.handle_graph_analytics()
                elif choice == "5":
                    # Search operations (simplified menu)
                    search_term = input("\nEnter search term: ").strip()
                    if search_term:
                        print("\nSearching movies...")
                        movies = self.movie_manager.search_movies(search_term)
                        self.display_movies_list(movies, f"Movie search: '{search_term}'")
                        
                        print("\nSearching people...")
                        people = self.person_manager.search_people(search_term)
                        self.display_people_list(people, f"People search: '{search_term}'")
                elif choice == "6":
                    print("\nData Import/Export features would be implemented here.")
                    print("Current implementation supports loading sample data from Database Management.")
                elif choice == "7":
                    db_info = self.client.get_database_info()
                    self.display_database_info(db_info)
                elif choice == "0":
                    print("\nGoodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
                
                # Pause for user to read results
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            print(f"\nAn unexpected error occurred: {e}")
        finally:
            if self.client:
                self.client.close()
