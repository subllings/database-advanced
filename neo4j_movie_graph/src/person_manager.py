"""
Person Manager Module

This module handles person-specific operations in the Neo4j graph database.
"""

import logging
from neo4j_client import Neo4jClient


class PersonManager:
    """Manages person operations in the Neo4j graph database."""
    
    def __init__(self, client: Neo4jClient):
        """
        Initialize person manager.
        
        Args:
            client (Neo4jClient): Connected Neo4j client
        """
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def add_person(self, name, birth_year=None, nationality=None, biography=None):
        """
        Add a new person to the database.
        
        Args:
            name (str): Person's name
            birth_year (int): Birth year (optional)
            nationality (str): Nationality (optional)
            biography (str): Biography (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            CREATE (p:Person {
                name: $name,
                birth_year: $birth_year,
                nationality: $nationality,
                biography: $biography
            })
            RETURN p
            """
            
            result = self.client.execute_write_query(query, {
                "name": name,
                "birth_year": birth_year,
                "nationality": nationality,
                "biography": biography
            })
            
            self.logger.info(f"Added person: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding person {name}: {e}")
            return False
    
    def get_person_by_name(self, name):
        """
        Get person by name.
        
        Args:
            name (str): Person's name
            
        Returns:
            dict: Person data or None
        """
        try:
            query = """
            MATCH (p:Person {name: $name})
            RETURN p.name as name, p.birth_year as birth_year,
                   p.nationality as nationality, p.biography as biography
            """
            
            result = self.client.execute_query(query, {"name": name})
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Error getting person {name}: {e}")
            return None
    
    def search_people(self, search_term, limit=10):
        """
        Search people by name.
        
        Args:
            search_term (str): Search term
            limit (int): Maximum number of results
            
        Returns:
            list: List of matching people
        """
        try:
            query = """
            MATCH (p:Person)
            WHERE toLower(p.name) CONTAINS toLower($search_term)
            RETURN p.name as name, p.birth_year as birth_year,
                   p.nationality as nationality
            ORDER BY p.name
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {
                "search_term": search_term,
                "limit": limit
            })
            
        except Exception as e:
            self.logger.error(f"Error searching people: {e}")
            return []
    
    def get_person_movies_as_actor(self, name):
        """
        Get movies where person acted.
        
        Args:
            name (str): Person's name
            
        Returns:
            list: List of movies and characters
        """
        try:
            query = """
            MATCH (p:Person {name: $name})-[r:ACTED_IN]->(m:Movie)
            RETURN m.title as title, m.year as year, m.rating as rating,
                   r.character as character
            ORDER BY m.year DESC
            """
            
            return self.client.execute_query(query, {"name": name})
            
        except Exception as e:
            self.logger.error(f"Error getting actor movies for {name}: {e}")
            return []
    
    def get_person_movies_as_director(self, name):
        """
        Get movies where person directed.
        
        Args:
            name (str): Person's name
            
        Returns:
            list: List of movies
        """
        try:
            query = """
            MATCH (p:Person {name: $name})-[:DIRECTED]->(m:Movie)
            RETURN m.title as title, m.year as year, m.rating as rating,
                   m.duration as duration, m.plot as plot
            ORDER BY m.year DESC
            """
            
            return self.client.execute_query(query, {"name": name})
            
        except Exception as e:
            self.logger.error(f"Error getting director movies for {name}: {e}")
            return []
    
    def get_person_collaborators(self, name, limit=10):
        """
        Get people who collaborated with this person.
        
        Args:
            name (str): Person's name
            limit (int): Maximum number of results
            
        Returns:
            list: List of collaborators and collaboration count
        """
        try:
            query = """
            MATCH (p1:Person {name: $name})-[:ACTED_IN|DIRECTED]->(m:Movie)<-[:ACTED_IN|DIRECTED]-(p2:Person)
            WHERE p1 <> p2
            RETURN p2.name as collaborator, p2.birth_year as birth_year,
                   p2.nationality as nationality, count(m) as collaborations
            ORDER BY collaborations DESC, p2.name
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {
                "name": name,
                "limit": limit
            })
            
        except Exception as e:
            self.logger.error(f"Error getting collaborators for {name}: {e}")
            return []
    
    def get_actors_by_nationality(self, nationality):
        """
        Get actors by nationality.
        
        Args:
            nationality (str): Nationality
            
        Returns:
            list: List of actors from that nationality
        """
        try:
            query = """
            MATCH (p:Person {nationality: $nationality})-[:ACTED_IN]->(m:Movie)
            RETURN DISTINCT p.name as name, p.birth_year as birth_year,
                   count(m) as movie_count
            ORDER BY movie_count DESC, p.name
            """
            
            return self.client.execute_query(query, {"nationality": nationality})
            
        except Exception as e:
            self.logger.error(f"Error getting actors by nationality {nationality}: {e}")
            return []
    
    def get_directors_by_nationality(self, nationality):
        """
        Get directors by nationality.
        
        Args:
            nationality (str): Nationality
            
        Returns:
            list: List of directors from that nationality
        """
        try:
            query = """
            MATCH (p:Person {nationality: $nationality})-[:DIRECTED]->(m:Movie)
            RETURN DISTINCT p.name as name, p.birth_year as birth_year,
                   count(m) as movie_count
            ORDER BY movie_count DESC, p.name
            """
            
            return self.client.execute_query(query, {"nationality": nationality})
            
        except Exception as e:
            self.logger.error(f"Error getting directors by nationality {nationality}: {e}")
            return []
    
    def get_most_prolific_actors(self, limit=10):
        """
        Get actors with most movies.
        
        Args:
            limit (int): Maximum number of results
            
        Returns:
            list: List of actors and their movie count
        """
        try:
            query = """
            MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
            RETURN p.name as name, p.birth_year as birth_year,
                   p.nationality as nationality, count(m) as movie_count
            ORDER BY movie_count DESC, p.name
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {"limit": limit})
            
        except Exception as e:
            self.logger.error(f"Error getting most prolific actors: {e}")
            return []
    
    def get_most_prolific_directors(self, limit=10):
        """
        Get directors with most movies.
        
        Args:
            limit (int): Maximum number of results
            
        Returns:
            list: List of directors and their movie count
        """
        try:
            query = """
            MATCH (p:Person)-[:DIRECTED]->(m:Movie)
            RETURN p.name as name, p.birth_year as birth_year,
                   p.nationality as nationality, count(m) as movie_count
            ORDER BY movie_count DESC, p.name
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {"limit": limit})
            
        except Exception as e:
            self.logger.error(f"Error getting most prolific directors: {e}")
            return []
    
    def get_actor_director_pairs(self):
        """
        Get people who are both actors and directors.
        
        Returns:
            list: List of actor-directors
        """
        try:
            query = """
            MATCH (p:Person)-[:ACTED_IN]->(m1:Movie)
            MATCH (p)-[:DIRECTED]->(m2:Movie)
            RETURN DISTINCT p.name as name, p.birth_year as birth_year,
                   p.nationality as nationality,
                   count(DISTINCT m1) as acted_movies,
                   count(DISTINCT m2) as directed_movies
            ORDER BY p.name
            """
            
            return self.client.execute_query(query)
            
        except Exception as e:
            self.logger.error(f"Error getting actor-director pairs: {e}")
            return []
    
    def add_actor_relationship(self, person_name, movie_title, character=None):
        """
        Add acting relationship between person and movie.
        
        Args:
            person_name (str): Actor's name
            movie_title (str): Movie title
            character (str): Character name (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            MATCH (p:Person {name: $person_name})
            MATCH (m:Movie {title: $movie_title})
            CREATE (p)-[:ACTED_IN {character: $character}]->(m)
            """
            
            self.client.execute_write_query(query, {
                "person_name": person_name,
                "movie_title": movie_title,
                "character": character
            })
            
            self.logger.info(f"Added acting relationship: {person_name} -> {movie_title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding acting relationship: {e}")
            return False
    
    def add_director_relationship(self, person_name, movie_title):
        """
        Add directing relationship between person and movie.
        
        Args:
            person_name (str): Director's name
            movie_title (str): Movie title
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            MATCH (p:Person {name: $person_name})
            MATCH (m:Movie {title: $movie_title})
            CREATE (p)-[:DIRECTED]->(m)
            """
            
            self.client.execute_write_query(query, {
                "person_name": person_name,
                "movie_title": movie_title
            })
            
            self.logger.info(f"Added directing relationship: {person_name} -> {movie_title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding directing relationship: {e}")
            return False
    
    def get_people_born_in_year(self, year):
        """
        Get people born in a specific year.
        
        Args:
            year (int): Birth year
            
        Returns:
            list: List of people born in that year
        """
        try:
            query = """
            MATCH (p:Person {birth_year: $year})
            RETURN p.name as name, p.nationality as nationality
            ORDER BY p.name
            """
            
            return self.client.execute_query(query, {"year": year})
            
        except Exception as e:
            self.logger.error(f"Error getting people born in {year}: {e}")
            return []
    
    def update_person_info(self, name, birth_year=None, nationality=None, biography=None):
        """
        Update person information.
        
        Args:
            name (str): Person's name
            birth_year (int): Birth year (optional)
            nationality (str): Nationality (optional)
            biography (str): Biography (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build update query dynamically
            set_clauses = []
            params = {"name": name}
            
            if birth_year is not None:
                set_clauses.append("p.birth_year = $birth_year")
                params["birth_year"] = birth_year
            
            if nationality is not None:
                set_clauses.append("p.nationality = $nationality")
                params["nationality"] = nationality
            
            if biography is not None:
                set_clauses.append("p.biography = $biography")
                params["biography"] = biography
            
            if not set_clauses:
                self.logger.warning("No fields to update")
                return False
            
            query = f"""
            MATCH (p:Person {{name: $name}})
            SET {", ".join(set_clauses)}
            RETURN p
            """
            
            result = self.client.execute_write_query(query, params)
            
            if result:
                self.logger.info(f"Updated person info for: {name}")
                return True
            else:
                self.logger.warning(f"Person not found: {name}")
                return False
            
        except Exception as e:
            self.logger.error(f"Error updating person {name}: {e}")
            return False
    
    def delete_person(self, name):
        """
        Delete a person and all their relationships.
        
        Args:
            name (str): Person's name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            query = """
            MATCH (p:Person {name: $name})
            DETACH DELETE p
            """
            
            self.client.execute_write_query(query, {"name": name})
            self.logger.info(f"Deleted person: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting person {name}: {e}")
            return False
