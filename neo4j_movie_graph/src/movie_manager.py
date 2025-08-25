"""
Movie Manager Module

This module handles movie-specific operations in the Neo4j graph database.
"""

import logging
from neo4j_client import Neo4jClient


class MovieManager:
    """Manages movie operations in the Neo4j graph database."""
    
    def __init__(self, client: Neo4jClient):
        """
        Initialize movie manager.
        
        Args:
            client (Neo4jClient): Connected Neo4j client
        """
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def add_movie(self, title, year, rating=None, duration=None, plot=None, poster_url=None):
        """
        Add a new movie to the database.
        
        Args:
            title (str): Movie title
            year (int): Release year
            rating (float): Movie rating (optional)
            duration (int): Duration in minutes (optional)
            plot (str): Movie plot (optional)
            poster_url (str): Poster URL (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            CREATE (m:Movie {
                title: $title,
                year: $year,
                rating: $rating,
                duration: $duration,
                plot: $plot,
                poster_url: $poster_url
            })
            RETURN m
            """
            
            result = self.client.execute_write_query(query, {
                "title": title,
                "year": year,
                "rating": rating,
                "duration": duration,
                "plot": plot,
                "poster_url": poster_url
            })
            
            self.logger.info(f"Added movie: {title} ({year})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding movie {title}: {e}")
            return False
    
    def get_movie_by_title(self, title):
        """
        Get movie by title.
        
        Args:
            title (str): Movie title
            
        Returns:
            dict: Movie data or None
        """
        try:
            query = """
            MATCH (m:Movie {title: $title})
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot, m.poster_url as poster_url
            """
            
            result = self.client.execute_query(query, {"title": title})
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Error getting movie {title}: {e}")
            return None
    
    def search_movies(self, search_term, limit=10):
        """
        Search movies by title.
        
        Args:
            search_term (str): Search term
            limit (int): Maximum number of results
            
        Returns:
            list: List of matching movies
        """
        try:
            query = """
            MATCH (m:Movie)
            WHERE toLower(m.title) CONTAINS toLower($search_term)
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.rating DESC
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {
                "search_term": search_term,
                "limit": limit
            })
            
        except Exception as e:
            self.logger.error(f"Error searching movies: {e}")
            return []
    
    def get_movies_by_year(self, year):
        """
        Get movies by release year.
        
        Args:
            year (int): Release year
            
        Returns:
            list: List of movies from that year
        """
        try:
            query = """
            MATCH (m:Movie {year: $year})
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.rating DESC
            """
            
            return self.client.execute_query(query, {"year": year})
            
        except Exception as e:
            self.logger.error(f"Error getting movies by year {year}: {e}")
            return []
    
    def get_movies_by_rating_range(self, min_rating, max_rating=10.0):
        """
        Get movies within rating range.
        
        Args:
            min_rating (float): Minimum rating
            max_rating (float): Maximum rating
            
        Returns:
            list: List of movies within rating range
        """
        try:
            query = """
            MATCH (m:Movie)
            WHERE m.rating >= $min_rating AND m.rating <= $max_rating
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.rating DESC
            """
            
            return self.client.execute_query(query, {
                "min_rating": min_rating,
                "max_rating": max_rating
            })
            
        except Exception as e:
            self.logger.error(f"Error getting movies by rating range: {e}")
            return []
    
    def get_movie_cast(self, title):
        """
        Get cast of a movie.
        
        Args:
            title (str): Movie title
            
        Returns:
            list: List of actors and their characters
        """
        try:
            query = """
            MATCH (p:Person)-[r:ACTED_IN]->(m:Movie {title: $title})
            RETURN p.name as actor, r.character as character
            ORDER BY p.name
            """
            
            return self.client.execute_query(query, {"title": title})
            
        except Exception as e:
            self.logger.error(f"Error getting cast for {title}: {e}")
            return []
    
    def get_movie_directors(self, title):
        """
        Get directors of a movie.
        
        Args:
            title (str): Movie title
            
        Returns:
            list: List of directors
        """
        try:
            query = """
            MATCH (p:Person)-[:DIRECTED]->(m:Movie {title: $title})
            RETURN p.name as director, p.birth_year as birth_year, p.nationality as nationality
            ORDER BY p.name
            """
            
            return self.client.execute_query(query, {"title": title})
            
        except Exception as e:
            self.logger.error(f"Error getting directors for {title}: {e}")
            return []
    
    def get_movie_genres(self, title):
        """
        Get genres of a movie.
        
        Args:
            title (str): Movie title
            
        Returns:
            list: List of genres
        """
        try:
            query = """
            MATCH (m:Movie {title: $title})-[:HAS_GENRE]->(g:Genre)
            RETURN g.name as genre
            ORDER BY g.name
            """
            
            return self.client.execute_query(query, {"title": title})
            
        except Exception as e:
            self.logger.error(f"Error getting genres for {title}: {e}")
            return []
    
    def get_movies_by_genre(self, genre):
        """
        Get movies by genre.
        
        Args:
            genre (str): Genre name
            
        Returns:
            list: List of movies in that genre
        """
        try:
            query = """
            MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: $genre})
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.rating DESC
            """
            
            return self.client.execute_query(query, {"genre": genre})
            
        except Exception as e:
            self.logger.error(f"Error getting movies by genre {genre}: {e}")
            return []
    
    def get_movies_with_actor(self, actor_name):
        """
        Get movies featuring a specific actor.
        
        Args:
            actor_name (str): Actor name
            
        Returns:
            list: List of movies and characters
        """
        try:
            query = """
            MATCH (p:Person {name: $actor_name})-[r:ACTED_IN]->(m:Movie)
            RETURN m.title as title, m.year as year, m.rating as rating,
                   r.character as character
            ORDER BY m.year DESC
            """
            
            return self.client.execute_query(query, {"actor_name": actor_name})
            
        except Exception as e:
            self.logger.error(f"Error getting movies with actor {actor_name}: {e}")
            return []
    
    def get_movies_by_director(self, director_name):
        """
        Get movies by a specific director.
        
        Args:
            director_name (str): Director name
            
        Returns:
            list: List of movies
        """
        try:
            query = """
            MATCH (p:Person {name: $director_name})-[:DIRECTED]->(m:Movie)
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.year DESC
            """
            
            return self.client.execute_query(query, {"director_name": director_name})
            
        except Exception as e:
            self.logger.error(f"Error getting movies by director {director_name}: {e}")
            return []
    
    def get_similar_movies(self, title, limit=5):
        """
        Get movies similar to the given movie (same actors or directors).
        
        Args:
            title (str): Movie title
            limit (int): Maximum number of results
            
        Returns:
            list: List of similar movies
        """
        try:
            query = """
            MATCH (m1:Movie {title: $title})
            MATCH (m1)<-[:ACTED_IN|DIRECTED]-(p:Person)-[:ACTED_IN|DIRECTED]->(m2:Movie)
            WHERE m1 <> m2
            RETURN m2.title as title, m2.year as year, m2.rating as rating,
                   count(p) as shared_people
            ORDER BY shared_people DESC, m2.rating DESC
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {
                "title": title,
                "limit": limit
            })
            
        except Exception as e:
            self.logger.error(f"Error getting similar movies to {title}: {e}")
            return []
    
    def get_top_rated_movies(self, limit=10):
        """
        Get top rated movies.
        
        Args:
            limit (int): Maximum number of results
            
        Returns:
            list: List of top rated movies
        """
        try:
            query = """
            MATCH (m:Movie)
            WHERE m.rating IS NOT NULL
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.rating DESC
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {"limit": limit})
            
        except Exception as e:
            self.logger.error(f"Error getting top rated movies: {e}")
            return []
    
    def update_movie_rating(self, title, new_rating):
        """
        Update movie rating.
        
        Args:
            title (str): Movie title
            new_rating (float): New rating
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            MATCH (m:Movie {title: $title})
            SET m.rating = $new_rating
            RETURN m
            """
            
            result = self.client.execute_write_query(query, {
                "title": title,
                "new_rating": new_rating
            })
            
            if result:
                self.logger.info(f"Updated rating for {title} to {new_rating}")
                return True
            else:
                self.logger.warning(f"Movie not found: {title}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error updating rating for {title}: {e}")
            return False
    
    def delete_movie(self, title):
        """
        Delete a movie and all its relationships.
        
        Args:
            title (str): Movie title
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            MATCH (m:Movie {title: $title})
            DETACH DELETE m
            """
            
            self.client.execute_write_query(query, {"title": title})
            self.logger.info(f"Deleted movie: {title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting movie {title}: {e}")
            return False
