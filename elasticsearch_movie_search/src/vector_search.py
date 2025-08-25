"""
Vector embeddings module for movie plot similarity search.

This module provides simple TF-IDF-like embeddings and cosine similarity
for semantic search in movie descriptions.
"""

import numpy as np
import re
from typing import List, Dict, Any, Tuple
from collections import Counter
import math


class SimpleVectorizer:
    """
    Simple TF-IDF vectorizer for movie plot embeddings.
    
    Uses basic term frequency and inverse document frequency
    to create vector representations of text.
    """
    
    def __init__(self, max_features: int = 100):
        """
        Initialize the vectorizer.
        
        Args:
            max_features: Maximum number of features to keep
        """
        self.max_features = max_features
        self.vocabulary = {}
        self.idf_scores = {}
        self.fitted = False
    
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by tokenizing and cleaning.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        
        # Split into words and remove short words
        words = [word for word in text.split() if len(word) > 2]
        
        return words
    
    def fit(self, documents: List[str]) -> None:
        """
        Fit the vectorizer on a collection of documents.
        
        Args:
            documents: List of text documents
        """
        # Count word frequencies across all documents
        word_counts = Counter()
        doc_word_counts = []
        
        for doc in documents:
            words = self._preprocess_text(doc)
            doc_words = set(words)
            doc_word_counts.append(doc_words)
            word_counts.update(words)
        
        # Select top features
        top_words = word_counts.most_common(self.max_features)
        self.vocabulary = {word: idx for idx, (word, _) in enumerate(top_words)}
        
        # Calculate IDF scores
        num_docs = len(documents)
        for word in self.vocabulary:
            # Count documents containing this word
            doc_freq = sum(1 for doc_words in doc_word_counts if word in doc_words)
            # Calculate IDF
            self.idf_scores[word] = math.log(num_docs / (doc_freq + 1))
        
        self.fitted = True
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform documents to TF-IDF vectors.
        
        Args:
            documents: List of text documents
            
        Returns:
            Matrix of TF-IDF vectors
        """
        if not self.fitted:
            raise ValueError("Vectorizer must be fitted before transform")
        
        vectors = []
        
        for doc in documents:
            words = self._preprocess_text(doc)
            word_counts = Counter(words)
            
            # Create TF-IDF vector
            vector = np.zeros(len(self.vocabulary))
            
            for word, tf in word_counts.items():
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    # TF-IDF = (term frequency) * (inverse document frequency)
                    vector[idx] = tf * self.idf_scores[word]
            
            vectors.append(vector)
        
        return np.array(vectors)
    
    def fit_transform(self, documents: List[str]) -> np.ndarray:
        """
        Fit the vectorizer and transform documents.
        
        Args:
            documents: List of text documents
            
        Returns:
            Matrix of TF-IDF vectors
        """
        self.fit(documents)
        return self.transform(documents)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


class MovieVectorSearch:
    """
    Vector-based similarity search for movies.
    
    Provides semantic search capabilities using plot embeddings.
    """
    
    def __init__(self):
        """Initialize the vector search engine."""
        self.vectorizer = SimpleVectorizer(max_features=50)
        self.movie_vectors = None
        self.movies = []
        self.fitted = False
    
    def fit(self, movies: List[Dict[str, Any]]) -> None:
        """
        Fit the vector search on movie data.
        
        Args:
            movies: List of movie dictionaries with 'description' field
        """
        self.movies = movies
        
        # Extract descriptions
        descriptions = [movie.get('description', '') for movie in movies]
        
        # Create embeddings
        self.movie_vectors = self.vectorizer.fit_transform(descriptions)
        
        self.fitted = True
    
    def find_similar_movies(self, query_movie_id: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Find movies similar to a given movie.
        
        Args:
            query_movie_id: ID of the query movie
            top_k: Number of similar movies to return
            
        Returns:
            List of (movie, similarity_score) tuples
        """
        if not self.fitted:
            raise ValueError("Vector search must be fitted before use")
        
        # Find the query movie
        query_idx = None
        for idx, movie in enumerate(self.movies):
            if movie.get('id') == query_movie_id:
                query_idx = idx
                break
        
        if query_idx is None:
            return []
        
        # Get query vector
        query_vector = self.movie_vectors[query_idx]
        
        # Calculate similarities
        similarities = []
        for idx, movie_vector in enumerate(self.movie_vectors):
            if idx != query_idx:  # Don't include the query movie itself
                similarity = cosine_similarity(query_vector, movie_vector)
                similarities.append((idx, similarity))
        
        # Sort by similarity and get top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in similarities[:top_k]:
            results.append((self.movies[idx], score))
        
        return results
    
    def search_by_description(self, query_text: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for movies similar to a text description.
        
        Args:
            query_text: Description to search for
            top_k: Number of results to return
            
        Returns:
            List of (movie, similarity_score) tuples
        """
        if not self.fitted:
            raise ValueError("Vector search must be fitted before use")
        
        # Transform query text
        query_vector = self.vectorizer.transform([query_text])[0]
        
        # Calculate similarities
        similarities = []
        for idx, movie_vector in enumerate(self.movie_vectors):
            similarity = cosine_similarity(query_vector, movie_vector)
            similarities.append((idx, similarity))
        
        # Sort by similarity and get top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in similarities[:top_k]:
            if score > 0:  # Only include movies with positive similarity
                results.append((self.movies[idx], score))
        
        return results
