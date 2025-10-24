import httpx
import json
import logging
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class SaptivaLLMClient:
    def __init__(self):
        self.api_key = settings.SAPTIVA_API_KEY
        self.api_url = settings.SAPTIVA_API_URL
        self.timeout = 30.0
    
    def generate_response(self, prompt: str, context: str = "") -> Optional[str]:
        """Generate a response using Saptiva OPS API"""
        if not self.api_key:
            logger.error("Saptiva API key not configured")
            return None
        
        # Build the full prompt with context
        full_prompt = self._build_prompt(prompt, context)
        
        # Prepare the request payload
        payload = {
            "model": "gpt-3.5-turbo",  # Adjust based on Saptiva's available models
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un asistente médico especializado. Responde preguntas médicas basándote en la información proporcionada. Si no tienes suficiente información, indica que necesitas más contexto."
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    logger.info("Successfully generated response from Saptiva OPS")
                    return content
                else:
                    logger.error(f"Unexpected response format: {result}")
                    return None
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error calling Saptiva OPS: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request error calling Saptiva OPS: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling Saptiva OPS: {e}")
            return None
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build the full prompt with context"""
        if context:
            return f"""Contexto médico relevante:
{context}

Pregunta: {question}

Por favor, responde la pregunta basándote en el contexto proporcionado. Si el contexto no contiene información suficiente para responder completamente, indica qué información adicional necesitas."""
        else:
            return f"""Pregunta médica: {question}

Por favor, proporciona una respuesta médica profesional. Si no tienes suficiente información para responder completamente, indica qué información adicional necesitas."""
    
    def test_connection(self) -> bool:
        """Test the connection to Saptiva OPS API"""
        try:
            test_prompt = "Test connection"
            response = self.generate_response(test_prompt)
            return response is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

# Global instance
llm_client = SaptivaLLMClient()

