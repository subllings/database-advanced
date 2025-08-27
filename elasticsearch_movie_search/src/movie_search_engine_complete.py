"""
Complete Movie Search Engine using Elasticsearch.

This module provides comprehensive search functionality for movies including:
- Full-text search across titles and descriptions
- Multi-field filtering (genre, year, rating, etc.)
- Sorting by various criteria
- Advanced features like autocomplete, "more like this", and vector search
- Aggregations for analytics
"""

from typing import Dict, List, Any, Optional, Union
from elasticsearch import Elasticsearch
from src.elasticsearch_client import ElasticsearchClient


class MovieSearchEngine:
    """
    Complete Movie Search Engine for Elasticsearch.

    Provides comprehensive search functionality including:
    - Full-text search across titles and descriptions
    - Multi-field filtering (genre, year, rating, etc.)
    - Sorting by various criteria (rating, popularity, year)
    - Advanced features like autocomplete and "more like this"
    - Aggregations for analytics and insights
    - Vector search capabilities for semantic similarity
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

    def search_movies(self, 
                     query: str = "", 
                     filters: Optional[Dict[str, Any]] = None,
                     size: int = 10,
                     from_: int = 0,
                     sort_by: Optional[str] = None,
                     sort_order: str = "desc",
                     highlight: bool = True) -> Dict[str, Any]:
        """
        Advanced movie search with full-text search, filtering, and sorting.
        
        Args:
            query: Search query string for title/description
            filters: Dictionary of filters (genre, year, rating, etc.)
            size: Number of results to return
            from_: Starting position for pagination
            sort_by: Field to sort by (rating, year, popularity, title)
            sort_order: Sort order (asc/desc)
            highlight: Whether to highlight matching terms
            
        Returns:
            Dictionary containing search results with metadata
        """
        try:
            search_body = {
                "size": size,
                "from": from_,
                "track_total_hits": True
            }
            
            # Build query
            if query.strip():
                search_body["query"] = {
                    "bool": {
                        "should": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "title^3",
                                        "title.keyword^2", 
                                        "description^2",
                                        "director^1.5",
                                        "cast^1.2"
                                    ],
                                    "type": "best_fields",
                                    "fuzziness": "AUTO",
                                    "prefix_length": 2
                                }
                            },
                            {
                                "match_phrase": {
                                    "title": {
                                        "query": query,
                                        "boost": 5
                                    }
                                }
                            }
                        ],
                        "minimum_should_match": 1
                    }
                }
            else:
                search_body["query"] = {"match_all": {}}
            
            # Apply filters
            filter_clauses = []
            if filters:
                # Year range filter
                if 'year_from' in filters or 'year_to' in filters:
                    year_range = {}
                    if 'year_from' in filters:
                        year_range['gte'] = filters['year_from']
                    if 'year_to' in filters:
                        year_range['lte'] = filters['year_to']
                    filter_clauses.append({"range": {"year": year_range}})
                
                # Specific year filter
                if 'year' in filters:
                    filter_clauses.append({"term": {"year": filters['year']}})
                
                # Rating range filter
                if 'rating_from' in filters or 'rating_to' in filters:
                    rating_range = {}
                    if 'rating_from' in filters:
                        rating_range['gte'] = filters['rating_from']
                    if 'rating_to' in filters:
                        rating_range['lte'] = filters['rating_to']
                    filter_clauses.append({"range": {"rating": rating_range}})
                
                # Genre filter (supports multiple genres)
                if 'genres' in filters and filters['genres']:
                    genres = filters['genres'] if isinstance(filters['genres'], list) else [filters['genres']]
                    filter_clauses.append({"terms": {"genres": genres}})
                
                # Director filter
                if 'director' in filters and filters['director']:
                    filter_clauses.append({
                        "match_phrase": {
                            "director": {
                                "query": filters['director'],
                                "slop": 1
                            }
                        }
                    })
                
                # Country filter
                if 'country' in filters and filters['country']:
                    filter_clauses.append({"term": {"country": filters['country']}})
                
                # Language filter
                if 'language' in filters and filters['language']:
                    filter_clauses.append({"term": {"language": filters['language']}})
                
                # Duration range filter
                if 'duration_from' in filters or 'duration_to' in filters:
                    duration_range = {}
                    if 'duration_from' in filters:
                        duration_range['gte'] = filters['duration_from']
                    if 'duration_to' in filters:
                        duration_range['lte'] = filters['duration_to']
                    filter_clauses.append({"range": {"duration": duration_range}})
            
            # Apply filters to query
            if filter_clauses:
                if "bool" in search_body["query"]:
                    search_body["query"]["bool"]["filter"] = filter_clauses
                else:
                    search_body["query"] = {
                        "bool": {
                            "must": search_body["query"],
                            "filter": filter_clauses
                        }
                    }
            
            # Add sorting
            if sort_by:
                sort_field = sort_by
                if sort_by == "title":
                    sort_field = "title.keyword"
                elif sort_by == "popularity":
                    sort_field = "box_office"
                elif sort_by == "director":
                    sort_field = "director.keyword"
                
                search_body["sort"] = [{sort_field: {"order": sort_order}}]
                
                # Add secondary sort by relevance score if searching
                if query.strip():
                    search_body["sort"].append({"_score": {"order": "desc"}})
            elif query.strip():
                # Default sort by relevance for searches
                search_body["sort"] = [{"_score": {"order": "desc"}}]
            else:
                # Default sort by rating for browse
                search_body["sort"] = [{"rating": {"order": "desc"}}]
            
            # Add highlighting
            if highlight and query.strip():
                search_body["highlight"] = {
                    "fields": {
                        "title": {
                            "pre_tags": ["<mark>"],
                            "post_tags": ["</mark>"],
                            "fragment_size": 150,
                            "number_of_fragments": 1
                        },
                        "description": {
                            "pre_tags": ["<mark>"],
                            "post_tags": ["</mark>"],
                            "fragment_size": 200,
                            "number_of_fragments": 2
                        }
                    }
                }
            
            # Execute search
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            # Enhance response with metadata
            enhanced_response = {
                "hits": response["hits"],
                "search_metadata": {
                    "query": query,
                    "filters_applied": filters or {},
                    "total_results": response["hits"]["total"]["value"],
                    "search_time_ms": response["took"],
                    "max_score": response["hits"]["max_score"]
                }
            }
            
            return enhanced_response
            
        except Exception as e:
            print(f"Search error: {e}")
            return {
                "hits": {"hits": [], "total": {"value": 0}},
                "search_metadata": {
                    "query": query,
                    "error": str(e)
                }
            }

    def get_movie_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific movie by document ID.
        
        Args:
            movie_id: The Elasticsearch document ID
            
        Returns:
            Movie document or None if not found
        """
        try:
            response = self.client.get(
                index=self.index_name,
                id=movie_id
            )
            return {
                "id": response["_id"],
                "source": response["_source"]
            }
        except Exception as e:
            print(f"Error getting movie by ID {movie_id}: {e}")
            return None

    def get_similar_movies(self, movie_id: str, size: int = 5) -> Dict[str, Any]:
        """
        Find movies similar to a given movie using "More Like This" query.
        
        Args:
            movie_id: ID of the reference movie
            size: Number of similar movies to return
            
        Returns:
            Search results with similar movies
        """
        try:
            search_body = {
                "size": size,
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
                        "min_doc_freq": 1,
                        "minimum_should_match": "30%"
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            return response
            
        except Exception as e:
            print(f"Error finding similar movies: {e}")
            return {"hits": {"hits": [], "total": {"value": 0}}}

    def get_movie_autocomplete(self, partial_title: str, size: int = 10) -> List[Dict[str, Any]]:
        """
        Get movie title suggestions for autocomplete functionality.
        
        Args:
            partial_title: Partial movie title entered by user
            size: Maximum number of suggestions
            
        Returns:
            List of suggested movie titles with metadata
        """
        try:
            search_body = {
                "size": size,
                "_source": ["title", "year", "rating", "genres"],
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match_phrase_prefix": {
                                    "title": {
                                        "query": partial_title,
                                        "boost": 3
                                    }
                                }
                            },
                            {
                                "match": {
                                    "title": {
                                        "query": partial_title,
                                        "fuzziness": "AUTO",
                                        "boost": 1
                                    }
                                }
                            }
                        ]
                    }
                },
                "sort": [
                    {"_score": {"order": "desc"}},
                    {"rating": {"order": "desc"}}
                ]
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            suggestions = []
            for hit in response["hits"]["hits"]:
                suggestion = {
                    "id": hit["_id"],
                    "title": hit["_source"]["title"],
                    "year": hit["_source"].get("year"),
                    "rating": hit["_source"].get("rating"),
                    "genres": hit["_source"].get("genres", []),
                    "score": hit["_score"]
                }
                suggestions.append(suggestion)
            
            return suggestions
            
        except Exception as e:
            print(f"Error getting autocomplete suggestions: {e}")
            return []

    def get_movies_by_genre(self, genre: str, size: int = 20, sort_by: str = "rating") -> Dict[str, Any]:
        """
        Get movies filtered by specific genre.
        
        Args:
            genre: Genre to filter by
            size: Maximum number of results
            sort_by: Sort field (rating, year, title)
            
        Returns:
            Search results for the genre
        """
        return self.search_movies(
            filters={'genres': [genre]},
            size=size,
            sort_by=sort_by
        )

    def get_movies_by_director(self, director: str, size: int = 20) -> Dict[str, Any]:
        """
        Get movies by a specific director.
        
        Args:
            director: Director name
            size: Maximum number of results
            
        Returns:
            Search results for the director
        """
        return self.search_movies(
            query=director,
            filters={'director': director},
            size=size,
            sort_by="year"
        )

    def get_top_rated_movies(self, min_rating: float = 8.0, size: int = 20) -> Dict[str, Any]:
        """
        Get top-rated movies above a threshold.
        
        Args:
            min_rating: Minimum rating threshold
            size: Maximum number of results
            
        Returns:
            Search results for top-rated movies
        """
        return self.search_movies(
            filters={'rating_from': min_rating},
            size=size,
            sort_by="rating"
        )

    def get_recent_movies(self, year_from: int = 2020, size: int = 20) -> Dict[str, Any]:
        """
        Get recent movies from a specific year onwards.
        
        Args:
            year_from: Starting year
            size: Maximum number of results
            
        Returns:
            Search results for recent movies
        """
        return self.search_movies(
            filters={'year_from': year_from},
            size=size,
            sort_by="year"
        )

    def search_movies_by_year_range(self, year_from: int, year_to: int, size: int = 20) -> Dict[str, Any]:
        """
        Search movies within a specific year range.
        
        Args:
            year_from: Starting year
            year_to: Ending year
            size: Maximum number of results
            
        Returns:
            Search results for the year range
        """
        return self.search_movies(
            filters={
                'year_from': year_from,
                'year_to': year_to
            },
            size=size,
            sort_by="year"
        )

    def get_genre_aggregation(self) -> Dict[str, Any]:
        """
        Get comprehensive genre statistics and distribution.
        
        Returns:
            Dictionary with genre counts and statistics
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "genres": {
                        "terms": {
                            "field": "genres",
                            "size": 50
                        },
                        "aggs": {
                            "avg_rating": {
                                "avg": {"field": "rating"}
                            },
                            "avg_year": {
                                "avg": {"field": "year"}
                            }
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            genre_stats = {}
            if 'aggregations' in response:
                for bucket in response['aggregations']['genres']['buckets']:
                    genre_stats[bucket['key']] = {
                        'count': bucket['doc_count'],
                        'avg_rating': round(bucket['avg_rating']['value'] or 0, 2),
                        'avg_year': round(bucket['avg_year']['value'] or 0, 1)
                    }
            
            return genre_stats
            
        except Exception as e:
            print(f"Error getting genre aggregation: {e}")
            return {}

    def get_rating_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive rating statistics across all movies.
        
        Returns:
            Dictionary with detailed rating statistics
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "rating_stats": {
                        "stats": {"field": "rating"}
                    },
                    "rating_histogram": {
                        "histogram": {
                            "field": "rating",
                            "interval": 1,
                            "min_doc_count": 1
                        }
                    },
                    "rating_percentiles": {
                        "percentiles": {
                            "field": "rating",
                            "percents": [25, 50, 75, 90, 95, 99]
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            if 'aggregations' in response:
                aggs = response['aggregations']
                return {
                    'basic_stats': {
                        'count': aggs['rating_stats']['count'],
                        'min': aggs['rating_stats']['min'],
                        'max': aggs['rating_stats']['max'],
                        'avg': round(aggs['rating_stats']['avg'], 2),
                        'sum': aggs['rating_stats']['sum']
                    },
                    'percentiles': aggs['rating_percentiles']['values'],
                    'histogram': [
                        {'rating': bucket['key'], 'count': bucket['doc_count']}
                        for bucket in aggs['rating_histogram']['buckets']
                    ]
                }
            
            return {}
            
        except Exception as e:
            print(f"Error getting rating statistics: {e}")
            return {}

    def get_year_distribution(self) -> Dict[str, Any]:
        """
        Get movie distribution by release year.
        
        Returns:
            Dictionary with year distribution data
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "years": {
                        "date_histogram": {
                            "field": "year",
                            "calendar_interval": "1y",
                            "format": "yyyy",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "avg_rating": {
                                "avg": {"field": "rating"}
                            }
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            year_data = []
            if 'aggregations' in response:
                for bucket in response['aggregations']['years']['buckets']:
                    year_data.append({
                        'year': int(bucket['key_as_string']),
                        'movie_count': bucket['doc_count'],
                        'avg_rating': round(bucket['avg_rating']['value'] or 0, 2)
                    })
            
            return {'year_distribution': year_data}
            
        except Exception as e:
            print(f"Error getting year distribution: {e}")
            return {}

    def get_director_statistics(self, min_movies: int = 2) -> Dict[str, Any]:
        """
        Get statistics about directors and their movies.
        
        Args:
            min_movies: Minimum number of movies to include director
            
        Returns:
            Dictionary with director statistics
        """
        try:
            search_body = {
                "size": 0,
                "aggs": {
                    "directors": {
                        "terms": {
                            "field": "director.keyword",
                            "size": 50,
                            "min_doc_count": min_movies
                        },
                        "aggs": {
                            "avg_rating": {
                                "avg": {"field": "rating"}
                            },
                            "total_box_office": {
                                "sum": {"field": "box_office"}
                            },
                            "movies": {
                                "top_hits": {
                                    "size": 5,
                                    "_source": ["title", "year", "rating"],
                                    "sort": [{"rating": {"order": "desc"}}]
                                }
                            }
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            director_stats = {}
            if 'aggregations' in response:
                for bucket in response['aggregations']['directors']['buckets']:
                    movies = [
                        hit['_source'] for hit in bucket['movies']['hits']['hits']
                    ]
                    
                    director_stats[bucket['key']] = {
                        'movie_count': bucket['doc_count'],
                        'avg_rating': round(bucket['avg_rating']['value'] or 0, 2),
                        'total_box_office': bucket['total_box_office']['value'] or 0,
                        'top_movies': movies
                    }
            
            return director_stats
            
        except Exception as e:
            print(f"Error getting director statistics: {e}")
            return {}

    def suggest_did_you_mean(self, query: str) -> List[str]:
        """
        Provide "did you mean" suggestions for misspelled queries.
        
        Args:
            query: Original search query
            
        Returns:
            List of suggested corrections
        """
        try:
            search_body = {
                "suggest": {
                    "title_suggestion": {
                        "text": query,
                        "term": {
                            "field": "title",
                            "size": 3,
                            "min_word_length": 3
                        }
                    }
                }
            }
            
            response = self.client.search(
                index=self.index_name,
                **search_body
            )
            
            suggestions = []
            if 'suggest' in response:
                for suggestion in response['suggest']['title_suggestion']:
                    for option in suggestion.get('options', []):
                        suggestions.append(option['text'])
            
            return list(set(suggestions))  # Remove duplicates
            
        except Exception as e:
            print(f"Error getting spelling suggestions: {e}")
            return []

    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive database statistics and insights.
        
        Returns:
            Dictionary with complete database analytics
        """
        try:
            stats = {
                'overview': {},
                'ratings': self.get_rating_statistics(),
                'genres': self.get_genre_aggregation(),
                'years': self.get_year_distribution(),
                'directors': self.get_director_statistics()
            }
            
            # Get overview stats
            total_response = self.client.count(index=self.index_name)
            stats['overview']['total_movies'] = total_response['count']
            
            # Get latest movie by year
            latest_response = self.client.search(
                index=self.index_name,
                size=1,
                sort=[{"release_year": {"order": "desc"}}, {"rating": {"order": "desc"}}],
                _source=["title", "release_year", "rating"]
            )
            
            if latest_response['hits']['hits']:
                latest_movie = latest_response['hits']['hits'][0]['_source']
                stats['overview']['latest_movie'] = f"{latest_movie['title']} ({latest_movie['release_year']})"
            
            return stats
            
        except Exception as e:
            print(f"Error getting comprehensive stats: {e}")
            return {}
