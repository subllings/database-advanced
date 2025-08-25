"""
Data Loader Module

This module handles loading movie and person data into the Neo4j graph database.
"""

import logging
import json
import csv
from pathlib import Path
from neo4j_client import Neo4jClient


class DataLoader:
    """Loads movie and person data into Neo4j graph database."""
    
    def __init__(self, client: Neo4jClient):
        """
        Initialize data loader.
        
        Args:
            client (Neo4jClient): Connected Neo4j client
        """
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def load_sample_data(self):
        """
        Load sample movie and person data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info("Loading sample movie data...")
            
            # Sample movies data
            movies_data = [
                {
                    "title": "The Matrix",
                    "year": 1999,
                    "rating": 8.7,
                    "duration": 136,
                    "plot": "A computer programmer discovers that reality as he knows it might not be real.",
                    "poster_url": "https://example.com/matrix.jpg"
                },
                {
                    "title": "The Matrix Reloaded",
                    "year": 2003,
                    "rating": 7.2,
                    "duration": 138,
                    "plot": "Neo and his allies race against time before the machines discover the city of Zion.",
                    "poster_url": "https://example.com/matrix_reloaded.jpg"
                },
                {
                    "title": "The Matrix Revolutions",
                    "year": 2003,
                    "rating": 6.7,
                    "duration": 129,
                    "plot": "The human city of Zion defends itself against the massive invasion of the machines.",
                    "poster_url": "https://example.com/matrix_revolutions.jpg"
                },
                {
                    "title": "John Wick",
                    "year": 2014,
                    "rating": 7.4,
                    "duration": 101,
                    "plot": "An ex-hit-man comes out of retirement to track down the gangsters that took everything from him.",
                    "poster_url": "https://example.com/john_wick.jpg"
                },
                {
                    "title": "John Wick: Chapter 2",
                    "year": 2017,
                    "rating": 7.4,
                    "duration": 122,
                    "plot": "After returning to the criminal underworld to repay a debt, John Wick discovers that a large bounty has been put on his life.",
                    "poster_url": "https://example.com/john_wick_2.jpg"
                },
                {
                    "title": "Speed",
                    "year": 1994,
                    "rating": 7.3,
                    "duration": 116,
                    "plot": "A young police officer must prevent a bomb exploding aboard a city bus by keeping its speed above 50 mph.",
                    "poster_url": "https://example.com/speed.jpg"
                },
                {
                    "title": "The Devil Wears Prada",
                    "year": 2006,
                    "rating": 6.9,
                    "duration": 109,
                    "plot": "A smart but sensible new graduate lands a job as an assistant to Miranda Priestly, the demanding editor-in-chief of a high fashion magazine.",
                    "poster_url": "https://example.com/devil_wears_prada.jpg"
                },
                {
                    "title": "Forrest Gump",
                    "year": 1994,
                    "rating": 8.8,
                    "duration": 142,
                    "plot": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man.",
                    "poster_url": "https://example.com/forrest_gump.jpg"
                },
                {
                    "title": "The Godfather",
                    "year": 1972,
                    "rating": 9.2,
                    "duration": 175,
                    "plot": "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
                    "poster_url": "https://example.com/godfather.jpg"
                },
                {
                    "title": "Pulp Fiction",
                    "year": 1994,
                    "rating": 8.9,
                    "duration": 154,
                    "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
                    "poster_url": "https://example.com/pulp_fiction.jpg"
                }
            ]
            
            # Sample people data
            people_data = [
                {"name": "Keanu Reeves", "birth_year": 1964, "nationality": "Canadian"},
                {"name": "Laurence Fishburne", "birth_year": 1961, "nationality": "American"},
                {"name": "Carrie-Anne Moss", "birth_year": 1967, "nationality": "Canadian"},
                {"name": "Hugo Weaving", "birth_year": 1960, "nationality": "British"},
                {"name": "Lana Wachowski", "birth_year": 1965, "nationality": "American"},
                {"name": "Lilly Wachowski", "birth_year": 1967, "nationality": "American"},
                {"name": "Chad Stahelski", "birth_year": 1968, "nationality": "American"},
                {"name": "Jan de Bont", "birth_year": 1943, "nationality": "Dutch"},
                {"name": "Sandra Bullock", "birth_year": 1964, "nationality": "American"},
                {"name": "Dennis Hopper", "birth_year": 1936, "nationality": "American"},
                {"name": "David Frankel", "birth_year": 1959, "nationality": "American"},
                {"name": "Meryl Streep", "birth_year": 1949, "nationality": "American"},
                {"name": "Anne Hathaway", "birth_year": 1982, "nationality": "American"},
                {"name": "Robert Zemeckis", "birth_year": 1951, "nationality": "American"},
                {"name": "Tom Hanks", "birth_year": 1956, "nationality": "American"},
                {"name": "Francis Ford Coppola", "birth_year": 1939, "nationality": "American"},
                {"name": "Marlon Brando", "birth_year": 1924, "nationality": "American"},
                {"name": "Al Pacino", "birth_year": 1940, "nationality": "American"},
                {"name": "Quentin Tarantino", "birth_year": 1963, "nationality": "American"},
                {"name": "John Travolta", "birth_year": 1954, "nationality": "American"},
                {"name": "Samuel L. Jackson", "birth_year": 1948, "nationality": "American"}
            ]
            
            # Sample genres
            genres_data = [
                {"name": "Action"},
                {"name": "Sci-Fi"},
                {"name": "Thriller"},
                {"name": "Drama"},
                {"name": "Crime"},
                {"name": "Comedy"},
                {"name": "Romance"}
            ]
            
            # Load data into database
            success = True
            success &= self._load_movies(movies_data)
            success &= self._load_people(people_data)
            success &= self._load_genres(genres_data)
            success &= self._create_relationships()
            
            if success:
                self.logger.info("Sample data loaded successfully")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error loading sample data: {e}")
            return False
    
    def _load_movies(self, movies_data):
        """Load movies into the database."""
        try:
            query = """
            UNWIND $movies as movie
            CREATE (m:Movie {
                title: movie.title,
                year: movie.year,
                rating: movie.rating,
                duration: movie.duration,
                plot: movie.plot,
                poster_url: movie.poster_url
            })
            """
            
            self.client.execute_write_query(query, {"movies": movies_data})
            self.logger.info(f"Loaded {len(movies_data)} movies")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading movies: {e}")
            return False
    
    def _load_people(self, people_data):
        """Load people into the database."""
        try:
            query = """
            UNWIND $people as person
            CREATE (p:Person {
                name: person.name,
                birth_year: person.birth_year,
                nationality: person.nationality
            })
            """
            
            self.client.execute_write_query(query, {"people": people_data})
            self.logger.info(f"Loaded {len(people_data)} people")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading people: {e}")
            return False
    
    def _load_genres(self, genres_data):
        """Load genres into the database."""
        try:
            query = """
            UNWIND $genres as genre
            CREATE (g:Genre {
                name: genre.name
            })
            """
            
            self.client.execute_write_query(query, {"genres": genres_data})
            self.logger.info(f"Loaded {len(genres_data)} genres")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading genres: {e}")
            return False
    
    def _create_relationships(self):
        """Create relationships between movies, people, and genres."""
        try:
            # Actor relationships
            actor_relationships = [
                ("Keanu Reeves", "The Matrix", "Neo"),
                ("Keanu Reeves", "The Matrix Reloaded", "Neo"),
                ("Keanu Reeves", "The Matrix Revolutions", "Neo"),
                ("Keanu Reeves", "John Wick", "John Wick"),
                ("Keanu Reeves", "John Wick: Chapter 2", "John Wick"),
                ("Keanu Reeves", "Speed", "Jack Traven"),
                ("Laurence Fishburne", "The Matrix", "Morpheus"),
                ("Laurence Fishburne", "The Matrix Reloaded", "Morpheus"),
                ("Laurence Fishburne", "The Matrix Revolutions", "Morpheus"),
                ("Carrie-Anne Moss", "The Matrix", "Trinity"),
                ("Carrie-Anne Moss", "The Matrix Reloaded", "Trinity"),
                ("Carrie-Anne Moss", "The Matrix Revolutions", "Trinity"),
                ("Hugo Weaving", "The Matrix", "Agent Smith"),
                ("Hugo Weaving", "The Matrix Reloaded", "Agent Smith"),
                ("Hugo Weaving", "The Matrix Revolutions", "Agent Smith"),
                ("Sandra Bullock", "Speed", "Annie Porter"),
                ("Sandra Bullock", "The Devil Wears Prada", "Andy Sachs"),
                ("Dennis Hopper", "Speed", "Howard Payne"),
                ("Meryl Streep", "The Devil Wears Prada", "Miranda Priestly"),
                ("Anne Hathaway", "The Devil Wears Prada", "Andy Sachs"),
                ("Tom Hanks", "Forrest Gump", "Forrest Gump"),
                ("Marlon Brando", "The Godfather", "Vito Corleone"),
                ("Al Pacino", "The Godfather", "Michael Corleone"),
                ("John Travolta", "Pulp Fiction", "Vincent Vega"),
                ("Samuel L. Jackson", "Pulp Fiction", "Jules Winnfield")
            ]
            
            for actor, movie, character in actor_relationships:
                query = """
                MATCH (p:Person {name: $actor})
                MATCH (m:Movie {title: $movie})
                CREATE (p)-[:ACTED_IN {character: $character}]->(m)
                """
                self.client.execute_write_query(query, {
                    "actor": actor, "movie": movie, "character": character
                })
            
            # Director relationships
            director_relationships = [
                ("Lana Wachowski", "The Matrix"),
                ("Lilly Wachowski", "The Matrix"),
                ("Lana Wachowski", "The Matrix Reloaded"),
                ("Lilly Wachowski", "The Matrix Reloaded"),
                ("Lana Wachowski", "The Matrix Revolutions"),
                ("Lilly Wachowski", "The Matrix Revolutions"),
                ("Chad Stahelski", "John Wick"),
                ("Chad Stahelski", "John Wick: Chapter 2"),
                ("Jan de Bont", "Speed"),
                ("David Frankel", "The Devil Wears Prada"),
                ("Robert Zemeckis", "Forrest Gump"),
                ("Francis Ford Coppola", "The Godfather"),
                ("Quentin Tarantino", "Pulp Fiction")
            ]
            
            for director, movie in director_relationships:
                query = """
                MATCH (p:Person {name: $director})
                MATCH (m:Movie {title: $movie})
                CREATE (p)-[:DIRECTED]->(m)
                """
                self.client.execute_write_query(query, {
                    "director": director, "movie": movie
                })
            
            # Genre relationships
            genre_relationships = [
                ("The Matrix", ["Action", "Sci-Fi"]),
                ("The Matrix Reloaded", ["Action", "Sci-Fi"]),
                ("The Matrix Revolutions", ["Action", "Sci-Fi"]),
                ("John Wick", ["Action", "Thriller"]),
                ("John Wick: Chapter 2", ["Action", "Thriller"]),
                ("Speed", ["Action", "Thriller"]),
                ("The Devil Wears Prada", ["Comedy", "Drama"]),
                ("Forrest Gump", ["Drama", "Romance"]),
                ("The Godfather", ["Crime", "Drama"]),
                ("Pulp Fiction", ["Crime", "Drama"])
            ]
            
            for movie, genres in genre_relationships:
                for genre in genres:
                    query = """
                    MATCH (m:Movie {title: $movie})
                    MATCH (g:Genre {name: $genre})
                    CREATE (m)-[:HAS_GENRE]->(g)
                    """
                    self.client.execute_write_query(query, {
                        "movie": movie, "genre": genre
                    })
            
            self.logger.info("Relationships created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating relationships: {e}")
            return False
    
    def load_from_csv(self, csv_file_path):
        """
        Load data from CSV file.
        
        Args:
            csv_file_path (str): Path to CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            csv_path = Path(csv_file_path)
            if not csv_path.exists():
                self.logger.error(f"CSV file not found: {csv_file_path}")
                return False
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
            
            # Process based on file name or content
            filename = csv_path.stem.lower()
            
            if 'movie' in filename:
                return self._load_movies(data)
            elif 'person' in filename or 'people' in filename:
                return self._load_people(data)
            elif 'genre' in filename:
                return self._load_genres(data)
            else:
                self.logger.warning(f"Unknown CSV format: {filename}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading from CSV: {e}")
            return False
    
    def load_from_json(self, json_file_path):
        """
        Load data from JSON file.
        
        Args:
            json_file_path (str): Path to JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            json_path = Path(json_file_path)
            if not json_path.exists():
                self.logger.error(f"JSON file not found: {json_file_path}")
                return False
            
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Process based on data structure
            if isinstance(data, dict):
                if 'movies' in data:
                    self._load_movies(data['movies'])
                if 'people' in data:
                    self._load_people(data['people'])
                if 'genres' in data:
                    self._load_genres(data['genres'])
                return True
            else:
                self.logger.error("Invalid JSON structure")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading from JSON: {e}")
            return False
