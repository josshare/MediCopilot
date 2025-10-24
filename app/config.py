import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Saptiva OPS API Configuration
    SAPTIVA_API_KEY: str = os.getenv("SAPTIVA_API_KEY", "")
    SAPTIVA_API_URL: str = os.getenv("SAPTIVA_API_URL", "https://api.saptiva.com/v1/chat")
    
    # Weaviate Configuration
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
    
    # Embedding Model
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "MediCopilot")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".txt", ".docx"}
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_RETRIEVAL_RESULTS: int = 5

settings = Settings()

