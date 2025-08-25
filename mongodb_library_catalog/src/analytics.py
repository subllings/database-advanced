"""
Analytics Module

This module handles aggregation operations and provides analytical insights
about the library catalog data.
"""

import logging
from datetime import datetime, timedelta


class Analytics:
    """Analytics manager for library catalog insights."""
    
    def __init__(self, mongo_client):
        """
        Initialize analytics manager.
        
        Args:
            mongo_client: MongoDBClient instance
        """
        self.mongo_client = mongo_client
        self.db = mongo_client.get_database()
        self.books_collection = self.db.books
        self.users_collection = self.db.users
        self.logger = logging.getLogger(__name__)
    
    def get_books_per_genre(self):
        """
        Get count of books per genre.
        
        Returns:
            list: List of genre statistics
        """
        try:
            pipeline = [
                {"$unwind": "$genres"},
                {
                    "$group": {
                        "_id": "$genres",
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"count": -1}}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated genre statistics for {len(result)} genres")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting books per genre: {e}")
            return []
    
    def get_average_rating_per_genre(self):
        """
        Get average rating per genre.
        
        Returns:
            list: List of genre rating statistics
        """
        try:
            pipeline = [
                {"$unwind": "$genres"},
                {
                    "$group": {
                        "_id": "$genres",
                        "average_rating": {"$avg": "$ratings.average"},
                        "book_count": {"$sum": 1},
                        "total_ratings": {"$sum": "$ratings.count"}
                    }
                },
                {
                    "$project": {
                        "genre": "$_id",
                        "average_rating": {"$round": ["$average_rating", 2]},
                        "book_count": 1,
                        "total_ratings": 1,
                        "_id": 0
                    }
                },
                {"$sort": {"average_rating": -1}}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated rating statistics for {len(result)} genres")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting average rating per genre: {e}")
            return []
    
    def get_books_per_decade(self):
        """
        Get count of books published per decade.
        
        Returns:
            list: List of decade statistics
        """
        try:
            pipeline = [
                {
                    "$addFields": {
                        "decade": {
                            "$subtract": [
                                "$publication.year",
                                {"$mod": ["$publication.year", 10]}
                            ]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$decade",
                        "count": {"$sum": 1},
                        "average_rating": {"$avg": "$ratings.average"}
                    }
                },
                {
                    "$project": {
                        "decade": "$_id",
                        "count": 1,
                        "average_rating": {"$round": ["$average_rating", 2]},
                        "_id": 0
                    }
                },
                {"$sort": {"decade": 1}}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated decade statistics for {len(result)} decades")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting books per decade: {e}")
            return []
    
    def get_most_prolific_authors(self, limit=10):
        """
        Get authors with the most books.
        
        Args:
            limit (int): Number of top authors to return
            
        Returns:
            list: List of prolific authors
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$author.name",
                        "book_count": {"$sum": 1},
                        "average_rating": {"$avg": "$ratings.average"},
                        "total_pages": {"$sum": "$pages"},
                        "nationality": {"$first": "$author.nationality"},
                        "birth_year": {"$first": "$author.birth_year"}
                    }
                },
                {
                    "$project": {
                        "author": "$_id",
                        "book_count": 1,
                        "average_rating": {"$round": ["$average_rating", 2]},
                        "total_pages": 1,
                        "nationality": 1,
                        "birth_year": 1,
                        "_id": 0
                    }
                },
                {"$sort": {"book_count": -1}},
                {"$limit": limit}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated prolific authors list with {len(result)} authors")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting prolific authors: {e}")
            return []
    
    def get_authors_by_nationality(self):
        """
        Get count of authors by nationality.
        
        Returns:
            list: List of nationality statistics
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$author.nationality",
                        "author_count": {"$addToSet": "$author.name"},
                        "book_count": {"$sum": 1},
                        "average_rating": {"$avg": "$ratings.average"}
                    }
                },
                {
                    "$project": {
                        "nationality": "$_id",
                        "author_count": {"$size": "$author_count"},
                        "book_count": 1,
                        "average_rating": {"$round": ["$average_rating", 2]},
                        "_id": 0
                    }
                },
                {"$sort": {"author_count": -1}}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated nationality statistics for {len(result)} nationalities")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting authors by nationality: {e}")
            return []
    
    def get_top_rated_books(self, limit=10):
        """
        Get top-rated books.
        
        Args:
            limit (int): Number of top books to return
            
        Returns:
            list: List of top-rated books
        """
        try:
            pipeline = [
                {
                    "$match": {
                        "ratings.count": {"$gte": 100}  # Only books with sufficient ratings
                    }
                },
                {
                    "$project": {
                        "title": 1,
                        "author": "$author.name",
                        "average_rating": "$ratings.average",
                        "rating_count": "$ratings.count",
                        "genres": 1,
                        "publication_year": "$publication.year"
                    }
                },
                {"$sort": {"average_rating": -1, "rating_count": -1}},
                {"$limit": limit}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated top-rated books list with {len(result)} books")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting top-rated books: {e}")
            return []
    
    def get_language_distribution(self):
        """
        Get distribution of books by language.
        
        Returns:
            list: List of language statistics
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$language",
                        "count": {"$sum": 1},
                        "average_rating": {"$avg": "$ratings.average"},
                        "average_pages": {"$avg": "$pages"}
                    }
                },
                {
                    "$project": {
                        "language": "$_id",
                        "count": 1,
                        "average_rating": {"$round": ["$average_rating", 2]},
                        "average_pages": {"$round": ["$average_pages", 0]},
                        "_id": 0
                    }
                },
                {"$sort": {"count": -1}}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated language distribution for {len(result)} languages")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting language distribution: {e}")
            return []
    
    def get_publisher_statistics(self, limit=10):
        """
        Get statistics about publishers.
        
        Args:
            limit (int): Number of top publishers to return
            
        Returns:
            list: List of publisher statistics
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$publication.publisher",
                        "book_count": {"$sum": 1},
                        "average_rating": {"$avg": "$ratings.average"},
                        "total_pages": {"$sum": "$pages"},
                        "earliest_year": {"$min": "$publication.year"},
                        "latest_year": {"$max": "$publication.year"}
                    }
                },
                {
                    "$project": {
                        "publisher": "$_id",
                        "book_count": 1,
                        "average_rating": {"$round": ["$average_rating", 2]},
                        "total_pages": 1,
                        "active_years": {
                            "$subtract": ["$latest_year", "$earliest_year"]
                        },
                        "earliest_year": 1,
                        "latest_year": 1,
                        "_id": 0
                    }
                },
                {"$sort": {"book_count": -1}},
                {"$limit": limit}
            ]
            
            result = list(self.books_collection.aggregate(pipeline))
            self.logger.info(f"Generated publisher statistics for {len(result)} publishers")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting publisher statistics: {e}")
            return []
    
    def get_user_statistics(self):
        """
        Get statistics about users and their reading patterns.
        
        Returns:
            dict: User statistics
        """
        try:
            stats = {}
            
            # Total users
            stats["total_users"] = self.users_collection.count_documents({})
            
            # Users by membership type
            membership_pipeline = [
                {
                    "$group": {
                        "_id": "$membership.type",
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"count": -1}}
            ]
            stats["membership_distribution"] = list(self.users_collection.aggregate(membership_pipeline))
            
            # Users by reading frequency
            frequency_pipeline = [
                {
                    "$group": {
                        "_id": "$preferences.reading_frequency",
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"count": -1}}
            ]
            stats["reading_frequency_distribution"] = list(self.users_collection.aggregate(frequency_pipeline))
            
            # Most popular genres among users
            genre_pipeline = [
                {"$unwind": "$preferences.favorite_genres"},
                {
                    "$group": {
                        "_id": "$preferences.favorite_genres",
                        "user_count": {"$sum": 1}
                    }
                },
                {"$sort": {"user_count": -1}},
                {"$limit": 10}
            ]
            stats["popular_genres"] = list(self.users_collection.aggregate(genre_pipeline))
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting user statistics: {e}")
            return {}
    
    def get_borrowing_analytics(self):
        """
        Get analytics about borrowing patterns.
        
        Returns:
            dict: Borrowing analytics
        """
        try:
            analytics = {}
            
            # Total borrowing records
            pipeline = [
                {"$unwind": "$borrowing_history"},
                {
                    "$group": {
                        "_id": None,
                        "total_borrowings": {"$sum": 1},
                        "returned_books": {
                            "$sum": {
                                "$cond": [{"$ne": ["$borrowing_history.returned_date", None]}, 1, 0]
                            }
                        },
                        "current_borrowings": {
                            "$sum": {
                                "$cond": [{"$eq": ["$borrowing_history.returned_date", None]}, 1, 0]
                            }
                        },
                        "average_rating": {"$avg": "$borrowing_history.rating"}
                    }
                }
            ]
            
            result = list(self.users_collection.aggregate(pipeline))
            if result:
                analytics.update(result[0])
                analytics["average_rating"] = round(analytics.get("average_rating", 0), 2)
            
            # Most borrowed books
            most_borrowed_pipeline = [
                {"$unwind": "$borrowing_history"},
                {
                    "$group": {
                        "_id": "$borrowing_history.book_id",
                        "borrow_count": {"$sum": 1},
                        "average_user_rating": {"$avg": "$borrowing_history.rating"}
                    }
                },
                {
                    "$lookup": {
                        "from": "books",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "book_info"
                    }
                },
                {"$unwind": "$book_info"},
                {
                    "$project": {
                        "title": "$book_info.title",
                        "author": "$book_info.author.name",
                        "borrow_count": 1,
                        "average_user_rating": {"$round": ["$average_user_rating", 2]},
                        "_id": 0
                    }
                },
                {"$sort": {"borrow_count": -1}},
                {"$limit": 10}
            ]
            
            analytics["most_borrowed_books"] = list(self.users_collection.aggregate(most_borrowed_pipeline))
            
            # Most active users
            active_users_pipeline = [
                {
                    "$project": {
                        "user_id": 1,
                        "name": 1,
                        "borrowing_count": {"$size": "$borrowing_history"}
                    }
                },
                {"$sort": {"borrowing_count": -1}},
                {"$limit": 10}
            ]
            
            analytics["most_active_users"] = list(self.users_collection.aggregate(active_users_pipeline))
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting borrowing analytics: {e}")
            return {}
    
    def get_comprehensive_report(self):
        """
        Get a comprehensive analytics report.
        
        Returns:
            dict: Comprehensive analytics report
        """
        try:
            report = {
                "generated_at": datetime.utcnow(),
                "book_analytics": {
                    "genres": self.get_books_per_genre(),
                    "genre_ratings": self.get_average_rating_per_genre(),
                    "decades": self.get_books_per_decade(),
                    "top_authors": self.get_most_prolific_authors(),
                    "nationalities": self.get_authors_by_nationality(),
                    "top_rated": self.get_top_rated_books(),
                    "languages": self.get_language_distribution(),
                    "publishers": self.get_publisher_statistics()
                },
                "user_analytics": self.get_user_statistics(),
                "borrowing_analytics": self.get_borrowing_analytics()
            }
            
            self.logger.info("Generated comprehensive analytics report")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating comprehensive report: {e}")
            return {}
