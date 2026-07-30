from pathlib import Path


DATA_FOLDER = Path("data")


def chunk_markdown(text):
    lines = text.splitlines()

    chunks = []
    current_chunk = []

    for line in lines:
        if line.strip().startswith("## "):
            if current_chunk:
                chunks.append("\n".join(current_chunk).strip())

            current_chunk = [line]

        elif current_chunk:
            current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk).strip())

    return chunks


def main():
    all_chunks = []

    for file_path in sorted(DATA_FOLDER.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_markdown(text)

        print(f"\nFILE: {file_path.name}")
        print(f"Number of chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks, start=1):
            print(f"\n--- Chunk {index} ---")
            print(chunk)

            all_chunks.append(
                {
                    "source": file_path.name,
                    "text": chunk,
                }
            )

    print(f"\nTotal chunks: {len(all_chunks)}")


if __name__ == "__main__":
    main()