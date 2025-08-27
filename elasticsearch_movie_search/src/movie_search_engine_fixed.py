"""
Movie search engine using Elasticsearch.

This module provides search functionality for movies including
text search, filtering, and aggregations.
"""

from typing import Dict, List, Any, Optional
from elasticsearch import Elasticsearch
from src.elasticsearch_client import ElasticsearchClient


class MovieSearchEngine:
    """
    Movie search engine for Elasticsearch.
    
    Provides various search methods including text search,
    filtering, and aggregations.
    """

    def __init__(self, es_client: Optional[ElasticsearchClient] = None):
        """
        Initialize the movie search engine.
        
        Args:
            es_client: Elasticsearch client instance
        """
        self.es_client = es_client or ElasticsearchClient()
        self.client = self.es_client.client
        self.index_name = self.es_client.index_name

    def search_movies(self, query: str = "", 
                     filters: Optional[Dict[str, Any]] = None,
                     size: int = 10,
                     sort_by: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for movies with optional filters and sorting.
        
        Args:
            query: Search query string
            filters: Dictionary of filters to apply
            size: Maximum number of results to return
            sort_by: Field to sort by
            
        Returns:
            Dictionary containing search results
        """
        try:
            # Build the search body
            search_body = {
                "size": size
            }
            
            # Build query
            if query:
                search_body["query"] = {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "description^2", "director", "cast"],
                        "type": "best_fields",
                        "fuzziness": "AUTO"
                    }
                }
            else:
                search_body["query"] = {"match_all": {}}
            
            # Apply filters
            if filters:
                filter_clauses = []
                
                # Year filters
                if 'year_from' in filters or 'year_to' in filters:
                    year_range = {}
                    if 'year_from' in filters:
                        year_range['gte'] = filters['year_from']
                    if 'year_to' in filters:
                        year_range['lte'] = filters['year_to']
                    filter_clauses.append({"range": {"year": year_range}})
                
                # Rating filters
                if 'rating_from' in filters or 'rating_to' in filters:
                    rating_range = {}
                    if 'rating_from' in filters:
                        rating_range['gte'] = filters['rating_from']
                    if 'rating_to' in filters:
                        rating_range['lte'] = filters['rating_to']
                    filter_clauses.append({"range": {"rating": rating_range}})
                
                # Genre filter
                if 'genres' in filters and filters['genres']:
                    filter_clauses.append({"terms": {"genres": filters['genres']}})
                
                # Director filter
                if 'director' in filters and filters['director']:
                    filter_clauses.append({"match": {"director": filters['director']}})
                
                # Apply filters using bool query
                if filter_clauses:
                    if query:
                        search_body["query"] = {
                            "bool": {
                                "must": search_body["query"],
                                "filter": filter_clauses
                            }
                        }
                    else:
                        search_body["query"] = {
                            "bool": {
                                "filter": filter_clauses
                            }
                        }
            
            # Add sorting
            if sort_by:
                if sort_by == "rating":
                    search_body["sort"] = [{"rating": {"order": "desc"}}]
                elif sort_by == "year":
                    search_body["sort"] = [{"year": {"order": "desc"}}]
                elif sort_by == "title":
                    search_body["sort"] = [{"title.keyword": {"order": "asc"}}]
            
            # Execute search
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            return response
            
        except Exception as e:
            print(f"Search error: {e}")
            return {"hits": {"hits": [], "total": {"value": 0}}}

    def get_movie_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific movie by ID.
        
        Args:
            movie_id: The movie document ID
            
        Returns:
            Movie document or None if not found
        """
        try:
            response = self.client.get(
                index=self.index_name,
                id=movie_id
            )
            return response['_source']
            
        except Exception as e:
            print(f"Error getting movie by ID: {e}")
            return None

    def get_movies_by_genre(self, genre: str, size: int = 10) -> Dict[str, Any]:
        """
        Get movies by genre.
        
        Args:
            genre: Genre to search for
            size: Maximum number of results
            
        Returns:
            Search results
        """
        return self.search_movies(
            filters={'genres': [genre]},
            size=size,
            sort_by="rating"
        )

    def get_movies_by_director(self, director: str, size: int = 10) -> Dict[str, Any]:
        """
        Get movies by director.
        
        Args:
            director: Director name to search for
            size: Maximum number of results
            
        Returns:
            Search results
        """
        return self.search_movies(
            query=director,
            size=size,
            sort_by="year"
        )

    def get_top_rated_movies(self, min_rating: float = 8.0, size: int = 10) -> Dict[str, Any]:
        """
        Get top rated movies.
        
        Args:
            min_rating: Minimum rating threshold
            size: Maximum number of results
            
        Returns:
            Search results
        """
        return self.search_movies(
            filters={'rating_from': min_rating},
            size=size,
            sort_by="rating"
        )

    def search_movies_by_year_range(self, year_from: int, year_to: int, 
                                   size: int = 10) -> Dict[str, Any]:
        """
        Search movies within a year range.
        
        Args:
            year_from: Starting year
            year_to: Ending year
            size: Maximum number of results
            
        Returns:
            Search results
        """
        return self.search_movies(
            filters={
                'year_from': year_from,
                'year_to': year_to
            },
            size=size,
            sort_by="year"
        )

    def get_movie_suggestions(self, partial_title: str) -> List[str]:
        """
        Get movie title suggestions for autocomplete.
        
        Args:
            partial_title: Partial movie title
            
        Returns:
            List of suggested titles
        """
        try:
            search_body = {
                "size": 10,
                "_source": ["title"],
                "query": {
                    "match_phrase_prefix": {
                        "title": partial_title
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            suggestions = []
            for hit in response['hits']['hits']:
                suggestions.append(hit['_source']['title'])
            
            return suggestions
            
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            return []

    def get_genre_aggregation(self) -> Dict[str, int]:
        """
        Get genre distribution across all movies.
        
        Returns:
            Dictionary with genre counts
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "genres": {
                        "terms": {
                            "field": "genres",
                            "size": 50
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            genre_counts = {}
            if 'aggregations' in response:
                for bucket in response['aggregations']['genres']['buckets']:
                    genre_counts[bucket['key']] = bucket['doc_count']
            
            return genre_counts
            
        except Exception as e:
            print(f"Error getting genre aggregation: {e}")
            return {}

    def get_rating_statistics(self) -> Dict[str, float]:
        """
        Get rating statistics across all movies.
        
        Returns:
            Dictionary with rating statistics
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "rating_stats": {
                        "stats": {
                            "field": "rating"
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            if 'aggregations' in response:
                stats = response['aggregations']['rating_stats']
                return {
                    'min': stats['min'],
                    'max': stats['max'],
                    'avg': stats['avg'],
                    'count': stats['count']
                }
            
            return {}
            
        except Exception as e:
            print(f"Error getting rating statistics: {e}")
            return {}
