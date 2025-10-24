import logging
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from app.services.vectorstore import vectorstore
from app.services.llm import llm_client
from app.config import settings

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info(f"RAG pipeline initialized with model: {settings.EMBEDDING_MODEL}")
    
    def query(self, question: str, max_results: int = 5) -> Dict[str, Any]:
        """Process a query through the RAG pipeline"""
        try:
            # Generate embedding for the question
            question_embedding = self.embedding_model.encode([question])[0].tolist()
            
            # Retrieve relevant chunks
            relevant_chunks = vectorstore.search_similar(
                query_vector=question_embedding,
                limit=max_results
            )
            
            if not relevant_chunks:
                logger.warning("No relevant chunks found for query")
                return {
                    "answer": "No encontré información relevante en los documentos disponibles para responder tu pregunta.",
                    "sources": [],
                    "query": question
                }
            
            # Build context from retrieved chunks
            context = self._build_context(relevant_chunks)
            
            # Generate response using LLM
            answer = llm_client.generate_response(question, context)
            
            if not answer:
                answer = "Lo siento, no pude generar una respuesta en este momento. Por favor, intenta de nuevo."
            
            # Prepare sources
            sources = self._prepare_sources(relevant_chunks)
            
            logger.info(f"Successfully processed query: {len(relevant_chunks)} chunks retrieved")
            
            return {
                "answer": answer,
                "sources": sources,
                "query": question
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return {
                "answer": f"Error procesando la consulta: {str(e)}",
                "sources": [],
                "query": question
            }
    
    def _build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved chunks"""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            source_info = f"Fuente {i}: {chunk['filename']} (fragmento {chunk['chunk_index']})"
            content = chunk['content']
            
            context_parts.append(f"{source_info}\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _prepare_sources(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare source information for the response"""
        sources = []
        
        for chunk in chunks:
            source = {
                "filename": chunk['filename'],
                "chunk_index": chunk['chunk_index'],
                "content_preview": chunk['content'][:200] + "..." if len(chunk['content']) > 200 else chunk['content'],
                "relevance_score": 1 - chunk.get('distance', 0),  # Convert distance to similarity score
                "document_id": chunk['document_id']
            }
            sources.append(source)
        
        return sources
    
    def get_document_summary(self, document_id: str) -> Dict[str, Any]:
        """Get summary information about a document"""
        try:
            chunks = vectorstore.get_document_chunks(document_id)
            
            if not chunks:
                return {
                    "document_id": document_id,
                    "total_chunks": 0,
                    "filename": "Unknown",
                    "status": "not_found"
                }
            
            # Get basic info from first chunk
            first_chunk = chunks[0]
            filename = first_chunk['filename']
            
            # Calculate total content length
            total_content_length = sum(len(chunk['content']) for chunk in chunks)
            
            return {
                "document_id": document_id,
                "filename": filename,
                "total_chunks": len(chunks),
                "total_content_length": total_content_length,
                "status": "available"
            }
            
        except Exception as e:
            logger.error(f"Error getting document summary: {e}")
            return {
                "document_id": document_id,
                "status": "error",
                "error": str(e)
            }

# Global instance
rag_pipeline = RAGPipeline()

