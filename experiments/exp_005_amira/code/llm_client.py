# llm_client.py
"""
LLM Client - Handles communication with Language Models
Updated to support multiple specialized LLMs for different tasks
"""

import requests
import time
from typing import Optional
from config import (
    LOCAL_LLM_ENDPOINT,
    LOCAL_LLM_MODEL,
    SPARQL_LLM_MODEL,
    ANSWER_LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    REQUEST_TIMEOUT,
    MAX_RETRIES
)


class LLMClient:
    """Base LLM client for making requests to language models"""
    
    def __init__(
        self,
        endpoint: str = LOCAL_LLM_ENDPOINT,
        model: str = LOCAL_LLM_MODEL,
        temperature: float = LLM_TEMPERATURE,
        max_tokens: int = LLM_MAX_TOKENS
    ):
        """
        Initialize LLM client
        
        Args:
            endpoint: API endpoint URL
            model: Model name
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
        """
        self.endpoint = endpoint
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text from prompt
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            
        Returns:
            Generated text
        """
        # Use provided values or defaults
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Make request with retries
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.endpoint}/chat/completions",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temp,
                        "max_tokens": tokens,
                        "stream": False
                    },
                    timeout=REQUEST_TIMEOUT
                )
                
                response.raise_for_status()
                result = response.json()
                
                return result["choices"][0]["message"]["content"]
            
            except requests.exceptions.Timeout:
                if attempt < MAX_RETRIES - 1:
                    print(f"⚠️  Timeout, retry {attempt + 1}/{MAX_RETRIES}...")
                    time.sleep(2)
                else:
                    raise Exception("LLM request timed out after retries")
            
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"⚠️  Request error, retry {attempt + 1}/{MAX_RETRIES}...")
                    time.sleep(2)
                else:
                    raise Exception(f"LLM request failed: {str(e)}")
        
        raise Exception("Failed to generate response")


class SPARQLLLMClient(LLMClient):
    """
    Specialized LLM client for SPARQL generation
    Uses code-specialized models (Qwen2.5-Coder, DeepSeek-Coder)
    """
    
    def __init__(self):
        """Initialize SPARQL generation LLM"""
        model = SPARQL_LLM_MODEL or LOCAL_LLM_MODEL
        
        print(f"🔧 SPARQL LLM: {model}")
        
        super().__init__(
            endpoint=LOCAL_LLM_ENDPOINT,
            model=model,
            temperature=0.0,  # Very deterministic for SPARQL
            max_tokens=1500   # SPARQL queries are usually short
        )
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate SPARQL query
        
        Uses very low temperature for consistent, structured output
        """
        # Force low temperature for SPARQL (unless explicitly overridden)
        if temperature is None:
            temperature = 0.0
        
        # Add SPARQL-specific system context if not provided
        if not system_prompt:
            system_prompt = """You are an expert in generating SPARQL queries.
You generate valid, syntactically correct SPARQL queries.
You respond ONLY with valid JSON containing the SPARQL query.
You are precise and follow instructions exactly."""
        
        return super().generate(prompt, system_prompt, temperature, max_tokens)


class AnswerLLMClient(LLMClient):
    """
    Specialized LLM client for natural language answer generation
    Uses language models optimized for French (Mistral, Vigogne)
    """
    
    def __init__(self):
        """Initialize answer generation LLM"""
        model = ANSWER_LLM_MODEL or LOCAL_LLM_MODEL
        
        print(f"💬 Answer LLM: {model}")
        
        super().__init__(
            endpoint=LOCAL_LLM_ENDPOINT,
            model=model,
            temperature=0.3,  # More creative for natural language
            max_tokens=2000   # Longer for detailed answers
        )
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate natural language answer in French
        
        Uses slightly higher temperature for more natural, varied responses
        """
        # Use moderate temperature for answers (unless explicitly overridden)
        if temperature is None:
            temperature = 0.3
        
        # Add French-specific system context if not provided
        if not system_prompt:
            system_prompt = """Tu es un assistant expert et bienveillant.
Tu réponds en français de manière claire, naturelle et engageante.
Tu es précis et informatif tout en restant accessible."""
        
        return super().generate(prompt, system_prompt, temperature, max_tokens)


# Legacy class for backward compatibility
class FrenchLLMClient(LLMClient):
    """
    Legacy LLM client - kept for backward compatibility
    Use SPARQLLLMClient or AnswerLLMClient instead
    """
    
    def __init__(self, use_local: bool = True):
        """Initialize French LLM client"""
        if not use_local:
            raise NotImplementedError("Only local LLM is supported")
        
        print("⚠️  Using legacy FrenchLLMClient - consider using specialized clients")
        
        super().__init__(
            endpoint=LOCAL_LLM_ENDPOINT,
            model=LOCAL_LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_sparql_llm() -> SPARQLLLMClient:
    """Get LLM client for SPARQL generation"""
    return SPARQLLLMClient()


def get_answer_llm() -> AnswerLLMClient:
    """Get LLM client for answer generation"""
    return AnswerLLMClient()


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("Testing LLM Clients...\n")
    
    # Test SPARQL LLM
    print("="*80)
    print("1. Testing SPARQL LLM (Code-specialized)")
    print("="*80)
    try:
        sparql_llm = get_sparql_llm()
        
        test_prompt = """Generate a SPARQL query to find all horses.
Respond ONLY with JSON: {"sparql_query": "your query here"}"""
        
        response = sparql_llm.generate(test_prompt)
        print(f"Response: {response[:200]}...")
        print("✅ SPARQL LLM working!\n")
    except Exception as e:
        print(f"❌ SPARQL LLM error: {e}\n")
    
    # Test Answer LLM
    print("="*80)
    print("2. Testing Answer LLM (French language)")
    print("="*80)
    try:
        answer_llm = get_answer_llm()
        
        test_prompt = "Explique en une phrase ce qu'est un cheval."
        
        response = answer_llm.generate(test_prompt)
        print(f"Response: {response}")
        print("✅ Answer LLM working!\n")
    except Exception as e:
        print(f"❌ Answer LLM error: {e}\n")
    
    print("="*80)
    print("✅ All tests complete!")
