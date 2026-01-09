# COMPLETE SYSTEM DOCUMENTATION
## Equestrian Knowledge Graph Chatbot - File-by-File Explanation

---

## 🎯 SYSTEM OVERVIEW

Your GraphRAG system works like this:

```
Question → LLM generates SPARQL → Query GraphDB → Format results → LLM answers
```

**Key Innovation**: Instead of hardcoded rules, the LLM intelligently generates SPARQL queries by understanding your ontology structure.

---

## 📁 FILE 1: `.env`

### **Purpose:**
Stores all configuration as environment variables (passwords, endpoints, settings)

### **Why it exists:**
- ✅ Keeps sensitive data out of code
- ✅ Easy to change settings without modifying code
- ✅ Different configs for dev/test/prod

### **What it contains:**
- LM Studio endpoint and model name
- GraphDB connection details
- Named graph URIs
- Ontology namespace
- Display settings (verbose, show SPARQL, etc.)

### **How it's used:**
```python
# Other files import from config.py, which reads .env
from config import GRAPHDB_ENDPOINT, LOCAL_LLM_MODEL
```

### **Key Settings:**
```bash
LOCAL_LLM_MODEL=Meta-Llama-3.1-8B-Instruct-GGUF  # Your model
GRAPHDB_ENDPOINT=http://localhost:7200/repositories/horse-knowledge-graph
ONTOLOGY_NAMESPACE=http://.../Horses#  # From your ontology.owl
```

---

## 📁 FILE 2: `config.py`

### **Purpose:**
Central configuration hub - loads .env and provides settings to all other modules

### **Why it exists:**
- Single source of truth for all settings
- Validates configuration on startup
- Generates SPARQL prefixes automatically
- Easy to check current config

### **What it does:**
1. **Loads .env file** using `python-dotenv`
2. **Provides default values** if variables missing
3. **Validates settings** (checks if endpoints exist, etc.)
4. **Exports settings** for other modules
5. **Generates SPARQL prefixes** based on namespace

### **Key Functions:**

```python
validate_config()  # Checks if everything is set correctly
print_config()     # Displays current configuration
get_sparql_prefixes()  # Returns SPARQL PREFIX declarations
```

### **How it's used:**
```python
# At the top of other files:
from config import (
    GRAPHDB_ENDPOINT,
    LOCAL_LLM_MODEL,
    ONTOLOGY_NAMESPACE,
    get_sparql_prefixes
)
```

### **What it provides:**
- LLM settings (endpoint, model, temperature)
- GraphDB settings (endpoint, named graphs)
- Ontology settings (namespace, base URI)
- Application settings (language, verbose mode)

---

## 📁 FILE 3: `llm_client.py`

### **Purpose:**
Handles ALL communication with the LLM (LM Studio or OpenAI)

### **Why it exists:**
- Abstracts LLM communication from business logic
- Works with both local (LM Studio) and cloud (OpenAI) LLMs
- Optimized for French language
- Single place to handle errors/retries

### **What it does:**

**Main Class: `LLMClient`**
```python
class LLMClient:
    def __init__(self, use_local=True):
        # Connects to LM Studio or OpenAI
        
    def generate(self, prompt, system_prompt=None):
        # Sends prompt to LLM, returns response
```

**Specialized Class: `FrenchLLMClient`**
```python
class FrenchLLMClient(LLMClient):
    # Adds French-specific system prompts
    # Optimized for French responses
```

### **How it works:**

**For LM Studio (local):**
```python
# Sends HTTP POST to http://localhost:1234/v1/chat/completions
response = requests.post(endpoint, json={
    "model": "Meta-Llama-3.1-8B-Instruct-GGUF",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "temperature": 0.1
})
```

**For OpenAI:**
```python
# Uses OpenAI Python library
response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=[...]
)
```

### **Key Features:**
- ✅ Automatic retries on failure
- ✅ Timeout handling
- ✅ Error messages in French
- ✅ Temperature control
- ✅ Token limit management

### **Used by:**
- `intelligent_sparql_generator.py` (to generate SPARQL)
- `intelligent_chatbot.py` (to generate final answers)

---

## 📁 FILE 4: `graphdb_client.py`

### **Purpose:**
Handles ALL communication with GraphDB (your knowledge graph database)

### **Why it exists:**
- Executes SPARQL queries on GraphDB
- Handles connection errors
- Formats results consistently
- Provides helper methods for common queries

