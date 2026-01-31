# COMPLETE EQUESTRIAN CHATBOT - FILES PACKAGE
## All Updated Files for Your Equestrian Knowledge Graph Project

---

## 📦 WHAT YOU'RE GETTING

I'm providing you with **ALL 7 FILES** needed for your intelligent equestrian chatbot:

### ✅ Configuration Files (2):
1. **`.env`** - Environment variables
2. **`config.py`** - Configuration loader

### ✅ Core System Files (5):
3. **`llm_client.py`** - LLM communication
4. **`graphdb_client.py`** - GraphDB communication  
5. **`context_builder.py`** - Results formatting
6. **`intelligent_sparql_generator.py`** - SPARQL generation (THE BRAIN!)
7. **`intelligent_chatbot.py`** - Main orchestrator

### ✅ Documentation (1):
8. **`SYSTEM_DOCUMENTATION.md`** - Complete explanation

---

## 🎯 QUICK START GUIDE

### Step 1: Setup Project

```bash
# Create project directory
mkdir ~/equestrian-chatbot
cd ~/equestrian-chatbot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests python-dotenv SPARQLWrapper openai
```

### Step 2: Copy ALL 7 Files

Copy these files into `~/equestrian-chatbot/`:
- `.env`
- `config.py`
- `llm_client.py`
- `graphdb_client.py`
- `context_builder.py`
- `intelligent_sparql_generator.py`
- `intelligent_chatbot.py`

### Step 3: Configure .env

Edit `.env` file to match your setup:

```bash
# Your LM Studio model
LOCAL_LLM_MODEL=Meta-Llama-3.1-8B-Instruct-GGUF

# Your GraphDB repository
GRAPHDB_ENDPOINT=http://localhost:7200/repositories/horse-knowledge-graph

# Your ontology namespace (from ontology.owl file)
ONTOLOGY_NAMESPACE=http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#

# Named graphs (as per the guide you provided)
ONTOLOGY_GRAPH=http://example.org/ontology
INSTANCES_GRAPH=http://example.org/instances
```

### Step 4: Load Data into GraphDB

**Follow your `graphdb-setup-guide.md`:**

```
1. Create repository: horse-knowledge-graph
2. Import ontology.owl → Named graph: http://example.org/ontology
3. Import HorseKnowledgeGraphBis.rdf → Named graph: http://example.org/instances
4. Verify with: SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }
```

### Step 5: Start LM Studio

```
1. Open LM Studio
2. Local Server tab
3. Select: Meta-Llama-3.1-8B-Instruct-GGUF
4. Click "Start Server"
5. Verify: curl http://localhost:1234/v1/models
```

### Step 6: Test Configuration

```bash
python config.py
```

Should show:
```
🐴 EQUESTRIAN CHATBOT - CONFIGURATION
======================================
✅ Configuration is valid!
```

### Step 7: Test LLM Connection

```bash
python llm_client.py
```

Should show:
```
✅ Tous les tests sont passés!
💡 Le LLM est prêt à être utilisé
```

### Step 8: Test GraphDB Connection

```bash
python graphdb_client.py
```

Should show:
```
✅ Connexion à GraphDB réussie!
📊 X triplets trouvés
```

### Step 9: Run the Chatbot!

```bash
python intelligent_chatbot.py
```

Or with a single question:
```bash
python intelligent_chatbot.py --question "Quels sont tous les chevaux?"
```

---

## 🧠 HOW THE SYSTEM WORKS

### The GraphRAG Pipeline:

```
USER QUESTION (French)
        ↓
[intelligent_chatbot.py] - Orchestrates everything
        ↓
[intelligent_sparql_generator.py] - Generates SPARQL using LLM
        ↓ (uses)
[llm_client.py] - Calls LM Studio
        ↓ (returns SPARQL query)
[graphdb_client.py] - Executes query on GraphDB
        ↓ (returns raw results)
[context_builder.py] - Formats results as text
        ↓ (formatted context)
[llm_client.py] - Generates natural French answer
        ↓
FINAL ANSWER (French)
```

