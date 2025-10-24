# MediCopilot API - Quick Reference

## 🚀 Quick Start

1. **Setup**: `cp env.example .env` → Add your Saptiva API key
2. **Start**: `./start.sh` or `docker-compose up --build`
3. **Test**: `python3 test_setup.py`

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload Document
```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@medical_document.pdf"
```

### Query Medical Question
```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuáles son los efectos secundarios del paracetamol?",
    "max_results": 5
  }'
```

### Get Document Summary
```bash
curl http://localhost:8000/documents/{document_id}/summary
```

### Delete Document
```bash
curl -X DELETE http://localhost:8000/documents/{document_id}
```

### Get Statistics
```bash
curl http://localhost:8000/documents/stats
```

## 🔧 Configuration

### Environment Variables (.env)
```env
SAPTIVA_API_KEY=your_key_here
SAPTIVA_API_URL=https://api.saptiva.com/v1/chat
WEAVIATE_URL=http://weaviate:8080
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## 📊 Response Examples

### Upload Response
```json
{
  "document_id": "uuid-here",
  "filename": "document.pdf",
  "chunks_created": 15,
  "message": "Document processed successfully"
}
```

### Query Response
```json
{
  "answer": "Basándome en los documentos...",
  "sources": [
    {
      "filename": "document.pdf",
      "chunk_index": 3,
      "content_preview": "Efectos secundarios...",
      "relevance_score": 0.95,
      "document_id": "uuid-here"
    }
  ],
  "query": "¿Efectos secundarios del paracetamol?",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build --force-recreate
```

## 🔍 Troubleshooting

### Services not starting
```bash
# Check Docker is running
docker --version
docker-compose --version

# Check ports are free
lsof -i :8000
lsof -i :8080
```

### API errors
```bash
# Check API logs
docker-compose logs api

# Check Weaviate logs
docker-compose logs weaviate
```

### Memory issues
```bash
# Clean up Docker
docker system prune -a
docker-compose down
docker-compose up --build
```

## 📖 Full Documentation

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Weaviate Console**: http://localhost:8080