### **What it does:**

**Main Class: `GraphDBClient`**
```python
class GraphDBClient:
    def __init__(self, endpoint):
        # Connects to GraphDB
        self.endpoint = endpoint
        
    def query(self, sparql_query):
        # Executes SPARQL query
        # Returns JSON results
```

### **How it works:**

```python
# 1. Takes a SPARQL query
sparql_query = """
PREFIX horses: <...>
SELECT ?horse ?name
WHERE {
    ?horse rdf:type horses:Horse .
    ?horse horses:hasName ?name .
}
"""

# 2. Sends HTTP request to GraphDB
response = requests.post(
    "http://localhost:7200/repositories/horse-knowledge-graph",
    data=sparql_query,
    headers={"Accept": "application/sparql-results+json"}
)

# 3. Returns results as Python dict
return response.json()
```

### **Result Format:**
```json
{
  "results": {
    "bindings": [
      {
        "horse": {"value": "http://.../Thunder"},
        "name": {"value": "Thunder"}
      },
      ...
    ]
  }
}
```

### **Key Features:**
- ✅ Connection error handling
- ✅ Query timeout handling
- ✅ Named graph support (for your ontology/instances separation)
- ✅ Helper methods (get_all_horses, count_entities, etc.)

### **Used by:**
- `intelligent_chatbot.py` (to execute SPARQL queries)

---

## 📁 FILE 5: `intelligent_sparql_generator.py`

### **Purpose:**
**THE BRAIN** - Uses LLM to generate SPARQL queries from natural language questions

### **Why it exists:**
This is the KEY innovation! Instead of:
- ❌ Hardcoded rules (if question contains "horse" → use this query)
- ❌ Question classifier (classify into types)

We use:
- ✅ LLM intelligence to generate custom SPARQL for ANY question
- ✅ Few-shot learning (teach by examples)
- ✅ Ontology-aware (knows your classes and properties)

### **What it does:**

**Main Class: `IntelligentSPARQLGenerator`**
```python
class IntelligentSPARQLGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.ontology_summary = self._create_ontology_summary()
        
    def generate_sparql(self, question):
        # Takes question, returns SPARQL + metadata
```

### **How it works:**

**Step 1: Create Ontology Summary**
```python
ontology_summary = """
# Your Ontology Structure:
Classes:
- Horse (hasName, hasRace, hasHeight, hasWeight)
- Rider (hasName)
- Training (hasDate, Intensity, Frequency)

Relations:
- hasParticipatedTo (Horse → Training)
- AssociatedWith (Horse ↔ Rider)
- isAttachedTo (Horse → Sensor)

Examples of data:
- Horse "Thunder" participated in "Dressage Training"
- Omar Sy rides horse "Lightning"
"""
```

**Step 2: Build Prompt for LLM**
```python
prompt = f"""
You are a SPARQL expert for equestrian ontology.

ONTOLOGY STRUCTURE:
{ontology_summary}

USER QUESTION: {question}

TASK: Generate a SPARQL query to answer this question.

EXAMPLES:
Question: "Quels chevaux participent à des entraînements?"
SPARQL:
PREFIX horses: <...>
SELECT ?horse ?name ?training
WHERE {{
    ?horse rdf:type horses:Horse .
    ?horse horses:hasParticipatedTo ?training .
    ?horse horses:hasName ?name .
}}

[... more examples from your 10 questions ...]

Now generate SPARQL for: {question}

Respond ONLY with JSON:
{{
    "sparql_query": "...",
    "entities_used": ["Horse", "Training"],
    "relations_used": ["hasParticipatedTo"],
    "explanation": "Finds horses linked to trainings"
}}
"""
```

**Step 3: Send to LLM**
```python
llm_response = self.llm.generate(prompt)
```

**Step 4: Parse Response**
```python
result = json.loads(llm_response)
# Returns: {sparql_query, entities_used, relations_used, explanation}
```

### **Key Features:**
- ✅ **Few-Shot Learning**: Uses your 10 questions as examples
- ✅ **Ontology Aware**: Knows your classes/properties
- ✅ **Adaptive**: Works with any question
- ✅ **Explainable**: Returns which entities/relations it used
- ✅ **Handles Named Graphs**: Generates queries for your GraphDB setup

