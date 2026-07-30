from sentence_transformers import SentenceTransformer

from retrieval import load_chunks_from_database, retrieve
from llm import ask_llm


MODEL_NAME = "all-MiniLM-L6-v2"


def answer_question(question, model, chunks):
    results = retrieve(
        question,
        chunks,
        model,
        top_k=3,
    )

    context_parts = []

    for result in results:
        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a company policy assistant.

Answer the user's question using ONLY the information in the
provided knowledge base context.

Do not use outside knowledge.
Do not make assumptions.

If the answer is not available in the context, say:
"The information is not available in the knowledge base."

Knowledge Base Context:
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

    question = "Can an employee work from home 2 days a week?"

    answer, results = answer_question(
        question,
        model,
        chunks,
    )

    print("Question:")
    print(question)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")

    for result in results:
        print(
            f"- {result['source']} "
            f"(similarity: {result['score']:.4f})"
        )


if __name__ == "__main__":
    main()