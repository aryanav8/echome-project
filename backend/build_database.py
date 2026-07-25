import chromadb
from sentence_transformers import SentenceTransformer

# Load the model that converts text into embeddings (numbers AI can search)
print("Loading embedding model... (this may take a minute the first time)")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Read our writings file
with open("data/my_writings.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Split into individual entries (each entry is separated by a blank line)
entries = [e.strip() for e in content.split("\n\n") if e.strip()]
print(f"Found {len(entries)} entries to process")

# Set up ChromaDB (our vector database) - stores data in a local folder
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create (or reset) our collection
try:
    chroma_client.delete_collection(name="my_writings")
except Exception:
    pass
collection = chroma_client.create_collection(name="my_writings")

# Convert each entry into an embedding and store it
print("Creating embeddings and saving to database...")
embeddings = model.encode(entries).tolist()

collection.add(
    documents=entries,
    embeddings=embeddings,
    ids=[f"entry_{i}" for i in range(len(entries))]
)

print(f"Done! {len(entries)} entries stored in the database.")