### **This is where you'll improve the system:**
- Add more examples from your 10 questions
- Fine-tune the ontology summary
- Add constraints (OPTIONAL clauses, FILTERs)

---

## 📁 FILE 6: `context_builder.py`

### **Purpose:**
Formats raw SPARQL results into readable text for the LLM

### **Why it exists:**
SPARQL returns this:
```json
{
  "horse": {"value": "http://example.org/Horse123"},
  "name": {"value": "Thunder"},
  "race": {"value": "Arabian"}
}
```

But the LLM needs this:
```
Cheval: Thunder
Race: Arabian
```

### **What it does:**

**Main Class: `ContextBuilder`**
```python
class ContextBuilder:
    def format_results(self, sparql_results, question_type):
        # Takes raw SPARQL results
        # Returns human-readable text
```

### **How it works:**

**Input (from GraphDB):**
```json
{
  "results": {
    "bindings": [
      {"horse": {"value": "..."}, "name": {"value": "Thunder"}},
      {"horse": {"value": "..."}, "name": {"value": "Lightning"}}
    ]
  }
}
```

**Output (for LLM):**
```
Données trouvées (2 résultats):

Résultat 1:
  - horse: Horse123
  - name: Thunder
  - race: Arabian

Résultat 2:
  - horse: Horse456
  - name: Lightning
  - race: Thoroughbred
```

### **Key Features:**
- ✅ Removes long URIs (keeps only the ID)
- ✅ Formats in readable French
- ✅ Groups related data
- ✅ Handles empty results gracefully

### **Used by:**
- `intelligent_chatbot.py` (to format context before sending to LLM)

---

## 📁 FILE 7: `intelligent_chatbot.py`

### **Purpose:**
**THE ORCHESTRATOR** - Coordinates all components to answer questions

### **Why it exists:**
This is the main entry point - it brings everything together:
1. Gets question from user
2. Generates SPARQL (via intelligent_sparql_generator)
3. Executes query (via graphdb_client)
4. Formats results (via context_builder)
5. Generates answer (via llm_client)

### **What it does:**

**Main Class: `IntelligentEquestrianChatbot`**
```python
class IntelligentEquestrianChatbot:
    def __init__(self):
        self.graphdb = GraphDBClient()
        self.llm = FrenchLLMClient()
        self.sparql_generator = IntelligentSPARQLGenerator(self.llm)
        self.context_builder = ContextBuilder()
    
    def answer_question(self, question):
        # Coordinates everything
```

### **How it works (STEP BY STEP):**

**STEP 1: Generate SPARQL**
```python
# Uses intelligent_sparql_generator.py
query_result = self.sparql_generator.generate_sparql(question)
sparql_query = query_result["sparql_query"]
entities_used = query_result["entities_used"]
relations_used = query_result["relations_used"]
```

**STEP 2: Execute Query**
```python
# Uses graphdb_client.py
results = self.graphdb.query(sparql_query)
bindings = results['results']['bindings']
```

**STEP 3: Format Results**
```python
# Uses context_builder.py
context = self.context_builder.format_results(bindings)
```

**STEP 4: Generate Answer**
```python
# Uses llm_client.py
system_prompt = "Tu es un expert en données équestres..."
user_prompt = f"Question: {question}\n\nContexte: {context}"
answer = self.llm.generate(user_prompt, system_prompt)
```

**STEP 5: Return Everything**
```python
return {
    "success": True,
    "question": question,
    "sparql_query": sparql_query,
    "entities_used": entities_used,
    "relations_used": relations_used,
    "results_count": len(bindings),
    "answer": answer
}
```

### **Display Options:**

**Verbose Mode (ON):**
```
================================================================================
❓ QUESTION: Quels chevaux participent à des entraînements?
================================================================================

🔧 ÉTAPE 1: Génération de la requête SPARQL...
✅ Requête générée!
📊 Entités utilisées: Horse, Training
🔗 Relations utilisées: hasParticipatedTo

📝 Requête SPARQL:
PREFIX horses: <...>
SELECT ?horse ?name ?training
WHERE {
    ?horse rdf:type horses:Horse .
    ...
}

🔍 ÉTAPE 2: Exécution sur GraphDB...
✅ 5 résultats trouvés!

🤖 ÉTAPE 4: Génération de la réponse...
✅ Réponse générée!

💬 RÉPONSE FINALE:
================================================================================
Cinq chevaux participent actuellement à des entraînements:
- Thunder participe à la séance de dressage
- Lightning participe à l'entraînement de saut
...
================================================================================
```

