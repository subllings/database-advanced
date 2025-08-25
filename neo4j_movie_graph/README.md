# Neo4j Movie Social Graph

A comprehensive movie social graph system built with Neo4j and Python, demonstrating graph database capabilities for analyzing relationships between movies, actors, directors, and genres.

## Project Overview

This project implements a movie social graph using Neo4j to store, query, and analyze movie data. It demonstrates key graph database concepts including nodes, relationships, graph traversals, and pattern matching using Cypher queries.

## Features

### Must-Have (Core Requirements)
- [x] Graph model with nodes, relationships, and properties
- [x] Basic Cypher queries exploring the graph
- [x] Aggregation queries for insights
- [x] Update operations on nodes and relationships

### Nice-to-Have (Advanced Features)
- [x] Graph algorithms (PageRank, centrality, community detection)
- [x] Shortest path queries between people
- [x] Movie recommendation system
- [x] Interactive interface for graph exploration
- [x] Data visualization capabilities
- [x] Error handling and logging

## Project Structure

```
neo4j_movie_graph/
├── src/
│   ├── neo4j_client.py       # Neo4j connection management
│   ├── data_loader.py        # Data loading and graph creation
│   ├── movie_manager.py      # Movie-related queries and operations
│   ├── person_manager.py     # Person-related queries and operations
│   ├── graph_analytics.py    # Graph algorithms and analytics
│   └── interface.py          # Interactive command-line interface
├── data/
│   ├── movies.json          # Sample movie data
│   ├── persons.json         # Sample person data (actors, directors)
│   └── relationships.json   # Sample relationship data
├── scripts/
│   ├── setup-env.sh         # Environment setup
│   ├── start-neo4j.sh       # Start Neo4j with Docker
│   ├── stop-neo4j.sh        # Stop Neo4j
│   └── run-graph.sh         # Run the movie graph application
├── requirements.txt         # Python dependencies
├── main.py                 # Main application entry point
├── docker-compose.yml      # Neo4j Docker configuration
└── README.md              # This file
```

## Quick Start

### 1. Setup Environment
```bash
chmod +x scripts/*.sh
./scripts/setup-env.sh
```

### 2. Start Neo4j
```bash
./scripts/start-neo4j.sh
```

### 3. Run the Application
```bash
./scripts/run-graph.sh
```

## Neo4j Setup

### Using Docker (Recommended)
```bash
docker run -d -p 7474:7474 -p 7687:7687 --name neo4j neo4j:5.0
```

### Using Docker Compose
```bash
docker-compose up -d
```

## Graph Model

### Nodes
- **Movie**: title, year, plot, runtime, rating
- **Person**: name, birth_year, nationality
- **Genre**: name, description

### Relationships
- **(Person)-[:ACTED_IN]->(Movie)**: with properties (role, character)
- **(Person)-[:DIRECTED]->(Movie)**: with properties (year)
- **(Person)-[:PRODUCED]->(Movie)**: with properties (type)
- **(Movie)-[:HAS_GENRE]->(Genre)**
- **(Person)-[:COLLABORATED_WITH]->(Person)**: derived relationship

### Example Graph Structure
```cypher
(:Person {name: "Leonardo DiCaprio"})-[:ACTED_IN {role: "lead"}]->
(:Movie {title: "Inception", year: 2010})-[:HAS_GENRE]->(:Genre {name: "Sci-Fi"})

(:Person {name: "Christopher Nolan"})-[:DIRECTED]->
(:Movie {title: "Inception", year: 2010})
```

## Key Features Demonstrated

### 1. Graph Data Modeling
- Node types with properties
- Relationship types with properties
- Complex graph patterns

### 2. Cypher Query Operations
- **Pattern Matching**: Find actors in specific movies
- **Traversals**: Find all collaborators of an actor
- **Filtering**: Movies by genre, year, rating
- **Path Queries**: Shortest path between actors

### 3. Graph Analytics
- **Centrality Algorithms**: Most connected actors
- **Community Detection**: Actor collaboration clusters
- **PageRank**: Most influential people in the network
- **Recommendation Engine**: Similar movies/actors

### 4. Update Operations
- Add new movies and relationships
- Update person information
- Create derived relationships
- Bulk data modifications

## Usage Examples

### Basic Queries
```python
# Find all movies directed by Christopher Nolan
nolan_movies = movie_manager.find_movies_by_director("Christopher Nolan")

# Find all actors who worked with Leonardo DiCaprio
dicaprio_collaborators = person_manager.find_collaborators("Leonardo DiCaprio")

# Find action movies after 2010
recent_action = movie_manager.find_movies_by_genre_and_year("Action", 2010)
```

### Graph Analytics
```python
# Find most influential actors using PageRank
top_actors = analytics.calculate_pagerank("Person")

# Find shortest path between two actors
path = analytics.shortest_path("Actor1", "Actor2")

# Get movie recommendations for a person
recommendations = analytics.recommend_movies("Leonardo DiCaprio")
```

### Graph Algorithms
```python
# Find actor collaboration communities
communities = analytics.detect_communities()

# Calculate betweenness centrality
centrality = analytics.betweenness_centrality()

# Find most frequent collaborators
collaborators = analytics.frequent_collaborators()
```

## Technologies Used

- **Neo4j 5.0**: Graph database
- **Python 3.12**: Programming language
- **py2neo**: Neo4j Python driver
- **Pandas**: Data manipulation and analysis
- **Docker**: Containerization for Neo4j
- **Cypher**: Graph query language

## Learning Objectives Achieved

- Graph Database Concepts: Nodes, relationships, properties
- Cypher Query Language: Pattern matching, traversals, aggregations
- Graph Algorithms: Centrality, community detection, shortest paths
- Data Loading: From datasets to graph structures
- Performance Considerations: Indexing and query optimization
- Real-world Applications: Social networks, recommendation systems

## Sample Queries and Results

The application includes comprehensive Cypher queries demonstrating:

1. **Pattern Matching**: Finding complex relationship patterns
2. **Graph Traversals**: Multi-hop relationship exploration
3. **Aggregations**: Counting, grouping, statistical analysis
4. **Path Finding**: Shortest paths and path analysis
5. **Updates**: Adding and modifying graph data
6. **Algorithms**: Graph theory applications

## Development Notes

This project demonstrates production-ready practices:
- Clean code organization with modular components
- Comprehensive error handling and logging
- Interactive user interface for graph exploration
- Docker-based development environment
- Clear documentation with examples

## Graph Database Advantages

This project showcases why graph databases excel at:
- **Relationship Analysis**: Natural representation of connections
- **Pattern Detection**: Complex relationship patterns
- **Recommendation Systems**: Collaborative filtering
- **Social Network Analysis**: Community detection, influence
- **Performance**: Fast traversals of connected data

## Next Steps

Potential enhancements for advanced learning:
- Implement real-time graph streaming
- Add temporal relationships (time-based connections)
- Integrate with external movie APIs (TMDB, IMDB)
- Build web-based graph visualization
- Implement machine learning on graph features

---

**Built as part of the BeCode Database Advanced curriculum**
