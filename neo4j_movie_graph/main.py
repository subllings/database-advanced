"""
Neo4j Movie Graph - Main Application Entry Point

This module serves as the main entry point for the Neo4j Movie Graph application.
It orchestrates the setup, data loading, and user interface interactions.
"""

import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from neo4j_client import Neo4jClient
from data_loader import DataLoader
from interface import MovieGraphInterface


def setup_logging():
    """Configure logging for the application."""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'movie_graph.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=" * 60)
    print("     NEO4J MOVIE SOCIAL GRAPH SYSTEM")
    print("=" * 60)
    print()
    
    try:
        # Start interactive interface directly
        logger.info("Starting Neo4j Movie Graph interface...")
        interface = MovieGraphInterface()
        interface.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nUnexpected error occurred: {e}")
        print("Please check the logs for more details.")
    
    print("\nThank you for using Neo4j Movie Graph!")
    return True


if __name__ == "__main__":
    main()
