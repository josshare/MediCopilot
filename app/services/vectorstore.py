import weaviate
from typing import List, Dict, Any, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class WeaviateClient:
    def __init__(self):
        self.client = None
        self.class_name = "DocumentChunk"
        self._connect()
        self._create_schema()
    
    def _connect(self):
        """Connect to Weaviate instance"""
        try:
            self.client = weaviate.Client(
                url=settings.WEAVIATE_URL,
                timeout_config=(5, 15)
            )
            logger.info(f"Connected to Weaviate at {settings.WEAVIATE_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate: {e}")
            raise
    
    def _create_schema(self):
        """Create the document chunk schema in Weaviate"""
        if self.client.schema.exists(self.class_name):
            logger.info(f"Schema {self.class_name} already exists")
            return
        
        schema = {
            "class": self.class_name,
            "description": "Medical document chunks for RAG",
            "vectorizer": "none",  # We'll provide our own vectors
            "properties": [
                {
                    "name": "content",
                    "dataType": ["text"],
                    "description": "The text content of the chunk"
                },
                {
                    "name": "document_id",
                    "dataType": ["string"],
                    "description": "ID of the source document"
                },
                {
                    "name": "filename",
                    "dataType": ["string"],
                    "description": "Original filename"
                },
                {
                    "name": "chunk_index",
                    "dataType": ["int"],
                    "description": "Index of this chunk in the document"
                },
                {
                    "name": "metadata",
                    "dataType": ["object"],
                    "description": "Additional metadata about the chunk"
                }
            ]
        }
        
        try:
            self.client.schema.create_class(schema)
            logger.info(f"Created schema {self.class_name}")
        except Exception as e:
            logger.error(f"Failed to create schema: {e}")
            raise
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> bool:
        """Add document chunks to Weaviate"""
        try:
            with self.client.batch as batch:
                for chunk in chunks:
                    batch.add_data_object(
                        data_object={
                            "content": chunk["content"],
                            "document_id": chunk["document_id"],
                            "filename": chunk["filename"],
                            "chunk_index": chunk["chunk_index"],
                            "metadata": chunk["metadata"]
                        },
                        class_name=self.class_name,
                        vector=chunk["vector"]
                    )
            logger.info(f"Added {len(chunks)} chunks to Weaviate")
            return True
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def search_similar(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks using vector similarity"""
        try:
            result = (
                self.client.query
                .get(self.class_name, ["content", "document_id", "filename", "chunk_index", "metadata"])
                .with_near_vector({"vector": query_vector})
                .with_limit(limit)
                .do()
            )
            
            chunks = []
            if "data" in result and "Get" in result["data"]:
                for item in result["data"]["Get"][self.class_name]:
                    chunks.append({
                        "content": item["content"],
                        "document_id": item["document_id"],
                        "filename": item["filename"],
                        "chunk_index": item["chunk_index"],
                        "metadata": item["metadata"],
                        "distance": item.get("_additional", {}).get("distance", 0)
                    })
            
            logger.info(f"Found {len(chunks)} similar chunks")
            return chunks
        except Exception as e:
            logger.error(f"Failed to search similar documents: {e}")
            return []
    
    def get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """Get all chunks for a specific document"""
        try:
            result = (
                self.client.query
                .get(self.class_name, ["content", "document_id", "filename", "chunk_index", "metadata"])
                .with_where({
                    "path": ["document_id"],
                    "operator": "Equal",
                    "valueString": document_id
                })
                .do()
            )
            
            chunks = []
            if "data" in result and "Get" in result["data"]:
                for item in result["data"]["Get"][self.class_name]:
                    chunks.append({
                        "content": item["content"],
                        "document_id": item["document_id"],
                        "filename": item["filename"],
                        "chunk_index": item["chunk_index"],
                        "metadata": item["metadata"]
                    })
            
            return chunks
        except Exception as e:
            logger.error(f"Failed to get document chunks: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """Delete all chunks for a specific document"""
        try:
            result = (
                self.client.query
                .get(self.class_name, ["id"])
                .with_where({
                    "path": ["document_id"],
                    "operator": "Equal",
                    "valueString": document_id
                })
                .do()
            )
            
            if "data" in result and "Get" in result["data"]:
                for item in result["data"]["Get"][self.class_name]:
                    self.client.data_object.delete(
                        uuid=item["id"],
                        class_name=self.class_name
                    )
            
            logger.info(f"Deleted document {document_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            result = self.client.query.aggregate(self.class_name).with_meta_count().do()
            count = result["data"]["Aggregate"][self.class_name][0]["meta"]["count"]
            return {"total_chunks": count}
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"total_chunks": 0}

# Global instance
vectorstore = WeaviateClient()

