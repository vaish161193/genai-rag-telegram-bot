from sentence_transformers import SentenceTransformer

from retrieval import load_chunks_from_database
from rag import answer_question


MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading knowledge base...")
    chunks = load_chunks_from_database()

    print(f"Loaded {len(chunks)} chunks.")
    print("\nGenAI Mini-RAG CLI Demo")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        answer, results = answer_question(
            question,
            model,
            chunks,
        )

        print("\nAnswer:")
        print(answer)

        if results and results[0]["score"] >= 0.30:
            print(f"\nSource: {results[0]['source']}")
            print(f"Similarity: {results[0]['score']:.4f}")

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()