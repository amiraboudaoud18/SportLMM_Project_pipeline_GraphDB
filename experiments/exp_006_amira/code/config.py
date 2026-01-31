# config.py
"""
Configuration Module - Equestrian Knowledge Graph Chatbot
Updated to support specialized LLMs for different tasks
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# LLM CONFIGURATION (UPDATED FOR DUAL-LLM SETUP)
# ============================================================================

USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
LOCAL_LLM_ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:1234/v1")

# Primary model (fallback if specialized models not specified)
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "Qwen2.5-Coder-14B-Instruct")

# Specialized models for different tasks
SPARQL_LLM_MODEL = os.getenv("SPARQL_LLM_MODEL", "")  # Code-specialized for SPARQL generation
ANSWER_LLM_MODEL = os.getenv("ANSWER_LLM_MODEL", "")  # Language model for French answers

LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# ============================================================================
# GRAPHDB CONFIGURATION
# ============================================================================

GRAPHDB_ENDPOINT = os.getenv(
    "GRAPHDB_ENDPOINT", 
    "http://localhost:7200/repositories/equestrian-kg"
)

ONTOLOGY_GRAPH = os.getenv("ONTOLOGY_GRAPH", "")
INSTANCES_GRAPH = os.getenv("INSTANCES_GRAPH", "")

# ============================================================================
# ONTOLOGY CONFIGURATION
# ============================================================================

ONTOLOGY_NAMESPACE = os.getenv(
    "ONTOLOGY_NAMESPACE",
    "http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#"
)

BASE_URI = os.getenv("BASE_URI", "http://example.org/horse-ontology#")

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "fr")
VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"
SHOW_SPARQL = os.getenv("SHOW_SPARQL", "true").lower() == "true"
SHOW_CONTEXT = os.getenv("SHOW_CONTEXT", "false").lower() == "true"

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "false").lower() == "true"

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/chatbot.log")

Path("logs").mkdir(exist_ok=True)

# ============================================================================
# FUNCTIONS
# ============================================================================

def validate_config():
    """Validate configuration"""
    errors = []
    
    if USE_LOCAL_LLM:
        if not LOCAL_LLM_ENDPOINT:
            errors.append("LOCAL_LLM_ENDPOINT is not set")
        if not LOCAL_LLM_MODEL and not (SPARQL_LLM_MODEL and ANSWER_LLM_MODEL):
            errors.append("Either LOCAL_LLM_MODEL or both SPARQL_LLM_MODEL and ANSWER_LLM_MODEL must be set")
    
    if not GRAPHDB_ENDPOINT:
        errors.append("GRAPHDB_ENDPOINT is not set")
    
    if not ONTOLOGY_NAMESPACE:
        errors.append("ONTOLOGY_NAMESPACE is not set")
    
    if DEFAULT_LANGUAGE not in ['fr', 'en']:
        errors.append("DEFAULT_LANGUAGE must be 'fr' or 'en'")
    
    if errors:
        print("\n Configuration Errors:")
        for error in errors:
            print(f"   • {error}")
        print()
        return False
    
    return True


def print_config():
    """Print current configuration"""
    print("\n" + "="*80)
    print(" EQUESTRIAN CHATBOT - CONFIGURATION")
    print("="*80)
    
    print("\n LLM Settings:")
    print(f"   Provider:        {'🖥️  Local (LM Studio)' if USE_LOCAL_LLM else '☁️  OpenAI'}")
    if USE_LOCAL_LLM:
        print(f"   Endpoint:        {LOCAL_LLM_ENDPOINT}")
        print(f"   Primary Model:   {LOCAL_LLM_MODEL}")
        
        # Show specialized models if configured
        if SPARQL_LLM_MODEL or ANSWER_LLM_MODEL:
            print("\n   Specialized Models:")
            print(f"      SPARQL Gen:   {SPARQL_LLM_MODEL or LOCAL_LLM_MODEL} (code-specialized)")
            print(f"      Answer Gen:   {ANSWER_LLM_MODEL or LOCAL_LLM_MODEL} (language model)")
        
    print(f"\n   Temperature:     {LLM_TEMPERATURE}")
    print(f"   Max Tokens:      {LLM_MAX_TOKENS}")
    
    print("\n GraphDB Settings:")
    print(f"   Endpoint:        {GRAPHDB_ENDPOINT}")
    if ONTOLOGY_GRAPH:
        print(f"   Ontology Graph:  {ONTOLOGY_GRAPH}")
    if INSTANCES_GRAPH:
        print(f"   Instances Graph: {INSTANCES_GRAPH}")
    
    print("\n Ontology Settings:")
    print(f"   Namespace:       {ONTOLOGY_NAMESPACE}")
    
    print("\n Application:")
    print(f"   Language:        {DEFAULT_LANGUAGE.upper()}")
    print(f"   Verbose:         {'✅' if VERBOSE else '❌'}")
    print(f"   Show SPARQL:     {'✅' if SHOW_SPARQL else '❌'}")
    
    print("="*80 + "\n")


def get_sparql_prefixes():
    """Generate SPARQL prefixes"""
    return f"""
PREFIX horses: <{ONTOLOGY_NAMESPACE}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""


def get_active_models():
    """Get information about active models"""
    return {
        'sparql_model': SPARQL_LLM_MODEL or LOCAL_LLM_MODEL,
        'answer_model': ANSWER_LLM_MODEL or LOCAL_LLM_MODEL,
        'using_specialized': bool(SPARQL_LLM_MODEL and ANSWER_LLM_MODEL)
    }


if __name__ == "__main__":
    print_config()
    
    if validate_config():
        print(" Configuration is valid!")
        
        models = get_active_models()
        if models['using_specialized']:
            print("\n Using specialized models:")
            print(f"   • SPARQL: {models['sparql_model']}")
            print(f"   • Answer: {models['answer_model']}")
        else:
            print(f"\n Using single model for both tasks: {models['sparql_model']}")
            print("   Consider configuring specialized models for better performance!")
    else:
        print("Configuration has errors")
