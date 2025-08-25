"""
Graph Analytics Module

This module provides graph analytics and algorithms for the movie database.
"""

import logging
from neo4j_client import Neo4jClient


class GraphAnalytics:
    """Provides graph analytics and algorithms for the movie database."""
    
    def __init__(self, client: Neo4jClient):
        """
        Initialize graph analytics.
        
        Args:
            client (Neo4jClient): Connected Neo4j client
        """
        self.client = client
        self.logger = logging.getLogger(__name__)
    
    def get_graph_statistics(self):
        """
        Get overall graph statistics.
        
        Returns:
            dict: Graph statistics
        """
        try:
            stats = {}
            
            # Basic counts
            stats['total_nodes'] = self.client.execute_query("MATCH (n) RETURN count(n) as count")[0]['count']
            stats['total_relationships'] = self.client.execute_query("MATCH ()-[r]->() RETURN count(r) as count")[0]['count']
            
            # Node counts by label
            node_counts = self.client.execute_query("""
                CALL db.labels() YIELD label
                CALL apoc.cypher.run('MATCH (n:' + label + ') RETURN count(n) as count', {})
                YIELD value
                RETURN label, value.count as count
            """)
            stats['node_counts'] = {item['label']: item['count'] for item in node_counts}
            
            # Relationship counts by type
            rel_counts = self.client.execute_query("""
                CALL db.relationshipTypes() YIELD relationshipType
                CALL apoc.cypher.run('MATCH ()-[r:' + relationshipType + ']->() RETURN count(r) as count', {})
                YIELD value
                RETURN relationshipType, value.count as count
            """)
            stats['relationship_counts'] = {item['relationshipType']: item['count'] for item in rel_counts}
            
            # Graph density (for movies and people only)
            movie_person_stats = self.client.execute_query("""
                MATCH (m:Movie), (p:Person)
                WITH count(m) as movies, count(p) as people
                MATCH (p:Person)-[r:ACTED_IN|DIRECTED]->(m:Movie)
                WITH movies, people, count(r) as relationships
                RETURN movies, people, relationships,
                       toFloat(relationships) / (movies * people) as density
            """)
            
            if movie_person_stats:
                stats['movie_person_density'] = movie_person_stats[0]['density']
                stats['movies'] = movie_person_stats[0]['movies']
                stats['people'] = movie_person_stats[0]['people']
                stats['movie_person_relationships'] = movie_person_stats[0]['relationships']
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting graph statistics: {e}")
            return {}
    
    def get_shortest_path(self, person1, person2):
        """
        Find shortest path between two people through movies.
        
        Args:
            person1 (str): First person's name
            person2 (str): Second person's name
            
        Returns:
            dict: Shortest path information
        """
        try:
            query = """
            MATCH p = shortestPath((p1:Person {name: $person1})-[*]-(p2:Person {name: $person2}))
            WHERE p1 <> p2
            RETURN p, length(p) as path_length
            """
            
            result = self.client.execute_query(query, {
                "person1": person1,
                "person2": person2
            })
            
            if result:
                return {
                    "path_exists": True,
                    "path_length": result[0]['path_length'],
                    "degrees_of_separation": result[0]['path_length'] // 2  # Divide by 2 because path includes movies
                }
            else:
                return {"path_exists": False}
                
        except Exception as e:
            self.logger.error(f"Error finding shortest path: {e}")
            return {"error": str(e)}
    
    def get_collaboration_network(self, person_name, depth=2):
        """
        Get collaboration network around a person.
        
        Args:
            person_name (str): Person's name
            depth (int): Network depth
            
        Returns:
            dict: Network data
        """
        try:
            query = f"""
            MATCH path = (p:Person {{name: $person_name}})-[:ACTED_IN|DIRECTED*1..{depth*2}]-(other:Person)
            WHERE p <> other
            WITH other, min(length(path)) as distance
            RETURN other.name as name, other.birth_year as birth_year,
                   other.nationality as nationality, distance/2 as degrees
            ORDER BY degrees, other.name
            """
            
            collaborators = self.client.execute_query(query, {"person_name": person_name})
            
            # Get direct collaborations for context
            direct_collabs = self.client.execute_query("""
                MATCH (p:Person {name: $person_name})-[:ACTED_IN|DIRECTED]->(m:Movie)<-[:ACTED_IN|DIRECTED]-(other:Person)
                WHERE p <> other
                RETURN other.name as name, collect(m.title) as shared_movies
                ORDER BY other.name
            """, {"person_name": person_name})
            
            return {
                "center_person": person_name,
                "network_size": len(collaborators),
                "collaborators": collaborators,
                "direct_collaborations": direct_collabs
            }
            
        except Exception as e:
            self.logger.error(f"Error getting collaboration network: {e}")
            return {}
    
    def get_most_connected_people(self, limit=10):
        """
        Get people with the most connections (highest degree centrality).
        
        Args:
            limit (int): Maximum number of results
            
        Returns:
            list: Most connected people
        """
        try:
            query = """
            MATCH (p:Person)-[r:ACTED_IN|DIRECTED]->(m:Movie)
            WITH p, count(r) as movie_connections
            MATCH (p)-[:ACTED_IN|DIRECTED]->(m:Movie)<-[:ACTED_IN|DIRECTED]-(other:Person)
            WHERE p <> other
            WITH p, movie_connections, count(DISTINCT other) as person_connections
            RETURN p.name as name, p.birth_year as birth_year,
                   p.nationality as nationality,
                   movie_connections, person_connections,
                   movie_connections + person_connections as total_connections
            ORDER BY total_connections DESC, p.name
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {"limit": limit})
            
        except Exception as e:
            self.logger.error(f"Error getting most connected people: {e}")
            return []
    
    def get_genre_analysis(self):
        """
        Analyze genre distribution and connections.
        
        Returns:
            dict: Genre analysis
        """
        try:
            # Genre popularity
            genre_popularity = self.client.execute_query("""
                MATCH (g:Genre)<-[:HAS_GENRE]-(m:Movie)
                RETURN g.name as genre, count(m) as movie_count,
                       avg(m.rating) as avg_rating
                ORDER BY movie_count DESC
            """)
            
            # Genre co-occurrence
            genre_cooccurrence = self.client.execute_query("""
                MATCH (m:Movie)-[:HAS_GENRE]->(g1:Genre)
                MATCH (m)-[:HAS_GENRE]->(g2:Genre)
                WHERE g1.name < g2.name
                RETURN g1.name as genre1, g2.name as genre2, count(m) as cooccurrence
                ORDER BY cooccurrence DESC
                LIMIT 20
            """)
            
            return {
                "genre_popularity": genre_popularity,
                "genre_cooccurrence": genre_cooccurrence
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing genres: {e}")
            return {}
    
    def get_movie_recommendations(self, person_name, limit=5):
        """
        Get movie recommendations based on collaboration patterns.
        
        Args:
            person_name (str): Person's name
            limit (int): Maximum number of recommendations
            
        Returns:
            list: Movie recommendations
        """
        try:
            query = """
            MATCH (p:Person {name: $person_name})-[:ACTED_IN|DIRECTED]->(m1:Movie)
            MATCH (m1)<-[:ACTED_IN|DIRECTED]-(other:Person)-[:ACTED_IN|DIRECTED]->(m2:Movie)
            WHERE p <> other AND NOT (p)-[:ACTED_IN|DIRECTED]->(m2)
            WITH m2, count(other) as recommendation_strength,
                 avg(m2.rating) as avg_rating
            WHERE m2.rating IS NOT NULL
            RETURN m2.title as title, m2.year as year, m2.rating as rating,
                   recommendation_strength,
                   m2.plot as plot
            ORDER BY recommendation_strength DESC, avg_rating DESC
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {
                "person_name": person_name,
                "limit": limit
            })
            
        except Exception as e:
            self.logger.error(f"Error getting movie recommendations: {e}")
            return []
    
    def get_actor_similarity(self, actor_name, limit=5):
        """
        Find actors similar to given actor based on shared movies and genres.
        
        Args:
            actor_name (str): Actor's name
            limit (int): Maximum number of results
            
        Returns:
            list: Similar actors
        """
        try:
            query = """
            MATCH (a1:Person {name: $actor_name})-[:ACTED_IN]->(m1:Movie)-[:HAS_GENRE]->(g:Genre)
            MATCH (a2:Person)-[:ACTED_IN]->(m2:Movie)-[:HAS_GENRE]->(g)
            WHERE a1 <> a2 AND NOT (a1)-[:ACTED_IN]->(m2)
            WITH a2, count(DISTINCT g) as shared_genres,
                 count(DISTINCT m2) as total_movies
            MATCH (a1)-[:ACTED_IN]->(shared_movie:Movie)<-[:ACTED_IN]-(a2)
            WITH a2, shared_genres, total_movies, count(shared_movie) as shared_movies
            RETURN a2.name as actor, a2.birth_year as birth_year,
                   a2.nationality as nationality,
                   shared_genres, shared_movies, total_movies,
                   (shared_genres + shared_movies * 2) as similarity_score
            ORDER BY similarity_score DESC, a2.name
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {
                "actor_name": actor_name,
                "limit": limit
            })
            
        except Exception as e:
            self.logger.error(f"Error getting actor similarity: {e}")
            return []
    
    def get_temporal_analysis(self):
        """
        Analyze trends over time.
        
        Returns:
            dict: Temporal analysis
        """
        try:
            # Movies per year
            movies_per_year = self.client.execute_query("""
                MATCH (m:Movie)
                WHERE m.year IS NOT NULL
                RETURN m.year as year, count(m) as movie_count, avg(m.rating) as avg_rating
                ORDER BY year
            """)
            
            # Career spans
            career_spans = self.client.execute_query("""
                MATCH (p:Person)-[:ACTED_IN|DIRECTED]->(m:Movie)
                WHERE m.year IS NOT NULL
                WITH p, min(m.year) as career_start, max(m.year) as career_end
                WHERE career_end > career_start
                RETURN p.name as person, career_start, career_end,
                       career_end - career_start as career_span
                ORDER BY career_span DESC
                LIMIT 10
            """)
            
            return {
                "movies_per_year": movies_per_year,
                "longest_careers": career_spans
            }
            
        except Exception as e:
            self.logger.error(f"Error in temporal analysis: {e}")
            return {}
    
    def get_influential_movies(self, limit=10):
        """
        Get most influential movies based on cast size and connections.
        
        Args:
            limit (int): Maximum number of results
            
        Returns:
            list: Most influential movies
        """
        try:
            query = """
            MATCH (m:Movie)<-[:ACTED_IN|DIRECTED]-(p:Person)
            WITH m, count(p) as cast_size
            MATCH (m)<-[:ACTED_IN|DIRECTED]-(p:Person)
            MATCH (p)-[:ACTED_IN|DIRECTED]->(other_movie:Movie)
            WHERE other_movie <> m
            WITH m, cast_size, count(DISTINCT other_movie) as connected_movies
            RETURN m.title as title, m.year as year, m.rating as rating,
                   cast_size, connected_movies,
                   cast_size * connected_movies as influence_score
            ORDER BY influence_score DESC, m.rating DESC
            LIMIT $limit
            """
            
            return self.client.execute_query(query, {"limit": limit})
            
        except Exception as e:
            self.logger.error(f"Error getting influential movies: {e}")
            return []
    
    def analyze_clustering_coefficient(self):
        """
        Calculate clustering coefficient for the collaboration network.
        
        Returns:
            dict: Clustering analysis
        """
        try:
            # This is a simplified clustering coefficient calculation
            query = """
            MATCH (p:Person)-[:ACTED_IN|DIRECTED]->(m:Movie)<-[:ACTED_IN|DIRECTED]-(friend:Person)
            WHERE p <> friend
            WITH p, collect(DISTINCT friend) as friends
            WHERE size(friends) >= 2
            UNWIND friends as friend1
            UNWIND friends as friend2
            WHERE friend1 <> friend2
            MATCH (friend1)-[:ACTED_IN|DIRECTED]->(shared_movie:Movie)<-[:ACTED_IN|DIRECTED]-(friend2)
            WITH p, size(friends) as friend_count, count(DISTINCT [friend1, friend2]) as connected_pairs
            WITH p, friend_count, connected_pairs,
                 toFloat(connected_pairs * 2) / (friend_count * (friend_count - 1)) as clustering_coefficient
            RETURN p.name as person, friend_count, connected_pairs, clustering_coefficient
            ORDER BY clustering_coefficient DESC
            LIMIT 10
            """
            
            return self.client.execute_query(query)
            
        except Exception as e:
            self.logger.error(f"Error analyzing clustering coefficient: {e}")
            return []
