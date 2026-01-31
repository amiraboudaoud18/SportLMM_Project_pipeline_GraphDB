# Implementation Guide — File-by-File

This document describes what each file in the project does and how they fit together.

## Architecture Overview

The system is a **Graph RAG (Retrieval-Augmented Generation)** pipeline:

1. **User question** → LLM generates **SPARQL** from ontology context  
2. **SPARQL** → executed on **GraphDB**  
3. **Query results** → formatted as context → **LLM** generates natural-language answer  

All configuration is centralized in `config.py` and can be switched (local LLM vs OpenAI, single vs dual model) via environment variables.

---

## Core Modules (in `code/`)

### `config.py`
- **Role:** Single source of configuration (LLM, GraphDB, ontology, app settings).
- **Behavior:** Loads from `.env` via `python-dotenv`, exposes constants and helpers.
- **Key exports:** `GRAPHDB_ENDPOINT`, `LOCAL_LLM_*`, `SPARQL_LLM_MODEL`, `ANSWER_LLM_MODEL`, `get_sparql_prefixes()`, `get_active_models()`, `validate_config()`, `print_config()`.
- **See:** [LLM_CONFIGURATIONS.md](LLM_CONFIGURATIONS.md) for the three configurations (single model, dual specialized, OpenAI).

### `graphdb_client.py`
- **Role:** Execute SPARQL queries against GraphDB.
- **Behavior:** POSTs queries to the repository endpoint, returns JSON results. Handles connection/timeout errors and returns empty bindings on failure.
- **Main API:** `GraphDBClient(endpoint).query(sparql_query)` → `{"results": {"bindings": [...]}}`, `test_connection()`.

### `llm_client.py`
- **Role:** Talk to LLMs (local OpenAI-compatible API or OpenAI).
- **Behavior:**  
  - `LLMClient`: base client (endpoint, model, temperature, max_tokens).  
  - `SPARQLLLMClient`: uses `SPARQL_LLM_MODEL` or `LOCAL_LLM_MODEL`, temperature 0, for SPARQL generation.  
  - `AnswerLLMClient`: uses `ANSWER_LLM_MODEL` or `LOCAL_LLM_MODEL`, temperature 0.3, for French answers.  
- **Helpers:** `get_sparql_llm()`, `get_answer_llm()` used by the chatbot.

### `intelligent_sparql_generator.py`
- **Role:** Generate SPARQL from natural-language questions using the ontology.
- **Behavior:** Builds an ontology summary (classes, properties, relationship directions, sensor types) and sends it + the question to the SPARQL LLM. Parses JSON `{"sparql_query": "..."}` from the response.
- **Main API:** `IntelligentSPARQLGenerator(llm).generate_sparql(question)` → SPARQL string.

### `context_builder.py`
- **Role:** Turn SPARQL result bindings into text for the answer LLM.
- **Behavior:** Formats bindings (and optional explanation) into a readable “Données trouvées” block; shortens URIs for display.
- **Main API:** `ContextBuilder().format_results(bindings, explanation)`, `format_for_display(bindings)`.

### `intelligent_chatbot.py`
- **Role:** Main orchestrator — end-to-end Graph RAG.
- **Behavior:**  
  1. Initialize GraphDB client, SPARQL generator (with SPARQL LLM), context builder, answer LLM.  
  2. `answer_question(question)`: generate SPARQL → run on GraphDB → build context → generate answer with answer LLM.  
- **Entry point:** `run_chatbot()` for interactive loop; can be imported and used programmatically.

---

## Evaluation (in `code/evaluation/` and `code/evaluation_service.py`)

### `evaluation_service.py`
- **Role:** Semantic similarity + LLM-as-judge for answer quality.
- **Behavior:**  
  - `init_evaluator()`: creates judge LLM (e.g. gpt-4o-mini) and embeddings (OpenAI).  
  - `calculate_semantic_similarity(answer, ground_truth, embeddings)`: cosine similarity in [0, 1].  
  - `llm_judge_answer(question, answer, ground_truth, judge_llm)`: score + reasoning.  
- **Requires:** `OPENAI_API_KEY`, `langchain-openai`, `openai`.

### `evaluation/evaluate.py`
- **Role:** RAGAS-based evaluation (faithfulness, answer_relevancy, context_precision, answer_correctness) + performance.
- **Behavior:** Loads a test dataset (e.g. `test_dataset.json`), runs the chatbot on each question, computes RAGAS metrics and timing, saves JSON results.
- **Requires:** `ragas`, `datasets`, test dataset with `question`, `ground_truth`, etc.

### `evaluation/run_semantic_evaluation.py`
- **Role:** Run semantic + LLM-judge evaluation on a dataset.
- **Behavior:** Uses `evaluation_service` (similarity + judge), runs on each item, writes results to `evaluation_results/` with metadata (model config, date).

### `evaluation/add_ragas_scores.py`
- **Role:** Add RAGAS scores to an existing evaluation results JSON.
- **Behavior:** Reads a results file, runs RAGAS on the stored (question, answer, context, ground_truth), appends scores and saves.

### `evaluation/compare_results.py`
- **Role:** Compare multiple `results_*.json` runs (e.g. different LLM configs).
- **Behavior:** Loads all result files from a directory, aggregates metrics, prints comparison tables and recommendations.

### `evaluation/generate_manual_evaluation.py`
- **Role:** Generate a manual evaluation sheet (e.g. CSV/JSON) from a test dataset for human scoring.

### `evaluation/questions_réponses.md`
- **Role:** Human-readable Q&A / ground-truth reference for the equestrian KG (French).

---

## Data (in `data/`)

- **`ontology.owl`** — Equestrian ontology (classes, properties) used by GraphDB and by the SPARQL generator’s ontology summary.
- **`Horse_generatedDataV2.rdf`** — RDF instance data (horses, sensors, events, training, etc.) loaded into GraphDB.
- **`french-graphrag-qa V2.md`** — Structured Q&A dataset (questions, ground truth, SPARQL, context) for evaluation and documentation.

---

## Run Modes

- **Chatbot (interactive):** From project root, `cd code && python intelligent_chatbot.py`.
- **Config check:** `cd code && python config.py`.
- **Evaluation (semantic + judge):** `cd code && python evaluation/run_semantic_evaluation.py` (dataset path configurable inside script).
- **Evaluation (RAGAS):** `cd code && python evaluation/evaluate.py` (expects `test_dataset.json` or path in script).
- **Add RAGAS to existing results:** `cd code && python evaluation/add_ragas_scores.py <path_to_results.json>`.
- **Compare runs:** `cd code && python evaluation/compare_results.py` (uses `evaluation_results/` by default).

All paths (GraphDB, LLM endpoint, model names, ontology namespace) are set in `config.py` and `.env`; see [LLM_CONFIGURATIONS.md](LLM_CONFIGURATIONS.md) for the three configurations used during development.
