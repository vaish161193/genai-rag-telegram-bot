import json
import sqlite3

import numpy as np
from sentence_transformers import SentenceTransformer


DATABASE = "rag.db"
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks_from_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, source, text, embedding
        FROM chunks
        """
    )

    rows = cursor.fetchall()
    connection.close()

    chunks = []

    for row in rows:
        chunk_id, source, text, embedding_json = row

        chunks.append(
            {
                "id": chunk_id,
                "source": source,
                "text": text,
                "embedding": np.array(json.loads(embedding_json)),
            }
        )

    return chunks


def cosine_similarity(query_vector, chunk_vector):
    return np.dot(query_vector, chunk_vector) / (
        np.linalg.norm(query_vector) * np.linalg.norm(chunk_vector)
    )


def retrieve(query, chunks, model, top_k=3):
    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    results = []

    for chunk in chunks:
        score = cosine_similarity(
            query_embedding,
            chunk["embedding"],
        )

        results.append(
            {
                "source": chunk["source"],
                "text": chunk["text"],
                "score": float(score),
            }
        )

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results[:top_k]


def main():
    model = SentenceTransformer(MODEL_NAME)

    chunks = load_chunks_from_database()

    query = "How many vacation days do employees get?"

    print(f"Question: {query}\n")

    results = retrieve(query, chunks, model, top_k=3)

    for position, result in enumerate(results, start=1):
        print(f"--- Result {position} ---")
        print(f"Source: {result['source']}")
        print(f"Similarity: {result['score']:.4f}")
        print(result["text"])
        print()


if __name__ == "__main__":
    main()