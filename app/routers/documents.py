import os
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from app.models import DocumentUploadResponse, ErrorResponse
from app.services.ingest import document_processor
from app.services.vectorstore import vectorstore
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a medical document"""
    
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not supported. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
        )
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Uploaded file: {file.filename}")
        
        # Process the document
        result = document_processor.process_document(file_path, file.filename)
        
        # Store chunks in vector database
        success = vectorstore.add_documents(result["chunks"])
        
        if not success:
            # Clean up uploaded file if storage failed
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store document in vector database"
            )
        
        # Clean up uploaded file (optional - you might want to keep it)
        os.remove(file_path)
        
        logger.info(f"Successfully processed document: {file.filename}")
        
        return DocumentUploadResponse(
            document_id=result["document_id"],
            filename=file.filename,
            chunks_created=result["total_chunks"],
            message=f"Document '{file.filename}' processed successfully with {result['total_chunks']} chunks"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {e}")
        
        # Clean up file if it exists
        file_path = f"data/{file.filename}"
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )

@router.get("/{document_id}/summary")
async def get_document_summary(document_id: str):
    """Get summary information about a document"""
    try:
        from app.services.rag import rag_pipeline
        summary = rag_pipeline.get_document_summary(document_id)
        return summary
    except Exception as e:
        logger.error(f"Error getting document summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving document summary: {str(e)}"
        )

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and all its chunks"""
    try:
        success = vectorstore.delete_document(document_id)
        
        if success:
            return {"message": f"Document {document_id} deleted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete document"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}"
        )

@router.get("/stats")
async def get_document_stats():
    """Get statistics about stored documents"""
    try:
        stats = vectorstore.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting document stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving document stats: {str(e)}"
        )

