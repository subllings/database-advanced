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
                hosts=[f"http://{self.host}:{self.port}"],
                timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
            return client
        except Exception as e:
            print(f"Error creating Elasticsearch client: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test connection to Elasticsearch.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Ping Elasticsearch
            if self.client.ping():
                print(f"Successfully connected to Elasticsearch at {self.host}:{self.port}")
                return True
            else:
                print(f"Failed to ping Elasticsearch at {self.host}:{self.port}")
                return False
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_cluster_info(self) -> Dict[str, Any]:
        """
        Get cluster information and health status.

        Returns:
            Dictionary containing cluster information
        """
        try:
            info = self.client.info()
            health = self.client.cluster.health()
            
            return {
                'cluster_name': info.get('cluster_name', 'Unknown'),
                'version': info.get('version', {}).get('number', 'Unknown'),
                'status': health.get('status', 'Unknown'),
                'number_of_nodes': health.get('number_of_nodes', 0),
                'number_of_data_nodes': health.get('number_of_data_nodes', 0)
            }
        except Exception as e:
            print(f"Error getting cluster info: {e}")
            return {}

    def check_index_exists(self, index_name: Optional[str] = None) -> bool:
        """
        Check if an index exists.

        Args:
            index_name: Name of the index to check (defaults to self.index_name)

        Returns:
            True if index exists, False otherwise
        """
        index = index_name or self.index_name
        try:
            return self.client.indices.exists(index=index).body
        except Exception as e:
            print(f"Error checking index existence: {e}")
            return False

    def create_index(self, index_name: Optional[str] = None, 
                    mapping: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create an index with optional mapping.

        Args:
            index_name: Name of the index to create (defaults to self.index_name)
            mapping: Index mapping configuration

        Returns:
            True if index was created successfully, False otherwise
        """
        index = index_name or self.index_name
        try:
            kwargs = {}
            if mapping:
                kwargs['mappings'] = mapping

            self.client.indices.create(index=index, **kwargs)
            print(f"Index '{index}' created successfully")
            return True
        except Exception as e:
            print(f"Error creating index '{index}': {e}")
            return False

    def delete_index(self, index_name: Optional[str] = None) -> bool:
        """
        Delete an index.

        Args:
            index_name: Name of the index to delete (defaults to self.index_name)

        Returns:
            True if index was deleted successfully, False otherwise
        """
        index = index_name or self.index_name
        try:
            if self.check_index_exists(index):
                self.client.indices.delete(index=index)
                print(f"Index '{index}' deleted successfully")
                return True
            else:
                print(f"Index '{index}' does not exist")
                return False
        except Exception as e:
            print(f"Error deleting index '{index}': {e}")
            return False

    def get_index_info(self, index_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about an index.

        Args:
            index_name: Name of the index (defaults to self.index_name)

        Returns:
            Dictionary containing index information
        """
        index = index_name or self.index_name
        try:
            if not self.check_index_exists(index):
                return {'error': f"Index '{index}' does not exist"}

            # Get index stats
            stats = self.client.indices.stats(index=index)
            mapping = self.client.indices.get_mapping(index=index)
            
            index_stats = stats['indices'][index]
            return {
                'index_name': index,
                'document_count': index_stats['total']['docs']['count'],
                'store_size': index_stats['total']['store']['size_in_bytes'],
                'mapping': mapping[index]['mappings'] if index in mapping else {}
            }
        except Exception as e:
            print(f"Error getting index info: {e}")
            return {'error': str(e)}

    def close(self):
        """Close the Elasticsearch client connection."""
        try:
            if hasattr(self.client, 'close'):
                self.client.close()
        except Exception as e:
            print(f"Error closing client: {e}")
