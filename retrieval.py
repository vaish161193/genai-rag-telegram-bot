from pathlib import Path

from sentence_transformers import SentenceTransformer, util

from ingest import chunk_markdown


DATA_FOLDER = Path("data")
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks():
    all_chunks = []

    for file_path in sorted(DATA_FOLDER.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_markdown(text)

        for chunk in chunks:
            all_chunks.append(
                {
                    "source": file_path.name,
                    "text": chunk,
                }
            )

    return all_chunks


def retrieve(query, chunks, model, top_k=3):
    texts = [chunk["text"] for chunk in chunks]

    chunk_embeddings = model.encode(
        texts,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    scores = util.cos_sim(query_embedding, chunk_embeddings)[0]

    top_results = scores.argsort(descending=True)[:top_k]

    results = []

    for index in top_results:
        index = int(index)

        results.append(
            {
                "source": chunks[index]["source"],
                "text": chunks[index]["text"],
                "score": float(scores[index]),
            }
        )

    return results


def main():
    model = SentenceTransformer(MODEL_NAME)

    chunks = load_chunks()

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