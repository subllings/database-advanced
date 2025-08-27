"""
Movie data indexer for Elasticsearch.

This module handles the creation of movie index, data preparation,
and bulk indexing operations for the movie search application.
"""

import os
import json
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import RequestError
from src.elasticsearch_client import ElasticsearchClient


class MovieDataIndexer:
    """
    Movie data indexer for Elasticsearch.
    
    This class manages the creation of movie index, data preparation,
    and bulk indexing operations.
    """

    def __init__(self, es_client: Optional[ElasticsearchClient] = None):
        """
        Initialize the movie data indexer.
        
        Args:
            es_client: Elasticsearch client instance
        """
        self.es_client = es_client or ElasticsearchClient()
        self.client = self.es_client.client
        self.index_name = self.es_client.index_name

    def get_movie_mapping(self) -> Dict[str, Any]:
        """
        Get the mapping configuration for movie documents.
        
        Returns:
            Dictionary containing the Elasticsearch mapping
        """
        return {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "description": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "genres": {
                    "type": "keyword"
                },
                "year": {
                    "type": "integer"
                },
                "rating": {
                    "type": "float"
                },
                "director": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "cast": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "duration": {
                    "type": "integer"
                },
                "budget": {
                    "type": "long"
                },
                "box_office": {
                    "type": "long"
                },
                "language": {
                    "type": "keyword"
                },
                "country": {
                    "type": "keyword"
                },
                "indexed_at": {
                    "type": "date"
                }
            }
        }

    def setup_index(self) -> bool:
        """
        Set up the movie index with proper mapping.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete existing index if it exists
            if self.es_client.check_index_exists():
                print(f"Deleting existing index '{self.index_name}'...")
                self.es_client.delete_index()

            # Create new index with mapping
            mapping = self.get_movie_mapping()
            success = self.es_client.create_index(mapping=mapping)
            
            if success:
                print(f"Successfully created index '{self.index_name}' with mapping")
                return True
            else:
                print(f"Failed to create index '{self.index_name}'")
                return False
                
        except Exception as e:
            print(f"Error setting up index: {e}")
            return False

    def get_sample_movies(self) -> List[Dict[str, Any]]:
        """
        Get sample movie data for indexing.
        
        Returns:
            List of movie dictionaries
        """
        return [
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "genres": ["Action", "Crime", "Drama"],
                "year": 2008,
                "rating": 9.0,
                "director": "Christopher Nolan",
                "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
                "duration": 152,
                "budget": 185000000,
                "box_office": 1004558444,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "genres": ["Action", "Sci-Fi", "Thriller"],
                "year": 2010,
                "rating": 8.8,
                "director": "Christopher Nolan",
                "cast": ["Leonardo DiCaprio", "Marion Cotillard", "Tom Hardy"],
                "duration": 148,
                "budget": 160000000,
                "box_office": 836836967,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "Pulp Fiction",
                "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "genres": ["Crime", "Drama"],
                "year": 1994,
                "rating": 8.9,
                "director": "Quentin Tarantino",
                "cast": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
                "duration": 154,
                "budget": 8000000,
                "box_office": 214179088,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "The Matrix",
                "description": "A computer programmer is led to fight an underground war against powerful computers who have constructed his entire reality with a system called the Matrix.",
                "genres": ["Action", "Sci-Fi"],
                "year": 1999,
                "rating": 8.7,
                "director": "The Wachowskis",
                "cast": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
                "duration": 136,
                "budget": 63000000,
                "box_office": 467222824,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "genres": ["Adventure", "Drama", "Sci-Fi"],
                "year": 2014,
                "rating": 8.6,
                "director": "Christopher Nolan",
                "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
                "duration": 169,
                "budget": 165000000,
                "box_office": 677471339,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "The Godfather",
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "genres": ["Crime", "Drama"],
                "year": 1972,
                "rating": 9.2,
                "director": "Francis Ford Coppola",
                "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
                "duration": 175,
                "budget": 6000000,
                "box_office": 246120974,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "Forrest Gump",
                "description": "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
                "genres": ["Drama", "Romance"],
                "year": 1994,
                "rating": 8.8,
                "director": "Robert Zemeckis",
                "cast": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
                "duration": 142,
                "budget": 55000000,
                "box_office": 677387716,
                "language": "English",
                "country": "USA"
            },
            {
                "title": "The Grand Budapest Hotel",
                "description": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.",
                "genres": ["Adventure", "Comedy", "Crime"],
                "year": 2014,
                "rating": 8.1,
                "director": "Wes Anderson",
                "cast": ["Ralph Fiennes", "F. Murray Abraham", "Mathieu Amalric"],
                "duration": 99,
                "budget": 25000000,
                "box_office": 174600318,
                "language": "English",
                "country": "Germany"
            }
        ]

    def index_sample_movies(self) -> Tuple[bool, int]:
        """
        Index sample movies into Elasticsearch.
        
        Returns:
            Tuple of (success: bool, count: int)
        """
        try:
            movies = self.get_sample_movies()
            
            # Prepare documents for bulk indexing
            docs = []
            for movie in movies:
                # Add timestamp
                movie['indexed_at'] = datetime.now().isoformat()
                
                doc = {
                    "_index": self.index_name,
                    "_source": movie
                }
                docs.append(doc)
            
            # Bulk index documents
            success, failed = helpers.bulk(
                self.client,
                docs,
                index=self.index_name,
                refresh=True
            )
            
            print(f"Successfully indexed {len(docs)} movies")
            return True, len(docs)
            
        except Exception as e:
            print(f"Error indexing movies: {e}")
            return False, 0

    def get_index_info(self) -> Dict[str, Any]:
        """
        Get information about the movie index.
        
        Returns:
            Dictionary containing index information
        """
        return self.es_client.get_index_info()

    def delete_all_movies(self) -> bool:
        """
        Delete all movies from the index.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete all documents
            response = self.client.delete_by_query(
                index=self.index_name,
                query={"match_all": {}}
            )
            
            deleted_count = response.get('deleted', 0)
            print(f"Deleted {deleted_count} movies from index")
            return True
            
        except Exception as e:
            print(f"Error deleting movies: {e}")
            return False
