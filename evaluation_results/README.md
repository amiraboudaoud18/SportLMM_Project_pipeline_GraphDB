# Evaluation Results (for supervisors)

This folder contains the **evaluation results** for the Graph RAG pipeline (GraphDB + local LLM + RDF).

---

## Contents

| Folder / file | Description |
|---------------|-------------|
| **RAGAS/** | RAGAS metrics (faithfulness, answer relevancy, context precision, answer correctness) for different model configurations (test1–test6). |
| **semantic_evaluation_20260129_215817_pipeline_graphdb.json** | Semantic similarity + LLM-as-judge evaluation (40 questions, overall metrics and per-question scores). |

---

## RAGAS runs (model configurations)

| File | Configuration |
|------|----------------|
| `eval_results_test1_qwen_llama.json` | test1 — Qwen + Llama (baseline) |
| `eval_results_test2_qwen_mistral.json` | test2 — Qwen + Mistral |
| `eval_results_test3_qwen_vigogne.json` | test3 — Qwen + Vigogne |
| `eval_results_test4_deepseek_mistral.json` | test4 — DeepSeek + Mistral |
| `eval_results_test5_codellama_mistral.json` | test5 — CodeLlama + Mistral |
| `eval_results_test6_GPT-OSS-20B_unified.json` | test6 — GPT-OSS-20B (unified) |

Each JSON includes metadata (model config, date), success rate, timing, and RAGAS scores.

---

## Semantic + LLM-judge run

- **File:** `semantic_evaluation_20260129_215817_pipeline_graphdb.json`
- **Metrics:** success rate, average semantic similarity, LLM-judge scores (correctness, completeness, accuracy), combined score, and per-category stats.

---

For how to reproduce or interpret these results, see [docs/EVALUATION_RESULTS.md](../docs/EVALUATION_RESULTS.md) in the repo.
