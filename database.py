import json
import sqlite3
from pathlib import Path

from sentence_transformers import SentenceTransformer

from ingest import chunk_markdown


DATABASE = "rag.db"
DATA_FOLDER = Path("data")
MODEL_NAME = "all-MiniLM-L6-v2"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            text TEXT NOT NULL,
            embedding TEXT
        )
        """
    )

    connection.commit()
    connection.close()


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


def insert_chunks():
    model = SentenceTransformer(MODEL_NAME)
    chunks = load_chunks()

    texts = [chunk["text"] for chunk in chunks]

    print("Creating embeddings...")
    embeddings = model.encode(texts)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM chunks")

    for chunk, embedding in zip(chunks, embeddings):
        embedding_json = json.dumps(embedding.tolist())

        cursor.execute(
            """
            INSERT INTO chunks (source, text, embedding)
            VALUES (?, ?, ?)
            """,
            (
                chunk["source"],
                chunk["text"],
                embedding_json,
            ),
        )

    connection.commit()
    connection.close()

    print(f"Inserted {len(chunks)} chunks with embeddings.")


def main():
    create_database()
    insert_chunks()


if __name__ == "__main__":
    main()