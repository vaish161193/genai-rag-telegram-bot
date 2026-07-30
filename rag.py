from sentence_transformers import SentenceTransformer

from retrieval import load_chunks_from_database, retrieve
from llm import ask_llm


MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.30


def answer_question(question, model, chunks):
    results = retrieve(
        question,
        chunks,
        model,
        top_k=3,
    )

    best_result = results[0]

    if best_result["score"] < SIMILARITY_THRESHOLD:
        return (
            "The information is not available in the knowledge base.",
            results,
        )

    context = (
        f"Source: {best_result['source']}\n"
        f"{best_result['text']}"
    )

    prompt = f"""
You are a company policy assistant.

The information below comes from the company's knowledge base.
Treat it as the authoritative source for answering the question.

Answer the user's question using ONLY the information in the knowledge base.
Do not use outside knowledge.
Do not invent details.

Knowledge Base:
{context}

User Question:
{question}

Answer:
"""

    answer = ask_llm(prompt)

    return answer, results


def main():
    model = SentenceTransformer(MODEL_NAME)
    chunks = load_chunks_from_database()

    test_questions = [
        "Can an employee work from home 2 days a week?",
        "Does the company provide dental insurance?",
        "How many annual leave days do employees get?",
        "Who is the Prime Minister of India?",
    ]

    for question in test_questions:
        answer, results = answer_question(
            question,
            model,
            chunks,
        )

        print("\nQuestion:")
        print(question)

        print("\nAnswer:")
        print(answer)

        print("\nBest Source:")
        print(
            f"{results[0]['source']} "
            f"(similarity: {results[0]['score']:.4f})"
        )

        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()