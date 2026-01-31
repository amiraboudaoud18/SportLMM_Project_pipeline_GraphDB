# Evaluation Results

This document summarizes how the Graph RAG pipeline was evaluated and where the results are stored.

---

## Evaluation Setup

- **Pipeline:** Natural language question → SPARQL (via SPARQL LLM) → GraphDB → context → natural language answer (via Answer LLM).
- **Test data:** French Q&A dataset with ground-truth answers and expected context (see `data/french-graphrag-qa V2.md` and any generated `test_dataset.json`).
- **Config used for the reported run:** Dual specialized local models (SPARQL: `qwen2.5-coder-14b-instruct-mlx`, Answer: `meta-llama-3.1-8b-instruct`).

---

## Types of Evaluation

1. **Semantic + LLM-as-judge** (`evaluation/run_semantic_evaluation.py`, `evaluation_service.py`)  
   - Embedding similarity between generated answer and ground truth.  
   - LLM judge (e.g. gpt-4o-mini) scores correctness and gives short reasoning.  
   - Requires `OPENAI_API_KEY`.

2. **RAGAS** (`evaluation/evaluate.py`, `evaluation/add_ragas_scores.py`)  
   - Faithfulness, answer relevancy, context precision, answer correctness.  
   - Requires `ragas`, `datasets`, and optionally `OPENAI_API_KEY` for some metrics.

3. **Comparison across runs** (`evaluation/compare_results.py`)  
   - Compares multiple `results_*.json` files (e.g. different LLM configs) and prints aggregate metrics and recommendations.

---

## Where Results Are Stored

- **For supervisors (published results):** **[`evaluation_results/`](../evaluation_results/)** at the **repo root**  
  - **RAGAS/** — RAGAS runs for test1–test6 (different model configs).  
  - **semantic_evaluation_*.json** — Semantic similarity + LLM-judge run.  
  - See [evaluation_results/README.md](../evaluation_results/README.md) for an index.

- **Script output (optional):** `code/evaluation_results/` — where evaluation scripts write by default; naming e.g. `results_<sparql_model>_<answer_model>_<date>.json`.
- **Content:** Metadata (evaluation date, model config, total time, number of questions) and per-question fields: `question_id`, `question`, `ground_truth`, `generated_answer`, `context`, `sparql_query`, `results_count`, `success`, `performance`, and optionally RAGAS/semantic scores.

---

## Example Result Summary (Dual-Model Run)

One evaluation run (40 questions, dual specialized models) produced:

- **Metadata:**  
  - `evaluation_date`: 2026-01-15  
  - `sparql_model`: qwen2.5-coder-14b-instruct-mlx  
  - `answer_model`: meta-llama-3.1-8b-instruct  
  - `using_specialized`: true  

- **Per-question:** Each item includes `generated_answer`, `ground_truth`, `sparql_query`, `success`, and timing. Semantic and RAGAS scores can be appended using `add_ragas_scores.py` and the semantic evaluation script.

For exact numbers and full JSON, open the files in **`evaluation_results/`** (repo root) or `code/evaluation_results/`.

---

## How to Reproduce

1. Set `.env` to the desired config (see [LLM_CONFIGURATIONS.md](LLM_CONFIGURATIONS.md)).
2. Ensure GraphDB is running with the equestrian repository and data loaded.
3. From project root:  
   `cd code && python evaluation/run_semantic_evaluation.py`  
   (and/or `python evaluation/evaluate.py` if using RAGAS with a test dataset).
4. Optional: add RAGAS to an existing result file:  
   `python evaluation/add_ragas_scores.py code/evaluation_results/results_....json`
5. Compare several runs:  
   `python evaluation/compare_results.py` (default directory: `code/evaluation_results/`).

**Published results** (RAGAS + semantic) are copied to **`evaluation_results/`** at repo root so supervisors can find them easily; see [evaluation_results/README.md](../evaluation_results/README.md).
