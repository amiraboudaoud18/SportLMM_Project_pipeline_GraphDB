# config_cinema.py
"""
Configuration for Cinema Chatbot - French Movies
Local LLM Only (LM Studio)
"""

from dotenv import load_dotenv

load_dotenv()

# ========================================
# LLM CONFIGURATION
# ========================================

# LOCAL LLM ONLY
USE_LOCAL_LLM = True  # Always True for this project

# Local LLM (LM Studio) settingsll
LOCAL_LLM_ENDPOINT = "http://localhost:1234/v1"
LOCAL_LLM_MODEL = "Meta-Llama-3.1-8B-Instruct-GGUF"  


# LLM parameters
LLM_TEMPERATURE = 0.1  # Lower = more focused/deterministic
LLM_MAX_TOKENS = 2000

# ========================================
# GRAPHDB CONFIGURATION
# ========================================

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/movie-test"

# ========================================
# ONTOLOGY CONFIGURATION - CINEMA
# ========================================

ONTOLOGY_NAMESPACE = "http://exemple.org/cinema#"
ONTOLOGY_FILE = "/mnt/user-data/uploads/cinema-ontologie.owl"

# ========================================
# LANGUAGE CONFIGURATION
# ========================================

DEFAULT_LANGUAGE = "fr"  # French only

# ========================================
# DISPLAY SETTINGS
# ========================================

VERBOSE = True  # Show detailed steps
SHOW_SPARQL = True  # Display generated SPARQL queries
SHOW_CONTEXT = True  # Display context sent to LLM
SHOW_RAW_RESULTS = False  # Show raw GraphDB results

# ========================================
# VALIDATION
# ========================================

def validate_config():
    """Validate configuration"""
    
    errors = []
    
    # Check GraphDB
    if not GRAPHDB_ENDPOINT:
        errors.append(" GraphDB endpoint is required")
    
    # Check language
    if DEFAULT_LANGUAGE not in ['fr', 'en']:
        errors.append(" DEFAULT_LANGUAGE must be 'fr' or 'en'")
    
    if errors:
        print("\n Configuration Errors:")
        for error in errors:
            print(f"   {error}")
        print()
        return False
    
    return True


def print_config():
    """Print current configuration"""
    
    print("\n" + "="*80)
    print(" CONFIGURATION DU CHATBOT CINÉMA")
    print("="*80)
    print("LLM Provider:         Local (LM Studio)")
    print(f"Local Endpoint:      {LOCAL_LLM_ENDPOINT}")
    print(f"Local Model:         {LOCAL_LLM_MODEL}")
    print(f"Language:            {DEFAULT_LANGUAGE.upper()}")
    print(f"GraphDB:             {GRAPHDB_ENDPOINT}")
    print(f"Namespace:           {ONTOLOGY_NAMESPACE}")
    print(f"Temperature:         {LLM_TEMPERATURE}")
    print(f"Max Tokens:          {LLM_MAX_TOKENS}")
    print("="*80 + "\n")


if __name__ == "__main__":
    print_config()
    
    if validate_config():
        print(" Configuration valide!")
    else:
        print(" Configuration invalide - corrigez les erreurs ci-dessus")