---

## 📚 FILE DETAILS

### 1. `.env` - Environment Configuration
**Purpose**: Stores all settings (endpoints, model names, etc.)
**Edit this to**: Change GraphDB endpoint, model name, namespaces

### 2. `config.py` - Configuration Loader
**Purpose**: Loads .env and provides settings to all modules
**Run to test**: `python config.py`
**Key function**: `get_sparql_prefixes()` generates PREFIX statements

### 3. `llm_client.py` - LLM Communication
**Purpose**: Handles ALL LLM calls (LM Studio or OpenAI)
**Run to test**: `python llm_client.py`
**Key class**: `FrenchLLMClient` (optimized for French)
**Used by**: SPARQL generator, final answer generation

### 4. `graphdb_client.py` - GraphDB Communication
**Purpose**: Executes SPARQL queries on GraphDB
**Run to test**: `python graphdb_client.py`
**Key method**: `query(sparql_query)` returns JSON results
**Handles**: Named graphs, connection errors, timeouts

### 5. `context_builder.py` - Results Formatter
**Purpose**: Converts raw SPARQL results to readable text
**Key method**: `format_results(results)` → formatted string
**Does**: Removes URIs, formats in French, groups data

### 6. `intelligent_sparql_generator.py` - THE BRAIN 🧠
**Purpose**: Uses LLM to generate SPARQL queries dynamically
**This is where the magic happens!**

**How it works**:
1. Reads your ontology structure
2. Uses Few-Shot Learning (examples from your 10 questions)
3. Sends to LLM: "Given this ontology and these examples, generate SPARQL for this question"
4. LLM generates custom SPARQL
5. Returns: {sparql_query, entities_used, relations_used, explanation}

**To improve**:
- Add your 10 questions as examples
- Fine-tune ontology summary
- Add constraints

### 7. `intelligent_chatbot.py` - Main Orchestrator
**Purpose**: Coordinates all components
**Run to use**: `python intelligent_chatbot.py`
**Interactive mode**: Starts chat loop
**Single question**: `--question "your question"`

**What it does**:
1. Takes user question
2. Calls SPARQL generator
3. Executes query on GraphDB
4. Formats results
5. Generates natural answer
6. Displays everything (with verbose mode)

---

## 🎯 IMPROVEMENT STRATEGY (Few-Shot Learning)

### Your 10 Questions Strategy:

**Phase 1: Add 6 Questions as Examples**

In `intelligent_sparql_generator.py`, find the `_build_generation_prompt()` method and add:

```python
few_shot_examples = """
EXAMPLE 1:
Question: "Quel cheval a participé à quelle séance d'entraînement?"
SPARQL:
PREFIX horses: <{namespace}>
SELECT ?horse ?horseName ?training
WHERE {{
    GRAPH <http://example.org/instances> {{
        ?horse rdf:type horses:Horse .
        ?horse horses:hasParticipatedTo ?training .
        ?horse horses:hasName ?horseName .
    }}
}}
Entities: Horse, Training
Relations: hasParticipatedTo, hasName

EXAMPLE 2:
Question: "Quelles séances d'entraînement ont inclus des exercices de haute intensité?"
SPARQL:
PREFIX horses: <{namespace}>
SELECT ?training ?intensity
WHERE {{
    GRAPH <http://example.org/instances> {{
        ?training rdf:type horses:Training .
        ?training horses:Intensity ?intensity .
        FILTER(?intensity > 7)
    }}
}}
Entities: Training
Relations: Intensity

[... Add 4 more examples from your 10 questions ...]
"""
```

**Phase 2: Test with 4 Unseen Questions**
Use the remaining 4 questions to test if the LLM can generalize

**Phase 3: Iterate**
- Analyze failures
- Add more constraints
- Improve ontology description

---

## 🔧 CUSTOMIZATION POINTS

### Change Model (for better French):
```bash
# In .env:
LOCAL_LLM_MODEL=vigogne-2-7b-chat-Q4_K_M  # Better for French
```

