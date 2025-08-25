"""
MongoDB Client Module

This module handles the MongoDB connection and provides basic database operations.
"""

import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import time


class MongoDBClient:
    """MongoDB client for library catalog operations."""
    
    def __init__(self, host="localhost", port=27017, username="admin", password="password123"):
        """
        Initialize MongoDB client.
        
        Args:
            host (str): MongoDB host
            port (int): MongoDB port
            username (str): MongoDB username
            password (str): MongoDB password
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.db = None
        self.logger = logging.getLogger(__name__)
        
        # Connection string
        self.connection_string = f"mongodb://{username}:{password}@{host}:{port}/"
    
    def connect(self, max_retries=3, retry_delay=2):
        """
        Connect to MongoDB database.
        
        Args:
            max_retries (int): Maximum connection retry attempts
            retry_delay (int): Delay between retry attempts in seconds
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Attempting to connect to MongoDB (attempt {attempt + 1}/{max_retries})")
                
                # Create MongoDB client
                self.client = MongoClient(
                    self.connection_string,
                    serverSelectionTimeoutMS=5000,  # 5 second timeout
                    connectTimeoutMS=10000,         # 10 second timeout
                    socketTimeoutMS=10000           # 10 second timeout
                )
                
                # Test the connection
                self.client.admin.command('ismaster')
                
                # Connect to library database
                self.db = self.client.library_catalog
                
                self.logger.info("Successfully connected to MongoDB")
                return True
                
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
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
    
    def get_database(self):
        """
        Get the library catalog database.
        
        Returns:
            Database: MongoDB database instance
        """
        if self.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db
    
    def get_collection(self, collection_name):
        """
        Get a specific collection from the database.
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            Collection: MongoDB collection instance
        """
        if self.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db[collection_name]
    
    def list_collections(self):
        """
        List all collections in the database.
        
        Returns:
            list: List of collection names
        """
        if self.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db.list_collection_names()
    
    def drop_collection(self, collection_name):
        """
        Drop a collection from the database.
        
        Args:
            collection_name (str): Name of the collection to drop
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.db[collection_name].drop()
            self.logger.info(f"Collection '{collection_name}' dropped successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error dropping collection '{collection_name}': {e}")
            return False
    
    def create_indexes(self):
        """
        Create indexes for better query performance.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Books collection indexes
            books = self.get_collection("books")
            books.create_index("title")
            books.create_index("author.name")
            books.create_index("genres")
            books.create_index("isbn")
            books.create_index("publication.year")
            books.create_index("ratings.average")
            
            # Users collection indexes
            users = self.get_collection("users")
            users.create_index("user_id", unique=True)
            users.create_index("email", unique=True)
            users.create_index("membership.type")
            
            self.logger.info("Database indexes created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating indexes: {e}")
            return False
    
    def get_connection_status(self):
        """
        Get current connection status and database information.
        
        Returns:
            dict: Connection status information
        """
        if self.client is None:
            return {"connected": False, "message": "No connection established"}
        
        try:
            # Test connection
            self.client.admin.command('ismaster')
            
            # Get database stats
            stats = self.db.command("dbstats")
            collections = self.list_collections()
            
            return {
                "connected": True,
                "host": self.host,
                "port": self.port,
                "database": "library_catalog",
                "collections": collections,
                "total_collections": len(collections),
                "data_size": stats.get("dataSize", 0),
                "storage_size": stats.get("storageSize", 0)
            }
            
        except Exception as e:
            return {"connected": False, "message": str(e)}
    
    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")
            self.client = None
            self.db = None
