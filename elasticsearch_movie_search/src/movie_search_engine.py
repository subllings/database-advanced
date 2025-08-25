"""
Movie Search Engine with Elasticsearch.

This module provides the main search functionality for the movie database,
including full-text search, filtering, sorting, and aggregations.
"""

from typing import Dict, List, Any, Optional, Union
from .elasticsearch_client import ElasticsearchClient


class MovieSearchEngine:
    """
    Main search engine for movie database.
    
    Provides comprehensive search functionality including:
    - Full-text search across titles and descriptions
    - Multi-field filtering (genre, year, rating, etc.)
    - Sorting by various criteria
    - Aggregations for statistics
    - "More like this" similarity search
    """
    
    def __init__(self):
        """Initialize the search engine with Elasticsearch client."""
        self.es_client = ElasticsearchClient()
        self.client = self.es_client.get_client()
        self.index_name = self.es_client.get_index_name()
    
    def search_movies(
        self,
        query: Optional[str] = None,
        genre: Optional[str] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        director: Optional[str] = None,
        sort_by: str = "relevance",
        sort_order: str = "desc",
        size: int = 10,
        from_: int = 0
    ) -> Dict[str, Any]:
        """
        Search movies with comprehensive filtering and sorting options.
        
        Args:
            query: Search query for title and description
            genre: Filter by specific genre
            min_year: Minimum release year
            max_year: Maximum release year
            min_rating: Minimum rating (0-10)
            max_rating: Maximum rating (0-10)
            director: Filter by director name
            sort_by: Sort field (relevance, rating, release_year, title)
            sort_order: Sort order (asc, desc)
            size: Number of results to return
            from_: Starting position for pagination
            
        Returns:
            Dictionary containing search results and metadata
        """
        try:
            # Build the query
            search_body = self._build_search_query(
                query, genre, min_year, max_year, min_rating, max_rating, director
            )
            
            # Add sorting
            if sort_by != "relevance":
                search_body["sort"] = self._build_sort_clause(sort_by, sort_order)
            
            # Add pagination
            search_body["size"] = size
            search_body["from"] = from_
            
            # Add highlighting
            search_body["highlight"] = {
                "fields": {
                    "title": {},
                    "description": {"fragment_size": 200}
                }
            }
            
            # Execute search
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            return self._format_search_response(response)
            
        except Exception as e:
            return {
                "error": f"Search failed: {str(e)}",
                "results": [],
                "total": 0,
                "took": 0
            }
    
    def _build_search_query(
        self,
        query: Optional[str],
        genre: Optional[str],
        min_year: Optional[int],
        max_year: Optional[int],
        min_rating: Optional[float],
        max_rating: Optional[float],
        director: Optional[str]
    ) -> Dict[str, Any]:
        """
        Build Elasticsearch query with filters.
        
        Returns:
            Dictionary containing the complete query structure
        """
        search_body = {"query": {"bool": {"must": [], "filter": []}}}
        
        # Text search
        if query:
            search_body["query"]["bool"]["must"].append({
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "description", "actors", "director"],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        else:
            search_body["query"]["bool"]["must"].append({"match_all": {}})
        
        # Genre filter
        if genre:
            search_body["query"]["bool"]["filter"].append({
                "term": {"genres": genre}
            })
        
        # Year range filter
        year_filter = {}
        if min_year:
            year_filter["gte"] = min_year
        if max_year:
            year_filter["lte"] = max_year
        
        if year_filter:
            search_body["query"]["bool"]["filter"].append({
                "range": {"release_year": year_filter}
            })
        
        # Rating range filter
        rating_filter = {}
        if min_rating:
            rating_filter["gte"] = min_rating
        if max_rating:
            rating_filter["lte"] = max_rating
        
        if rating_filter:
            search_body["query"]["bool"]["filter"].append({
                "range": {"rating": rating_filter}
            })
        
        # Director filter
        if director:
            search_body["query"]["bool"]["filter"].append({
                "match": {"director.keyword": director}
            })
        
        return search_body
    
    def _build_sort_clause(self, sort_by: str, sort_order: str) -> List[Dict[str, Any]]:
        """
        Build sorting clause for the query.
        
        Args:
            sort_by: Field to sort by
            sort_order: Sort order (asc/desc)
            
        Returns:
            List containing sort configuration
        """
        sort_mapping = {
            "rating": "rating",
            "release_year": "release_year",
            "title": "title.keyword"
        }
        
        field = sort_mapping.get(sort_by, "rating")
        return [{field: {"order": sort_order}}]
    
    def _format_search_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format Elasticsearch response for easier consumption.
        
        Args:
            response: Raw Elasticsearch response
            
        Returns:
            Formatted response with results and metadata
        """
        hits = response.get("hits", {})
        
        results = []
        for hit in hits.get("hits", []):
            movie = hit["_source"]
            movie["id"] = hit["_id"]
            movie["score"] = hit["_score"]
            
            # Add highlights if available
            if "highlight" in hit:
                movie["highlights"] = hit["highlight"]
            
            results.append(movie)
        
        return {
            "results": results,
            "total": hits.get("total", {}).get("value", 0),
            "took": response.get("took", 0),
            "max_score": hits.get("max_score", 0)
        }
    
    def find_similar_movies(self, movie_id: Union[str, int], size: int = 5) -> Dict[str, Any]:
        """
        Find movies similar to a given movie using "more like this" query.
        
        Args:
            movie_id: ID of the reference movie
            size: Number of similar movies to return
            
        Returns:
            Dictionary containing similar movies
        """
        try:
            search_body = {
                "query": {
                    "more_like_this": {
                        "fields": ["title", "description", "genres", "director"],
                        "like": [
                            {
                                "_index": self.index_name,
                                "_id": movie_id
                            }
                        ],
                        "min_term_freq": 1,
                        "max_query_terms": 12,
                        "min_doc_freq": 1
                    }
                },
                "size": size
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            return self._format_search_response(response)
            
        except Exception as e:
            return {
                "error": f"Similar search failed: {str(e)}",
                "results": [],
                "total": 0
            }
    
    def autocomplete_movies(self, query: str, size: int = 10) -> List[str]:
        """
        Provide autocomplete suggestions for movie titles.
        
        Args:
            query: Partial query string
            size: Number of suggestions to return
            
        Returns:
            List of movie title suggestions
        """
        try:
            search_body = {
                "query": {
                    "match": {
                        "title.autocomplete": {
                            "query": query,
                            "operator": "and"
                        }
                    }
                },
                "_source": ["title"],
                "size": size
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            suggestions = []
            for hit in response["hits"]["hits"]:
                suggestions.append(hit["_source"]["title"])
            
            return suggestions
            
        except Exception:
            return []
    
    def get_movie_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the movie database.
        
        Returns:
            Dictionary containing various statistics and aggregations
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "avg_rating": {
                        "avg": {"field": "rating"}
                    },
                    "total_movies": {
                        "value_count": {"field": "title.keyword"}
                    },
                    "genres": {
                        "terms": {
                            "field": "genres",
                            "size": 20
                        }
                    },
                    "movies_by_year": {
                        "date_histogram": {
                            "field": "release_year",
                            "calendar_interval": "year",
                            "format": "yyyy"
                        }
                    },
                    "top_directors": {
                        "terms": {
                            "field": "director.keyword",
                            "size": 10
                        }
                    },
                    "rating_distribution": {
                        "histogram": {
                            "field": "rating",
                            "interval": 1
                        }
                    },
                    "box_office_stats": {
                        "stats": {"field": "box_office"}
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            aggs = response.get("aggregations", {})
            
            return {
                "total_movies": aggs.get("total_movies", {}).get("value", 0),
                "avg_rating": round(aggs.get("avg_rating", {}).get("value", 0), 2),
                "genres": [
                    {
                        "genre": bucket["key"],
                        "count": bucket["doc_count"]
                    }
                    for bucket in aggs.get("genres", {}).get("buckets", [])
                ],
                "movies_by_year": [
                    {
                        "year": bucket["key_as_string"],
                        "count": bucket["doc_count"]
                    }
                    for bucket in aggs.get("movies_by_year", {}).get("buckets", [])
                ],
                "top_directors": [
                    {
                        "director": bucket["key"],
                        "movies": bucket["doc_count"]
                    }
                    for bucket in aggs.get("top_directors", {}).get("buckets", [])
                ],
                "rating_distribution": [
                    {
                        "rating_range": f"{bucket['key']}-{bucket['key'] + 1}",
                        "count": bucket["doc_count"]
                    }
                    for bucket in aggs.get("rating_distribution", {}).get("buckets", [])
                ],
                "box_office_stats": aggs.get("box_office_stats", {})
            }
            
        except Exception as e:
            return {"error": f"Statistics failed: {str(e)}"}
    
    def get_movie_by_id(self, movie_id: Union[str, int]) -> Dict[str, Any]:
        """
        Get a specific movie by its ID.
        
        Args:
            movie_id: ID of the movie to retrieve
            
        Returns:
            Dictionary containing movie details or error
        """
        try:
            response = self.client.get(
                index=self.index_name,
                id=movie_id
            )
            
            movie = response["_source"]
            movie["id"] = response["_id"]
            
            return movie
            
        except Exception as e:
            return {"error": f"Movie not found: {str(e)}"}
    
    def advanced_search(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform advanced search with custom parameters.
        
        Args:
            search_params: Dictionary containing advanced search parameters
            
        Returns:
            Search results with advanced filtering and boosting
        """
        try:
            # Build advanced query with boosting
            query = {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "title": {
                                    "query": search_params.get("query", ""),
                                    "boost": 3.0
                                }
                            }
                        },
                        {
                            "match": {
                                "description": {
                                    "query": search_params.get("query", ""),
                                    "boost": 1.0
                                }
                            }
                        },
                        {
                            "match": {
                                "actors": {
                                    "query": search_params.get("query", ""),
                                    "boost": 2.0
                                }
                            }
                        }
                    ],
                    "minimum_should_match": 1,
                    "filter": []
                }
            }
            
            # Add filters based on search parameters
            filters = []
            
            if search_params.get("genres"):
                filters.append({
                    "terms": {"genres": search_params["genres"]}
                })
            
            if search_params.get("year_range"):
                year_range = search_params["year_range"]
                filters.append({
                    "range": {
                        "release_year": {
                            "gte": year_range.get("min", 1900),
                            "lte": year_range.get("max", 2024)
                        }
                    }
                })
            
            if search_params.get("rating_range"):
                rating_range = search_params["rating_range"]
                filters.append({
                    "range": {
                        "rating": {
                            "gte": rating_range.get("min", 0),
                            "lte": rating_range.get("max", 10)
                        }
                    }
                })
            
            query["bool"]["filter"] = filters
            
            search_body = {
                "query": query,
                "size": search_params.get("size", 10),
                "from": search_params.get("from", 0)
            }
            
            # Add sorting if specified
            if search_params.get("sort"):
                search_body["sort"] = search_params["sort"]
            
            response = self.client.search(
                index=self.index_name,
                body=search_body
            )
            
            return self._format_search_response(response)
            
        except Exception as e:
            return {
                "error": f"Advanced search failed: {str(e)}",
                "results": [],
                "total": 0
            }
