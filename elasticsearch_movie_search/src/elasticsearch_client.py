"""
Elasticsearch client configuration and connection management.

This module provides a centralized way to connect to Elasticsearch
and manage the connection settings.
"""

import os
from typing import Dict, Any, Optional
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ElasticsearchClient:
    """
    Elasticsearch client wrapper for movie search application.
    
    Handles connection configuration, health checks, and provides
    a reusable client instance for the application.
    """
    
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None):
        """
        Initialize Elasticsearch client.
        
        Args:
            host: Elasticsearch host (defaults to env variable or localhost)
            port: Elasticsearch port (defaults to env variable or 9200)
        """
        self.host = host or os.getenv('ELASTICSEARCH_HOST', 'localhost')
        self.port = port or int(os.getenv('ELASTICSEARCH_PORT', 9200))
        self.index_name = os.getenv('ELASTICSEARCH_INDEX', 'movies')
        
        # Initialize client
        self.client = self._create_client()
        
    def _create_client(self) -> Elasticsearch:
        """
        Create and configure Elasticsearch client.
        
        Returns:
            Configured Elasticsearch client instance
        """
        try:
            # Basic configuration for local development
            client = Elasticsearch(
                [{'host': self.host, 'port': self.port}],
                # Disable SSL verification for local development
                verify_certs=False,
                # Optional authentication
                basic_auth=(
                    os.getenv('ELASTICSEARCH_USERNAME'),
                    os.getenv('ELASTICSEARCH_PASSWORD')
                ) if os.getenv('ELASTICSEARCH_USERNAME') else None
            )
            
            # Test connection
            if client.ping():
                print(f"✅ Connected to Elasticsearch at {self.host}:{self.port}")
                return client
            else:
                raise ConnectionError("Failed to ping Elasticsearch")
                
        except Exception as e:
            print(f"❌ Failed to connect to Elasticsearch: {e}")
            print(f"Make sure Elasticsearch is running on {self.host}:{self.port}")
            raise
    
    def get_client(self) -> Elasticsearch:
        """
        Get the Elasticsearch client instance.
        
        Returns:
            Elasticsearch client
        """
        return self.client
    
    def get_index_name(self) -> str:
        """
        Get the configured index name.
        
        Returns:
            Index name for movies
        """
        return self.index_name
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check Elasticsearch cluster health.
        
        Returns:
            Dictionary containing cluster health information
        """
        try:
            health = self.client.cluster.health()
            return {
                'status': health['status'],
                'cluster_name': health['cluster_name'],
                'number_of_nodes': health['number_of_nodes'],
                'active_primary_shards': health['active_primary_shards'],
                'active_shards': health['active_shards']
            }
        except Exception as e:
            return {'error': str(e)}
    
    def index_exists(self, index_name: Optional[str] = None) -> bool:
        """
        Check if an index exists.
        
        Args:
            index_name: Name of the index to check (defaults to configured index)
            
        Returns:
            True if index exists, False otherwise
        """
        index_name = index_name or self.index_name
        return self.client.indices.exists(index=index_name)
    
    def create_index(self, index_name: Optional[str] = None, mapping: Optional[Dict] = None) -> bool:
        """
        Create an index with optional mapping.
        
        Args:
            index_name: Name of the index to create (defaults to configured index)
            mapping: Index mapping configuration
            
        Returns:
            True if successful, False otherwise
        """
        index_name = index_name or self.index_name
        
        try:
            if self.index_exists(index_name):
                print(f"Index '{index_name}' already exists")
                return True
                
            body = {}
            if mapping:
                body['mappings'] = mapping
                
            response = self.client.indices.create(index=index_name, body=body)
            print(f"✅ Created index '{index_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create index '{index_name}': {e}")
            return False
    
    def delete_index(self, index_name: Optional[str] = None) -> bool:
        """
        Delete an index.
        
        Args:
            index_name: Name of the index to delete (defaults to configured index)
            
        Returns:
            True if successful, False otherwise
        """
        index_name = index_name or self.index_name
        
        try:
            if not self.index_exists(index_name):
                print(f"Index '{index_name}' does not exist")
                return True
                
            self.client.indices.delete(index=index_name)
            print(f"✅ Deleted index '{index_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Failed to delete index '{index_name}': {e}")
            return False
