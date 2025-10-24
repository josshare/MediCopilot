import logging
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from app.models import QueryRequest, QueryResponse, ErrorResponse
from app.services.rag import rag_pipeline

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/query", tags=["query"])

@router.post("/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the medical documents using RAG"""
    
    if not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty"
        )
    
    try:
        # Process the query through RAG pipeline
        result = rag_pipeline.query(
            question=request.question,
            max_results=request.max_results or 5
        )
        
        logger.info(f"Processed query: {request.question[:50]}...")
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            query=result["query"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/health")
async def query_health():
    """Check if the query service is healthy"""
    try:
        # Test LLM connection
        from app.services.llm import llm_client
        llm_healthy = llm_client.test_connection()
        
        # Test vector store
        from app.services.vectorstore import vectorstore
        vectorstore_healthy = vectorstore.client.is_ready()
        
        return {
            "status": "healthy" if llm_healthy and vectorstore_healthy else "unhealthy",
            "llm_connection": "ok" if llm_healthy else "error",
            "vectorstore_connection": "ok" if vectorstore_healthy else "error",
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now()
        }

