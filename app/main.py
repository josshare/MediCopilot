import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.config import settings
from app.models import HealthResponse, ErrorResponse
from app.routers import documents, query
from app.services.vectorstore import vectorstore
from app.services.llm import llm_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Asistente médico de nueva generación con RAG",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(query.router)

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with basic information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Asistente médico de nueva generación con RAG",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "upload": "/documents/upload",
            "query": "/query/"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check Weaviate connection
        weaviate_status = "ok" if vectorstore.client.is_ready() else "error"
        
        # Check LLM connection
        llm_status = "ok" if llm_client.test_connection() else "error"
        
        # Overall status
        overall_status = "healthy" if weaviate_status == "ok" and llm_status == "ok" else "unhealthy"
        
        return HealthResponse(
            status=overall_status,
            weaviate_status=weaviate_status,
            api_status="ok",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            weaviate_status="error",
            api_status="error",
            timestamp=datetime.now()
        )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "detail": f"The requested endpoint {request.url.path} was not found",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

