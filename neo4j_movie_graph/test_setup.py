#!/usr/bin/env python3
"""
Test Script for Neo4j Movie Graph Database

This script tests the basic functionality of the Neo4j movie graph database.
Run this after setting up the environment to verify everything works.
"""

import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

try:
    from neo4j_client import Neo4jClient
    from data_loader import DataLoader
    from movie_manager import MovieManager
    from person_manager import PersonManager
    from graph_analytics import GraphAnalytics
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)


def test_neo4j_connection():
    """Test Neo4j connection."""
    print("\n" + "="*50)
    print("Testing Neo4j Connection")
    print("="*50)
    
    client = Neo4jClient()
    
    if client.connect():
        print("✓ Connected to Neo4j successfully")
        
        # Test basic query
        try:
            result = client.execute_query("RETURN 'Hello, Neo4j!' as message")
            print(f"✓ Test query result: {result[0]['message']}")
        except Exception as e:
            print(f"✗ Test query failed: {e}")
            return False
        
        client.close()
        return True
    else:
        print("✗ Failed to connect to Neo4j")
        print("  Make sure Neo4j is running: ./start-neo4j.sh")
        return False


def test_database_operations():
    """Test basic database operations."""
    print("\n" + "="*50)
    print("Testing Database Operations")
    print("="*50)
    
    client = Neo4jClient()
    if not client.connect():
        print("✗ Cannot test database operations without connection")
        return False
    
    try:
        # Test creating indexes
        print("Creating database indexes...")
        client.create_indexes()
        print("✓ Indexes created successfully")
        
        # Test creating constraints
        print("Creating database constraints...")
        client.create_constraints()
        print("✓ Constraints created successfully")
        
        # Test data loader
        data_loader = DataLoader(client)
        print("Testing sample data loading...")
        
        # Clear existing data first
        client.clear_database()
        print("✓ Database cleared")
        
        # Load sample data
        if data_loader.load_sample_data():
            print("✓ Sample data loaded successfully")
        else:
            print("✗ Failed to load sample data")
            return False
        
        # Test managers
        movie_manager = MovieManager(client)
        person_manager = PersonManager(client)
        analytics = GraphAnalytics(client)
        
        # Test movie queries
        print("Testing movie queries...")
        movies = movie_manager.search_movies("Matrix")
        print(f"✓ Found {len(movies)} Matrix movies")
        
        # Test person queries
        print("Testing person queries...")
        people = person_manager.search_people("Keanu")
        print(f"✓ Found {len(people)} people named Keanu")
        
        # Test analytics
        print("Testing graph analytics...")
        stats = analytics.get_graph_statistics()
        print(f"✓ Graph has {stats.get('total_nodes', 0)} nodes and {stats.get('total_relationships', 0)} relationships")
        
        return True
        
    except Exception as e:
        print(f"✗ Database operations test failed: {e}")
        return False
    finally:
        client.close()


def test_environment():
    """Test environment setup."""
    print("\n" + "="*50)
    print("Testing Environment Setup")
    print("="*50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version >= (3, 8):
        print("✓ Python version is compatible")
    else:
        print("✗ Python 3.8+ required")
        return False
    
    # Check required directories
    required_dirs = ["src", "data", "logs"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ Directory exists: {dir_name}/")
        else:
            print(f"✗ Missing directory: {dir_name}/")
            return False
    
    # Check required files
    required_files = [
        "requirements.txt",
        "docker-compose.yml",
        "main.py",
        "src/neo4j_client.py",
        "src/data_loader.py",
        "src/movie_manager.py",
        "src/person_manager.py",
        "src/graph_analytics.py",
        "src/interface.py"
    ]
    
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"✓ File exists: {file_name}")
        else:
            print(f"✗ Missing file: {file_name}")
            return False
    
    return True


def main():
    """Run all tests."""
    print("Neo4j Movie Graph Database - Test Suite")
    print("="*60)
    
    all_passed = True
    
    # Test environment
    if not test_environment():
        print("\n✗ Environment test failed")
        all_passed = False
    
    # Test Neo4j connection
    if not test_neo4j_connection():
        print("\n✗ Neo4j connection test failed")
        all_passed = False
    else:
        # Only test database operations if connection works
        if not test_database_operations():
            print("\n✗ Database operations test failed")
            all_passed = False
    
    # Final result
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("Your Neo4j Movie Graph Database is ready to use.")
        print("Run 'python main.py' to start the interactive interface.")
    else:
        print("✗ SOME TESTS FAILED!")
        print("Please fix the issues above before using the application.")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