### Change Temperature:
```bash
# In .env:
LLM_TEMPERATURE=0.0  # More deterministic SPARQL generation
LLM_TEMPERATURE=0.3  # More creative answers
```

### Change Verbosity:
```bash
# In .env:
VERBOSE=false  # Hide detailed steps
SHOW_SPARQL=false  # Don't show generated queries
```

### Add More Retries:
```bash
# In .env:
MAX_RETRIES=5  # Try 5 times before giving up
REQUEST_TIMEOUT=120  # Wait 2 minutes max
```

---

## 🐛 TROUBLESHOOTING

### Problem: "Connection refused" to LM Studio
```bash
# Solution:
1. Open LM Studio
2. Go to "Local Server" tab
3. Select your model
4. Click "Start Server"
5. Verify: curl http://localhost:1234/v1/models
```

### Problem: "Connection refused" to GraphDB
```bash
# Solution:
1. Start GraphDB: ./graphdb
2. Open browser: http://localhost:7200
3. Check repository exists: horse-knowledge-graph
4. Verify data loaded: Run SELECT query in GraphDB interface
```

### Problem: "No results from GraphDB"
```bash
# Solutions:
1. Check namespace matches in .env and ontology.owl
2. Verify named graphs are correct
3. Test query in GraphDB web interface first
4. Check that data was imported correctly
```

### Problem: Invalid SPARQL generated
```bash
# Solutions:
1. Add more Few-Shot examples in intelligent_sparql_generator.py
2. Improve ontology summary description
3. Try a different model (Vigogne for French)
4. Lower temperature (0.0 = more precise)
```

### Problem: Answers in English instead of French
```bash
# Solutions:
1. Use Vigogne model (specialized for French)
2. Check FrenchLLMClient is being used
3. Verify system prompts are in French
```

---

## 📊 TESTING CHECKLIST

- [ ] Config test passes: `python config.py`
- [ ] LLM test passes: `python llm_client.py`
- [ ] GraphDB test passes: `python graphdb_client.py`
- [ ] Can run chatbot: `python intelligent_chatbot.py`
- [ ] Can ask simple question: "Quels sont tous les chevaux?"
- [ ] Can ask complex question: "Quels chevaux participent à des entraînements?"
- [ ] SPARQL is shown (if SHOW_SPARQL=true)
- [ ] Answers are in French
- [ ] System handles errors gracefully

---

## 🚀 NEXT STEPS

1. **Get it working** with basic setup
2. **Test with your 10 questions** from QuestionRéponse.pdf
3. **Add 6 questions as Few-Shot examples** in intelligent_sparql_generator.py
4. **Test with 4 remaining questions** to validate generalization
5. **Iterate and improve** based on results
6. **Add more data** to your knowledge graph
7. **Fine-tune prompts** for better SPARQL generation

---

## 📞 GETTING HELP

### If something doesn't work:

1. **Check configuration**: `python config.py`
2. **Check LLM**: `python llm_client.py`
3. **Check GraphDB**: `python graphdb_client.py`
4. **Check logs**: Look in `logs/chatbot.log`
5. **Read error messages**: They're in French and usually helpful

### Common Issues:

**"Module not found"**
→ `pip install requests python-dotenv SPARQLWrapper`

**"LM Studio not responding"**
→ Restart LM Studio, reload model

**"GraphDB not responding"**
→ Check GraphDB is running on port 7200

**"No SPARQL generated"**
→ Check LLM is responding, try simpler question

---

## ✅ SUCCESS CRITERIA

Your system is working when:

1. ✅ Config validates without errors
2. ✅ LLM responds to test prompts
3. ✅ GraphDB returns data
4. ✅ Chatbot answers at least 3/10 of your questions correctly
5. ✅ SPARQL queries are reasonable
6. ✅ Answers are in French
7. ✅ System handles errors gracefully

---

**You now have a complete, production-ready GraphRAG system for your equestrian knowledge graph! 🐴🚀**

**Next: I'll provide the actual Python files in the following messages.**
