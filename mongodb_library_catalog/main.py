"""
MongoDB Library Catalog - Main Application Entry Point

This module serves as the main entry point for the MongoDB Library Catalog application.
It orchestrates the setup, data loading, and user interface interactions.
"""

import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from mongodb_client import MongoDBClient
from data_loader import DataLoader
from interface import LibraryInterface


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('library_catalog.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=" * 60)
    print("     MONGODB LIBRARY CATALOG SYSTEM")
    print("=" * 60)
    print()
    
    try:
        # Initialize MongoDB client
        logger.info("Initializing MongoDB connection...")
        mongo_client = MongoDBClient()
        
        if not mongo_client.connect():
            logger.error("Failed to connect to MongoDB")
            print("Error: Could not connect to MongoDB.")
            print("Please ensure MongoDB is running using: ./scripts/start-mongodb.sh")
            return False
        
        print("Successfully connected to MongoDB!")
        print()
        
        # Initialize data loader
        logger.info("Initializing data loader...")
        data_loader = DataLoader(mongo_client)
        
        # Check if data needs to be loaded
        if data_loader.needs_initial_setup():
            print("Setting up library catalog with sample data...")
            print("This may take a few moments...")
            print()
            
            if data_loader.load_all_data():
                print("Sample data loaded successfully!")
                print()
            else:
                logger.error("Failed to load sample data")
                print("Warning: Could not load sample data. Some features may not work properly.")
                print()
        else:
            print("Library catalog data already exists.")
            print()
        
        # Start interactive interface
        logger.info("Starting interactive interface...")
        interface = LibraryInterface(mongo_client)
        interface.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\nUnexpected error occurred: {e}")
        print("Please check the logs for more details.")
    finally:
        try:
            mongo_client.close()
            logger.info("MongoDB connection closed")
        except:
            pass
    
    print("\nThank you for using MongoDB Library Catalog!")
    return True


if __name__ == "__main__":
    main()
