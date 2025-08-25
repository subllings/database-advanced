"""
Data indexer for movie search engine.

This module handles downloading, processing, and indexing movie data
into Elasticsearch. It creates sample movie data and manages the
indexing process with proper error handling.
"""

import json
import os
from typing import List, Dict, Any
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_client import ElasticsearchClient


class MovieDataIndexer:
    """
    Handles indexing of movie data into Elasticsearch.
    
    This class manages the creation of movie index, data preparation,
    and bulk indexing operations with proper error handling.
    """
    
    def __init__(self):
        """Initialize the data indexer with Elasticsearch client."""
        self.es_client = ElasticsearchClient()
        self.client = self.es_client.get_client()
        self.index_name = self.es_client.get_index_name()
        
    def get_movie_mapping(self) -> Dict[str, Any]:
        """
        Define the Elasticsearch mapping for movie documents.
        
        Returns:
            Dictionary containing the mapping configuration
        """
        return {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        },
                        "autocomplete": {
                            "type": "text",
                            "analyzer": "autocomplete",
                            "search_analyzer": "standard"
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
                "release_year": {
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
                "actors": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "duration_minutes": {
                    "type": "integer"
                },
                "box_office": {
                    "type": "long"
                }
            }
        }
    
    def get_index_settings(self) -> Dict[str, Any]:
        """
        Define index settings including analyzers for autocomplete.
        
        Returns:
            Dictionary containing index settings
        """
        return {
            "analysis": {
                "analyzer": {
                    "autocomplete": {
                        "tokenizer": "autocomplete",
                        "filter": ["lowercase"]
                    }
                },
                "tokenizer": {
                    "autocomplete": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 10,
                        "token_chars": ["letter", "digit"]
                    }
                }
            }
        }
    
    def create_sample_movies(self) -> List[Dict[str, Any]]:
        """
        Create a comprehensive sample dataset of movies.
        
        Returns:
            List of movie dictionaries with various genres and years
        """
        movies = [
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "genres": ["Action", "Crime", "Drama"],
                "release_year": 2008,
                "rating": 9.0,
                "director": "Christopher Nolan",
                "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
                "duration_minutes": 152,
                "box_office": 1004558444
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "genres": ["Action", "Sci-Fi", "Thriller"],
                "release_year": 2010,
                "rating": 8.8,
                "director": "Christopher Nolan",
                "actors": ["Leonardo DiCaprio", "Marion Cotillard", "Tom Hardy"],
                "duration_minutes": 148,
                "box_office": 836836967
            },
            {
                "title": "The Shawshank Redemption",
                "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "genres": ["Drama"],
                "release_year": 1994,
                "rating": 9.3,
                "director": "Frank Darabont",
                "actors": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
                "duration_minutes": 142,
                "box_office": 16000000
            },
            {
                "title": "Pulp Fiction",
                "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "genres": ["Crime", "Drama"],
                "release_year": 1994,
                "rating": 8.9,
                "director": "Quentin Tarantino",
                "actors": ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
                "duration_minutes": 154,
                "box_office": 214179088
            },
            {
                "title": "The Matrix",
                "description": "A computer programmer is led to fight an underground war against powerful computers who have constructed his entire reality with a system called the Matrix.",
                "genres": ["Action", "Sci-Fi"],
                "release_year": 1999,
                "rating": 8.7,
                "director": "The Wachowski Brothers",
                "actors": ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
                "duration_minutes": 136,
                "box_office": 467222824
            },
            {
                "title": "Forrest Gump",
                "description": "The presidencies of Kennedy and Johnson, Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75.",
                "genres": ["Drama", "Romance"],
                "release_year": 1994,
                "rating": 8.8,
                "director": "Robert Zemeckis",
                "actors": ["Tom Hanks", "Robin Wright", "Gary Sinise"],
                "duration_minutes": 142,
                "box_office": 677387716
            },
            {
                "title": "The Lord of the Rings: The Fellowship of the Ring",
                "description": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
                "genres": ["Adventure", "Drama", "Fantasy"],
                "release_year": 2001,
                "rating": 8.8,
                "director": "Peter Jackson",
                "actors": ["Elijah Wood", "Ian McKellen", "Orlando Bloom"],
                "duration_minutes": 178,
                "box_office": 871530324
            },
            {
                "title": "Spider-Man: Into the Spider-Verse",
                "description": "Teen Miles Morales becomes Spider-Man of his reality, crossing his path with five counterparts from other dimensions to stop a threat for all realities.",
                "genres": ["Animation", "Action", "Adventure"],
                "release_year": 2018,
                "rating": 8.4,
                "director": "Bob Persichetti",
                "actors": ["Shameik Moore", "Jake Johnson", "Hailee Steinfeld"],
                "duration_minutes": 117,
                "box_office": 375540831
            },
            {
                "title": "Parasite",
                "description": "A poor family schemes to become employed by a wealthy family by infiltrating their household and posing as unrelated, highly qualified individuals.",
                "genres": ["Comedy", "Drama", "Thriller"],
                "release_year": 2019,
                "rating": 8.6,
                "director": "Bong Joon Ho",
                "actors": ["Kang-ho Song", "Sun-kyun Lee", "Yeo-jeong Jo"],
                "duration_minutes": 132,
                "box_office": 258540436
            },
            {
                "title": "Avengers: Endgame",
                "description": "After the devastating events of Infinity War, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
                "genres": ["Action", "Adventure", "Drama"],
                "release_year": 2019,
                "rating": 8.4,
                "director": "Anthony Russo",
                "actors": ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
                "duration_minutes": 181,
                "box_office": 2797800564
            },
            {
                "title": "Joker",
                "description": "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime.",
                "genres": ["Crime", "Drama", "Thriller"],
                "release_year": 2019,
                "rating": 8.4,
                "director": "Todd Phillips",
                "actors": ["Joaquin Phoenix", "Robert De Niro", "Zazie Beetz"],
                "duration_minutes": 122,
                "box_office": 1074251311
            },
            {
                "title": "Mad Max: Fury Road",
                "description": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners.",
                "genres": ["Action", "Adventure", "Sci-Fi"],
                "release_year": 2015,
                "rating": 8.1,
                "director": "George Miller",
                "actors": ["Tom Hardy", "Charlize Theron", "Nicholas Hoult"],
                "duration_minutes": 120,
                "box_office": 374632194
            },
            {
                "title": "Toy Story",
                "description": "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.",
                "genres": ["Animation", "Adventure", "Comedy"],
                "release_year": 1995,
                "rating": 8.3,
                "director": "John Lasseter",
                "actors": ["Tom Hanks", "Tim Allen", "Don Rickles"],
                "duration_minutes": 81,
                "box_office": 373554033
            },
            {
                "title": "Blade Runner 2049",
                "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
                "genres": ["Action", "Drama", "Mystery"],
                "release_year": 2017,
                "rating": 8.0,
                "director": "Denis Villeneuve",
                "actors": ["Ryan Gosling", "Harrison Ford", "Ana de Armas"],
                "duration_minutes": 164,
                "box_office": 259239658
            },
            {
                "title": "The Grand Budapest Hotel",
                "description": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.",
                "genres": ["Adventure", "Comedy", "Crime"],
                "release_year": 2014,
                "rating": 8.1,
                "director": "Wes Anderson",
                "actors": ["Ralph Fiennes", "F. Murray Abraham", "Mathieu Amalric"],
                "duration_minutes": 99,
                "box_office": 172915324
            }
        ]
        
        return movies
    
    def save_sample_data(self, movies: List[Dict[str, Any]], filename: str = 'movies.json') -> str:
        """
        Save movie data to a JSON file.
        
        Args:
            movies: List of movie dictionaries
            filename: Name of the file to save
            
        Returns:
            Path to the saved file
        """
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        file_path = os.path.join(data_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(movies)} movies to {file_path}")
        return file_path
    
    def prepare_bulk_data(self, movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prepare movie data for bulk indexing.
        
        Args:
            movies: List of movie dictionaries
            
        Returns:
            List of documents formatted for Elasticsearch bulk API
        """
        bulk_data = []
        
        for i, movie in enumerate(movies, 1):
            doc = {
                "_index": self.index_name,
                "_id": i,
                "_source": movie
            }
            bulk_data.append(doc)
        
        return bulk_data
    
    def index_movies(self, movies: List[Dict[str, Any]]) -> bool:
        """
        Index movies into Elasticsearch using bulk API.
        
        Args:
            movies: List of movie dictionaries to index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create index with mapping and settings
            index_body = {
                "settings": self.get_index_settings(),
                "mappings": self.get_movie_mapping()
            }
            
            if self.es_client.index_exists():
                print(f"Index '{self.index_name}' already exists. Deleting and recreating...")
                self.es_client.delete_index()
            
            self.client.indices.create(index=self.index_name, body=index_body)
            print(f"✅ Created index '{self.index_name}' with mapping")
            
            # Prepare and index data
            bulk_data = self.prepare_bulk_data(movies)
            
            success, failed = bulk(
                self.client,
                bulk_data,
                index=self.index_name,
                chunk_size=100,
                request_timeout=60
            )
            
            print(f"✅ Successfully indexed {success} movies")
            if failed:
                print(f"❌ Failed to index {len(failed)} movies")
                for failure in failed[:5]:  # Show first 5 failures
                    print(f"  - {failure}")
            
            # Refresh index to make documents searchable
            self.client.indices.refresh(index=self.index_name)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to index movies: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the indexed data.
        
        Returns:
            Dictionary containing index statistics
        """
        try:
            stats = self.client.indices.stats(index=self.index_name)
            doc_count = stats['indices'][self.index_name]['total']['docs']['count']
            size_in_bytes = stats['indices'][self.index_name]['total']['store']['size_in_bytes']
            
            return {
                'document_count': doc_count,
                'index_size_bytes': size_in_bytes,
                'index_size_mb': round(size_in_bytes / (1024 * 1024), 2)
            }
        except Exception as e:
            return {'error': str(e)}


def main():
    """
    Main function to run the data indexing process.
    """
    print("🎬 Starting Movie Data Indexer...")
    
    try:
        # Initialize indexer
        indexer = MovieDataIndexer()
        
        # Create sample movie data
        movies = indexer.create_sample_movies()
        print(f"📊 Created {len(movies)} sample movies")
        
        # Save to file
        file_path = indexer.save_sample_data(movies)
        
        # Index movies
        success = indexer.index_movies(movies)
        
        if success:
            # Show statistics
            stats = indexer.get_index_stats()
            print(f"📈 Index Statistics:")
            print(f"   - Documents: {stats.get('document_count', 'N/A')}")
            print(f"   - Size: {stats.get('index_size_mb', 'N/A')} MB")
            print("🎉 Data indexing completed successfully!")
        else:
            print("❌ Data indexing failed!")
            
    except Exception as e:
        print(f"❌ Error during indexing process: {e}")


if __name__ == "__main__":
    main()
