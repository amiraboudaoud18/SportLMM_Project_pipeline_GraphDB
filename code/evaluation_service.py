# evaluation_service.py
"""
Evaluation Service - Semantic similarity + LLM-as-judge for GraphRAG answers.
Uses OpenAI for judge LLM and embeddings (set OPENAI_API_KEY).
"""

import json
import os
from typing import Any

# Cost constants for reporting (optional; set via env or use 0)
COST_PER_1K_INPUT = float(os.getenv("COST_PER_1K_INPUT", "0.0"))
COST_PER_1K_OUTPUT = float(os.getenv("COST_PER_1K_OUTPUT", "0.0"))
COST_PER_1K_EMBEDDING = float(os.getenv("COST_PER_1K_EMBEDDING", "0.0"))


def init_evaluator():
    """
    Initialize the evaluator: judge LLM (gpt-4o-mini) and embeddings.
    Requires OPENAI_API_KEY in environment.
    Returns:
        (judge_llm, embeddings) for use with llm_judge_answer and calculate_semantic_similarity.
    """
    try:
        from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    except ImportError:
        raise ImportError(
            "evaluation_service requires langchain-openai and openai. "
            "Install with: pip install langchain-openai openai"
        )
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Set it in .env or: export OPENAI_API_KEY=sk-..."
        )
    judge_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key,
    )
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key,
    )
    return judge_llm, embeddings


def calculate_semantic_similarity(
    answer: str, ground_truth: str, embeddings: Any
) -> float:
    """
    Compute cosine similarity between embeddings of answer and ground_truth.
    Returns a value in [0, 1] (clamped).
    """
    if not answer.strip() or not ground_truth.strip():
        return 0.0
    try:
        vecs = embeddings.embed_documents([answer.strip(), ground_truth.strip()])
        a, b = vecs[0], vecs[1]
    except Exception:
        return 0.0
    try:
        import numpy as np
        a_arr = np.array(a, dtype=float)
        b_arr = np.array(b, dtype=float)
        dot = float(np.dot(a_arr, b_arr))
        na, nb = float(np.linalg.norm(a_arr)), float(np.linalg.norm(b_arr))
        if na == 0 or nb == 0:
            return 0.0
        sim = dot / (na * nb)
        return max(0.0, min(1.0, float(sim)))
    except Exception:
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(y * y for y in b) ** 0.5
        if na == 0 or nb == 0:
            return 0.0
        sim = dot / (na * nb)
        return max(0.0, min(1.0, sim))


def llm_judge_answer(
    question: str, answer: str, ground_truth: str, judge_llm: Any
) -> dict:
    """
    Use LLM-as-judge to score the answer on correctness, completeness, accuracy, overall (0-1) and reasoning.
    Returns dict with keys: correctness, completeness, accuracy, overall, reasoning.
    """
    prompt = f"""You are an impartial judge evaluating an AI answer against a reference (ground truth).

Question: {question}

Reference (ground truth): {ground_truth}

Model answer: {answer}

Score the model answer from 0.0 to 1.0 on:
- correctness: factual correctness compared to the reference
- completeness: whether all important information from the reference is present
- accuracy: precision and relevance of the answer
- overall: overall quality (average of the above or your judgment)

Respond with a single JSON object only, no other text, with keys: "correctness", "completeness", "accuracy", "overall", "reasoning".
Example: {{"correctness": 0.9, "completeness": 0.8, "accuracy": 0.85, "overall": 0.85, "reasoning": "Brief explanation."}}"""

    default_scores = {
        "correctness": 0.0,
        "completeness": 0.0,
        "accuracy": 0.0,
        "overall": 0.0,
        "reasoning": "Evaluation failed",
    }
    try:
        response = judge_llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        default_scores["reasoning"] = f"Judge LLM error: {e}"
        return default_scores

    text = text.strip()
    start = text.find("{")
    if start == -1:
        return default_scores
    depth = 0
    end = start
    for i, c in enumerate(text[start:], start):
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return default_scores

    for key in ["correctness", "completeness", "accuracy", "overall"]:
        if key in data and isinstance(data[key], (int, float)):
            default_scores[key] = float(max(0, min(1, data[key])))
    if "reasoning" in data and isinstance(data["reasoning"], str):
        default_scores["reasoning"] = data["reasoning"]
    if default_scores["overall"] == 0 and any(
        default_scores[k] > 0 for k in ["correctness", "completeness", "accuracy"]
    ):
        default_scores["overall"] = (
            default_scores["correctness"]
            + default_scores["completeness"]
            + default_scores["accuracy"]
        ) / 3
    return default_scores
