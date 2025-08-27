"""
Movie search engine - Simple working version
"""

from typing import Dict, List, Any, Optional
from src.elasticsearch_client import ElasticsearchClient


class MovieSearchEngine:
    """Simple movie search engine for Elasticsearch."""

    def __init__(self, es_client: Optional[ElasticsearchClient] = None):
        """Initialize the movie search engine."""
        self.es_client = es_client or ElasticsearchClient()
        self.client = self.es_client.client
        self.index_name = self.es_client.index_name

    def search_movies(self, query: str = "", 
                     filters: Optional[Dict[str, Any]] = None,
                     size: int = 10) -> Dict[str, Any]:
        """Search for movies."""
        try:
            search_params = {
                "index": self.index_name,
                "size": size
            }
            
            if query:
                search_params["query"] = {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "description^2", "director", "cast"]
                    }
                }
            else:
                search_params["query"] = {"match_all": {}}
            
            # Apply filters
            if filters:
                filter_clauses = []
                
                if 'year_from' in filters:
                    filter_clauses.append({"range": {"year": {"gte": filters['year_from']}}})
                if 'year_to' in filters:
                    filter_clauses.append({"range": {"year": {"lte": filters['year_to']}}})
                if 'rating_from' in filters:
                    filter_clauses.append({"range": {"rating": {"gte": filters['rating_from']}}})
                if 'genres' in filters and filters['genres']:
                    filter_clauses.append({"terms": {"genres": filters['genres']}})
                
                if filter_clauses:
                    if query:
                        search_params["query"] = {
                            "bool": {
                                "must": search_params["query"],
                                "filter": filter_clauses
                            }
                        }
                    else:
                        search_params["query"] = {
                            "bool": {"filter": filter_clauses}
                        }
            
            response = self.client.search(**search_params)
            return response
            
        except Exception as e:
            print(f"Search error: {e}")
            return {"hits": {"hits": [], "total": {"value": 0}}}

    def get_genre_aggregation(self) -> Dict[str, int]:
        """Get genre distribution."""
        try:
            response = self.client.search(
                index=self.index_name,
                size=0,
                aggs={
                    "genres": {
                        "terms": {
                            "field": "genres",
                            "size": 50
                        }
                    }
                }
            )
            
            genre_counts = {}
            if 'aggregations' in response:
                for bucket in response['aggregations']['genres']['buckets']:
                    genre_counts[bucket['key']] = bucket['doc_count']
            
            return genre_counts
            
        except Exception as e:
            print(f"Error getting genres: {e}")
            return {}

    def get_rating_statistics(self) -> Dict[str, float]:
        """Get rating statistics."""
        try:
            response = self.client.search(
                index=self.index_name,
                size=0,
                aggs={
                    "rating_stats": {
                        "stats": {
                            "field": "rating"
                        }
                    }
                }
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
            print(f"Error getting statistics: {e}")
            return {}

    def get_top_rated_movies(self, min_rating: float = 8.0, size: int = 10) -> Dict[str, Any]:
        """Get top rated movies."""
        return self.search_movies(
            filters={'rating_from': min_rating},
            size=size
        )

    def search_movies_by_year_range(self, year_from: int, year_to: int, size: int = 10) -> Dict[str, Any]:
        """Search movies by year range."""
        return self.search_movies(
            filters={'year_from': year_from, 'year_to': year_to},
            size=size
        )
