# 🎬 Graph Database Mini-Project: Movie Social Graph with Neo4j

In this project, you’ll design a **Movie Social Graph** using **Neo4j**, a leading open-source graph database.  
The project will help you understand how to represent **nodes** (entities) and **relationships** (connections) and query them with Cypher.  



## 🎯 Goal
By the end of this exercise, you should be able to:  
- Understand **graph data modeling** (nodes, relationships, properties)  
- Load and explore data from an **open dataset**  
- Write **Cypher queries** to traverse the graph  
- Use **aggregations** and graph algorithms for insights  



## 📂 Dataset
Use an **open-source dataset** about movies and people. Possible options:  
- [The Movie Database (TMDB) Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)  
- [IMDB Datasets](https://datasets.imdbws.com/) (title.basics, name.basics, etc.)  
- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)  

👉 Choose a dataset that contains at least:  
- Movies (title, year, genre)  
- People (actors, directors)  
- Relationships (acted in, directed)  
- Optional: ratings or popularity  



## 📋 General Guidelines

### Step 1. Design Your Graph Model
Think about how to represent your data. Example:  
- **Nodes**: `Movie`, `Person`, `Genre`  
- **Relationships**:  
  - `(:Person)-[:ACTED_IN]->(:Movie)`  
  - `(:Person)-[:DIRECTED]->(:Movie)`  
  - `(:Movie)-[:HAS_GENRE]->(:Genre)`  

### Step 2. Insert Data
- Load your dataset into Neo4j  
- Insert a meaningful number of nodes and relationships (at least a few hundred)  

### Step 3. Run Queries
Write queries such as:  
- Find all movies by a given director  
- Find all actors who co-starred with a given actor  
- Find movies in a specific genre after 2010  

### Step 4. Aggregations / Patterns
Use Cypher to find patterns:  
- Most frequent collaborators (actor-director pairs)  
- Most popular genre (by number of movies)  
- Actors with the most connections  

### Step 5. Updates
Practice modifying the graph:  
- Add a new relationship between an actor and a movie  
- Add missing genres for certain movies  



## ✅ Deliverables

1 repository and your code and queries should follow **clean coding practices**:  
- Use meaningful variable names  
- Add docstrings to functions  
- Organize queries in reusable functions  
- Avoid hardcoding values unnecessarily  

### 🟢 Must-Have
By the end, you should have:  
1. A graph model with **nodes, relationships, and properties**  
2. Several **basic Cypher queries** that explore the graph  
3. At least one **aggregation query** to get insights from the graph  
4. At least one **update** to modify nodes or relationships  

### 🌟 Nice-to-Have
If you finish early or want to explore advanced features:  
- Use a **graph algorithm** (e.g., PageRank, community detection, centrality)  
- Find the **shortest path** between two people  
- Implement a simple **recommendation query** (e.g., “movies you might like” based on co-actors or genres)  
- Visualize the graph with Neo4j Bloom or external tools  



💡 **Key takeaway:** Graph databases like Neo4j excel at analyzing **relationships and connections** that are difficult to model in relational or document databases.
