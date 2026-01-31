# llm_client.py
"""
LLM Client supporting both Local (LM Studio) and OpenAI
Optimized for French language support
"""

import os
import requests
import json
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Unified LLM client for local and cloud models"""
    
    def __init__(
        self,
        use_local: bool = True,
        local_endpoint: str = "http://localhost:1234/v1",
        local_model: str = "meta-llama-3.1-8b-instruct",
        openai_model: str = "gpt-4",
        temperature: float = 0.1,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM client
        
        Args:
            use_local: If True, use local LM Studio; if False, use OpenAI
            local_endpoint: LM Studio API endpoint
            local_model: Model name in LM Studio
            openai_model: OpenAI model name
            temperature: Lower = more focused, higher = more creative
            max_tokens: Maximum tokens in response
        """
        self.use_local = use_local
        self.local_endpoint = local_endpoint
        self.local_model = local_model
        self.openai_model = openai_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Setup OpenAI if needed
        if not use_local:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text using LLM
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
        """
        if self.use_local:
            return self._generate_local(prompt, system_prompt)
        else:
            return self._generate_openai(prompt, system_prompt)
    
    def _generate_local(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate using local LM Studio"""
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(
                f"{self.local_endpoint}/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": self.local_model,
                    "messages": messages,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "stream": False
                },
                timeout=120  # 2 minutes timeout for local models
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            print(f" Error calling local LLM: {e}")
            print(" Make sure LM Studio server is running on http://localhost:1234")
            return ""
        except (KeyError, json.JSONDecodeError) as e:
            print(f" Error parsing response: {e}")
            return ""
    
    def _generate_openai(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate using OpenAI API"""
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f" Error calling OpenAI: {e}")
            return ""


class FrenchLLMClient(LLMClient):
    """
    Specialized LLM client optimized for French language
    """
    
    def __init__(self, use_local: bool = True, **kwargs):
        """
        Initialize French-optimized LLM
        
        Recommended models:
        - Local: vigogne, croissant-llm, or multilingual models
        - OpenAI: gpt-4 (best French support)
        """
        super().__init__(use_local=use_local, **kwargs)
        
        # Add French-specific system context
        self.french_system_context = """Tu es un assistant expert en analyse de données équestres.
Tu réponds toujours en français, de manière claire et précise.
Tu utilises une ontologie RDF pour interroger une base de connaissances sur les chevaux, cavaliers, et entraînements."""
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate with French context"""
        
        # Combine system prompts
        if system_prompt:
            combined_system = f"{self.french_system_context}\n\n{system_prompt}"
        else:
            combined_system = self.french_system_context
        
        return super().generate(prompt, combined_system)


# Test
if __name__ == "__main__":
    print("Testing LLM Client...")
    
    # Test local
    print("\n Testing Local LM Studio...")
    local_client = FrenchLLMClient(use_local=True)
    test_prompt = "Dis bonjour en français"
    response = local_client.generate(test_prompt)
    print(f"Response: {response[:100]}...")
    
    print("\n LLM Client ready!")
