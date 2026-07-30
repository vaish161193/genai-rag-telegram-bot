from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


model = SentenceTransformer(MODEL_NAME)


text = "Employees receive 24 days of annual leave per calendar year."

embedding = model.encode(text)


print("Original text:")
print(text)

print("\nEmbedding:")
print(embedding)

print("\nEmbedding length:")
print(len(embedding))