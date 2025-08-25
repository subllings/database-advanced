"""
Neo4j Client Module

This module handles the Neo4j connection and provides basic database operations.
"""

import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
import time


class Neo4jClient:
    """Neo4j client for movie graph operations."""
    
    def __init__(self, uri="bolt://localhost:7687", username="neo4j", password="password123"):
        """
        Initialize Neo4j client.
        
        Args:
            uri (str): Neo4j connection URI
            username (str): Neo4j username
            password (str): Neo4j password
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def connect(self, max_retries=3, retry_delay=2):
        """
        Connect to Neo4j database.
        
        Args:
            max_retries (int): Maximum connection retry attempts
            retry_delay (int): Delay between retry attempts in seconds
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Attempting to connect to Neo4j (attempt {attempt + 1}/{max_retries})")
                
                # Create Neo4j driver
                self.driver = GraphDatabase.driver(
                    self.uri,
                    auth=(self.username, self.password),
                    connection_timeout=10,
                    max_connection_lifetime=3600
                )
                
                # Test the connection
                with self.driver.session() as session:
                    session.run("RETURN 1")
                
                self.logger.info("Successfully connected to Neo4j")
                return True
                
            except (ServiceUnavailable, AuthError) as e:
                self.logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("All connection attempts failed")
                    return False
            except Exception as e:
                self.logger.error(f"Unexpected error during connection: {e}")
                return False
        
        return False
    
    def execute_query(self, query, parameters=None):
        """
        Execute a Cypher query.
        
        Args:
            query (str): Cypher query
            parameters (dict): Query parameters
            
        Returns:
            list: Query results
        """
        if self.driver is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Parameters: {parameters}")
            raise
    
    def execute_write_query(self, query, parameters=None):
        """
        Execute a write Cypher query.
        
        Args:
            query (str): Cypher query
            parameters (dict): Query parameters
            
        Returns:
            list: Query results
        """
        if self.driver is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        try:
            with self.driver.session() as session:
                result = session.write_transaction(self._execute_query, query, parameters or {})
                return result
        except Exception as e:
            self.logger.error(f"Error executing write query: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Parameters: {parameters}")
            raise
    
    def _execute_query(self, tx, query, parameters):
        """
        Execute query within a transaction.
        
        Args:
            tx: Neo4j transaction
            query (str): Cypher query
            parameters (dict): Query parameters
            
        Returns:
            list: Query results
        """
        result = tx.run(query, parameters)
        return [record.data() for record in result]
    
    def get_database_info(self):
        """
        Get database information and statistics.
        
        Returns:
            dict: Database information
        """
        try:
            # Get node count by label
            node_counts = self.execute_query("""
                CALL db.labels() YIELD label
                CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {})
                YIELD value
                RETURN label, value.count as count
            """)
            
            # Get relationship count by type
            rel_counts = self.execute_query("""
                CALL db.relationshipTypes() YIELD relationshipType
                CALL apoc.cypher.run('MATCH ()-[r:' + relationshipType + ']->() RETURN count(r) as count', {})
                YIELD value
                RETURN relationshipType, value.count as count
            """)
            
            # Get total counts
            total_nodes = self.execute_query("MATCH (n) RETURN count(n) as count")[0]['count']
            total_relationships = self.execute_query("MATCH ()-[r]->() RETURN count(r) as count")[0]['count']
            
            return {
                "connected": True,
                "uri": self.uri,
                "total_nodes": total_nodes,
                "total_relationships": total_relationships,
                "node_counts": {item['label']: item['count'] for item in node_counts},
                "relationship_counts": {item['relationshipType']: item['count'] for item in rel_counts}
            }
            
        except Exception as e:
            self.logger.error(f"Error getting database info: {e}")
            return {"connected": False, "message": str(e)}
    
    def clear_database(self):
        """
        Clear all data from the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.execute_write_query("MATCH (n) DETACH DELETE n")
            self.logger.info("Database cleared successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing database: {e}")
            return False
    
    def create_indexes(self):
        """
        Create indexes for better performance.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            indexes = [
                "CREATE INDEX movie_title IF NOT EXISTS FOR (m:Movie) ON (m.title)",
                "CREATE INDEX movie_year IF NOT EXISTS FOR (m:Movie) ON (m.year)",
                "CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)",
                "CREATE INDEX genre_name IF NOT EXISTS FOR (g:Genre) ON (g.name)"
            ]
            
            for index_query in indexes:
                self.execute_write_query(index_query)
            
            self.logger.info("Database indexes created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating indexes: {e}")
            return False
    
    def create_constraints(self):
        """
        Create constraints for data integrity.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            constraints = [
                "CREATE CONSTRAINT movie_title_unique IF NOT EXISTS FOR (m:Movie) REQUIRE m.title IS UNIQUE",
                "CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT genre_name_unique IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE"
            ]
            
            for constraint_query in constraints:
                try:
                    self.execute_write_query(constraint_query)
                except Exception as e:
                    # Constraints might already exist
                    self.logger.warning(f"Constraint creation warning: {e}")
            
            self.logger.info("Database constraints created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating constraints: {e}")
            return False
    
    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
            self.logger.info("Neo4j connection closed")
            self.driver = None
