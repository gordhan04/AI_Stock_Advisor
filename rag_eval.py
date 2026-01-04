"""
RAG Evaluation Script
Tests whether correct Minervini concepts are retrieved
"""

from rag_engine import get_vector_db, get_rag_context

# ---------------- TEST CASES ----------------

EVAL_QUESTIONS = [
    {
        "question": "What defines Stage 2 in Minervini methodology?",
        "expected_keywords": ["stage 2", "150", "moving average", "uptrend"]
    },
    {
        "question": "How much loss does Minervini allow on a trade?",
        "expected_keywords": ["loss", "stop", "7", "8"]
    },
    {
        "question": "What volume behavior confirms a breakout?",
        "expected_keywords": ["volume", "accumulation", "increase"]
    },
    {
        "question": "What happens in Stage 4 decline?",
        "expected_keywords": ["stage 4", "decline", "below", "moving average"]
    },
]

# ---------------- EVALUATION ----------------

def evaluate_rag():
    vectordb = get_vector_db()

    total = len(EVAL_QUESTIONS)
    passed = 0

    print("\n📘 RAG EVALUATION RESULTS\n" + "-" * 40)

    for idx, test in enumerate(EVAL_QUESTIONS, start=1):
        context = get_rag_context(test["question"], vectordb)
        context_lower = context.lower()

        hits = [
            keywrd for keywrd in test["expected_keywords"]
            if keywrd in context_lower
        ]

        score = len(hits) / len(test["expected_keywords"])

        print(f"\nTest {idx}")
        print(f"Q: {test['question']}")
        print(f"Score: {score:.2f}")
        print(f"Matched keywords: {hits}")

        if score >= 0.4:
            print("✅ PASS")
            passed += 1
        else:
            print("❌ FAIL")

    print("\n" + "-" * 40)
    print(f"Final Score: {passed}/{total} tests passed")

    return passed, total


if __name__ == "__main__":
    evaluate_rag()
