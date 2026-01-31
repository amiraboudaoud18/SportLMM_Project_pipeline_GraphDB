# Experiments Branch — Initial Configurations

This branch keeps **initial configurations** of the Graph RAG architecture (GraphDB + local LLM + RDF) that were tried before the production version.

**Production code lives on the `main` branch** — that is the stable, working pipeline (exp_006_amira promoted to root).

---

## Contents

| Experiment | Description |
|------------|-------------|
| **exp_001_jiwoo** | Early RDF/LLM pipeline (Horse KG, notebooks). |
| **exp_002_amira** | Graph RAG system (config.yaml, graph_rag_system). |
| **exp_003_amira** | Cinema ontology/chatbot (OWL, SPARQL, GraphDB). |
| **exp_004_amira** | Equestrian chatbot package (config, context, GraphDB, intelligent chatbot). |
| **exp_005_amira** | Refined pipeline (French Q&A, Horse_generatedData). |
| **exp_006_amira** | **Production version** — dual LLM, evaluation (RAGAS, semantic, compare). Now on `main`. |

---

## Summary

- **exp_001–003:** Early trials (different ontologies, notebooks, cinema vs equestrian).
- **exp_004–005:** Equestrian pipeline with config, GraphDB client, SPARQL generator, context builder, LLM client.
- **exp_006:** Final architecture: specialized SPARQL + answer LLMs, evaluation scripts, semantic + RAGAS + comparison. This codebase was reorganized onto `main` with docs and a single `requirements.txt`.

Each experiment folder may have its own `requirements.txt` or `config.yaml`; for a single consolidated setup, use the **main** branch.
