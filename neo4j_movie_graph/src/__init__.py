"""
Neo4j Movie Graph Database Package

This package provides a complete Neo4j-based movie graph database system
with support for movies, people, relationships, and graph analytics.
"""

from .neo4j_client import Neo4jClient
from .data_loader import DataLoader
from .movie_manager import MovieManager
from .person_manager import PersonManager
from .graph_analytics import GraphAnalytics
from .interface import MovieGraphInterface

__version__ = "1.0.0"
__author__ = "Database Advanced Project"
__description__ = "Neo4j Movie Graph Database System"

__all__ = [
    "Neo4jClient",
    "DataLoader", 
    "MovieManager",
    "PersonManager",
    "GraphAnalytics",
    "MovieGraphInterface"
]
