import os
import uuid
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pypdf
from docx import Document
from sentence_transformers import SentenceTransformer
from app.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info(f"Loaded embedding model: {settings.EMBEDDING_MODEL}")
    
    def process_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Process a document and return chunks with embeddings"""
        try:
            # Extract text based on file type
            text = self._extract_text(file_path, filename)
            if not text:
                raise ValueError("Could not extract text from document")
            
            # Generate document ID
            document_id = str(uuid.uuid4())
            
            # Chunk the text
            chunks = self._chunk_text(text, document_id, filename)
            
            # Generate embeddings for each chunk
            chunk_texts = [chunk["content"] for chunk in chunks]
            embeddings = self.embedding_model.encode(chunk_texts).tolist()
            
            # Add embeddings to chunks
            for i, chunk in enumerate(chunks):
                chunk["vector"] = embeddings[i]
            
            logger.info(f"Processed document {filename}: {len(chunks)} chunks created")
            
            return {
                "document_id": document_id,
                "filename": filename,
                "chunks": chunks,
                "total_chunks": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            raise
    
    def _extract_text(self, file_path: str, filename: str) -> str:
        """Extract text from different file types"""
        file_ext = Path(filename).suffix.lower()
        
        try:
            if file_ext == ".pdf":
                return self._extract_pdf_text(file_path)
            elif file_ext == ".txt":
                return self._extract_txt_text(file_path)
            elif file_ext == ".docx":
                return self._extract_docx_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}")
            raise
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    def _extract_txt_text(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    def _chunk_text(self, text: str, document_id: str, filename: str) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks"""
        chunks = []
        chunk_size = settings.CHUNK_SIZE
        chunk_overlap = settings.CHUNK_OVERLAP
        
        # Split text into sentences for better chunking
        sentences = self._split_into_sentences(text)
        
        current_chunk = ""
        chunk_index = 0
        
        for i, sentence in enumerate(sentences):
            # If adding this sentence would exceed chunk size, save current chunk
            if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
                chunks.append(self._create_chunk(
                    current_chunk.strip(),
                    document_id,
                    filename,
                    chunk_index
                ))
                chunk_index += 1
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk, chunk_overlap)
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(self._create_chunk(
                current_chunk.strip(),
                document_id,
                filename,
                chunk_index
            ))
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        import re
        # Simple sentence splitting - can be improved with more sophisticated NLP
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_overlap_text(self, text: str, overlap_size: int) -> str:
        """Get the last part of text for overlap"""
        if len(text) <= overlap_size:
            return text
        return text[-overlap_size:].strip()
    
    def _create_chunk(self, content: str, document_id: str, filename: str, chunk_index: int) -> Dict[str, Any]:
        """Create a chunk dictionary"""
        return {
            "content": content,
            "document_id": document_id,
            "filename": filename,
            "chunk_index": chunk_index,
            "metadata": {
                "chunk_size": len(content),
                "created_at": "2024-01-01T00:00:00Z"  # Could add timestamp
            }
        }

# Global instance
document_processor = DocumentProcessor()

