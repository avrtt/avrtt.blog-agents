# agents/vector_search/lancedb_client.py
"""
LanceDB client for vector search capabilities
"""
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    import lancedb
    import numpy as np
    from sentence_transformers import SentenceTransformer
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    print("LanceDB not available - install with: pip install lancedb sentence-transformers")

class VectorSearchClient:
    """Client for vector search operations"""
    
    def __init__(self, db_path: str = "vector_db"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        if not LANCEDB_AVAILABLE:
            self.db = None
            self.model = None
            return
        
        try:
            # Initialize LanceDB
            self.db = lancedb.connect(self.db_path)
            
            # Load embedding model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create tables if they don't exist
            self._ensure_tables()
            
        except Exception as e:
            print(f"Error initializing LanceDB: {e}")
            self.db = None
            self.model = None
    
    def _ensure_tables(self):
        """Ensure required tables exist"""
        if not self.db:
            return
        
        # Posts table
        if "posts" not in self.db.table_names():
            schema = {
                "id": "string",
                "title": "string", 
                "content": "string",
                "url": "string",
                "embedding": "float32[384]",
                "metadata": "string"
            }
            self.db.create_table("posts", schema=schema)
        
        # Sources table
        if "sources" not in self.db.table_names():
            schema = {
                "id": "string",
                "url": "string",
                "title": "string",
                "content": "string", 
                "embedding": "float32[384]",
                "metadata": "string"
            }
            self.db.create_table("sources", schema=schema)
    
    def add_post(self, post_id: str, title: str, content: str, url: str, metadata: Dict = None):
        """Add a blog post to the vector database"""
        if not self.db or not self.model:
            print("LanceDB not available")
            return False
        
        try:
            # Generate embedding
            text = f"{title} {content}"
            embedding = self.model.encode(text).tolist()
            
            # Prepare data
            data = {
                "id": post_id,
                "title": title,
                "content": content[:1000],  # Limit content length
                "url": url,
                "embedding": embedding,
                "metadata": json.dumps(metadata or {})
            }
            
            # Insert into table
            table = self.db.open_table("posts")
            table.add([data])
            
            return True
            
        except Exception as e:
            print(f"Error adding post: {e}")
            return False
    
    def add_source(self, source_id: str, url: str, title: str, content: str, metadata: Dict = None):
        """Add a source to the vector database"""
        if not self.db or not self.model:
            print("LanceDB not available")
            return False
        
        try:
            # Generate embedding
            text = f"{title} {content}"
            embedding = self.model.encode(text).tolist()
            
            # Prepare data
            data = {
                "id": source_id,
                "url": url,
                "title": title,
                "content": content[:1000],  # Limit content length
                "embedding": embedding,
                "metadata": json.dumps(metadata or {})
            }
            
            # Insert into table
            table = self.db.open_table("sources")
            table.add([data])
            
            return True
            
        except Exception as e:
            print(f"Error adding source: {e}")
            return False
    
    def search_posts(self, query: str, limit: int = 5) -> List[Dict]:
        """Search posts by similarity"""
        if not self.db or not self.model:
            print("LanceDB not available")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query).tolist()
            
            # Search table
            table = self.db.open_table("posts")
            results = table.search(query_embedding).limit(limit).to_pandas()
            
            # Convert to list of dicts
            posts = []
            for _, row in results.iterrows():
                posts.append({
                    "id": row["id"],
                    "title": row["title"],
                    "content": row["content"],
                    "url": row["url"],
                    "score": row["_distance"],
                    "metadata": json.loads(row["metadata"])
                })
            
            return posts
            
        except Exception as e:
            print(f"Error searching posts: {e}")
            return []
    
    def search_sources(self, query: str, limit: int = 5) -> List[Dict]:
        """Search sources by similarity"""
        if not self.db or not self.model:
            print("LanceDB not available")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.model.encode(query).tolist()
            
            # Search table
            table = self.db.open_table("sources")
            results = table.search(query_embedding).limit(limit).to_pandas()
            
            # Convert to list of dicts
            sources = []
            for _, row in results.iterrows():
                sources.append({
                    "id": row["id"],
                    "url": row["url"],
                    "title": row["title"],
                    "content": row["content"],
                    "score": row["_distance"],
                    "metadata": json.loads(row["metadata"])
                })
            
            return sources
            
        except Exception as e:
            print(f"Error searching sources: {e}")
            return []
    
    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        if not self.db:
            return {"posts": 0, "sources": 0}
        
        try:
            stats = {}
            
            if "posts" in self.db.table_names():
                posts_table = self.db.open_table("posts")
                stats["posts"] = len(posts_table)
            
            if "sources" in self.db.table_names():
                sources_table = self.db.open_table("sources")
                stats["sources"] = len(sources_table)
            
            return stats
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"posts": 0, "sources": 0}

# Global client instance
vector_client = VectorSearchClient()
