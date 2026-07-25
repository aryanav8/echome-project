import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="my_writings")

# Try a test question
query = "How do you feel about mornings?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3
)

print(f"\nQuery: {query}\n")
print("Top matching entries from your writing:")
for i, doc in enumerate(results["documents"][0]):
    print(f"\n{i+1}. {doc}")