**Verbose Mode (OFF):**
```
Cinq chevaux participent actuellement à des entraînements:
- Thunder participe à la séance de dressage
- Lightning participe à l'entraînement de saut
...
```

### **Interactive Mode:**
```python
chatbot.chat()  # Starts interactive loop

🐴 Chatbot Équestre - Mode Interactif
Posez vos questions...

❓ Votre question: Quels chevaux participent à des entraînements?
[answer...]

❓ Votre question: Quel est le couplage cheval-cavalier?
[answer...]

❓ Votre question: quitter
👋 Au revoir!
```

---

## 🔄 COMPLETE DATA FLOW

### Example: "Quels chevaux participent à des entraînements?"

```
1. USER enters question
   ↓
2. CHATBOT receives question
   ↓
3. INTELLIGENT_SPARQL_GENERATOR:
   - Reads ontology structure
   - Uses Few-Shot examples
   - Calls LLM_CLIENT
   - LLM generates SPARQL
   - Returns: {sparql_query, entities, relations, explanation}
   ↓
4. GRAPHDB_CLIENT:
   - Receives SPARQL query
   - Sends to GraphDB endpoint
   - Returns raw results (JSON)
   ↓
5. CONTEXT_BUILDER:
   - Takes raw SPARQL results
   - Formats as readable text
   - Returns context string
   ↓
6. LLM_CLIENT (again):
   - Takes question + context
   - Generates natural French answer
   - Returns answer
   ↓
7. CHATBOT:
   - Displays everything
   - Shows SPARQL, entities, answer
   ↓
8. USER sees answer
```

---

## 🎯 KEY CONCEPTS

### 1. **Few-Shot Learning**
Instead of training a model, we teach by examples:
```
Example 1: "Quels chevaux?" → SELECT ?horse WHERE {...}
Example 2: "Qui a réalisé X?" → SELECT ?realisateur WHERE {...}
Example 3: ...

Now answer: "Quel cheval participe à X?"
LLM generates: SELECT ?horse ?training WHERE {...}
```

### 2. **Ontology-Aware Generation**
The LLM knows your ontology:
```
Classes: Horse, Rider, Training, Sensor
Properties: hasName, hasRace, hasParticipatedTo
Relations: AssociatedWith, isAttachedTo

Question: "Quels capteurs sont attachés aux chevaux?"
LLM knows: Use isAttachedTo relation, Horse and Sensor classes
```

### 3. **Named Graphs**
Your GraphDB has TWO graphs:
```
http://example.org/ontology → ontology.owl (schema)
http://example.org/instances → HorseKnowledgeGraphBis.rdf (data)

SPARQL must specify:
GRAPH <http://example.org/instances> { ?horse a horses:Horse }
```

### 4. **No Classifier Needed**
Traditional approach:
```
Classify question → Choose template → Fill template
```

Your approach:
```
Question → LLM generates custom SPARQL → Execute
```

---

## 🚀 IMPROVEMENT STRATEGY

### Phase 1: Add Few-Shot Examples (6 questions)
In `intelligent_sparql_generator.py`, add your 10 questions as examples:

```python
examples = """
Example 1:
Question: "Quel cheval a participé à quelle séance d'entraînement?"
SPARQL:
SELECT ?horse ?name ?training
WHERE {
    GRAPH <http://example.org/instances> {
        ?horse rdf:type horses:Horse .
        ?horse horses:hasParticipatedTo ?training .
        ?horse horses:hasName ?name .
    }
}

Example 2:
Question: "Quelles séances d'entraînement ont inclus des exercices de haute intensité?"
SPARQL:
SELECT ?training ?intensity
WHERE {
    GRAPH <http://example.org/instances> {
        ?training rdf:type horses:Training .
        ?training horses:Intensity ?intensity .
        FILTER(?intensity > 7)
    }
}

[... add all 10 questions ...]
"""
```

### Phase 2: Test with 4 remaining questions
Use questions NOT in examples to test generalization

### Phase 3: Iterate and improve
- Analyze failures
- Add constraints
- Improve ontology summary

---

**This is your complete GraphRAG system! Each file has a specific role, and they work together to create an intelligent chatbot that generates SPARQL dynamically.** 🐴🚀
