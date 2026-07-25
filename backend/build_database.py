import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Read our writings file
with open("data/my_writings.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Split into individual entries (each entry is separated by a blank line)
entries = [e.strip() for e in content.split("\n\n") if e.strip()]
print(f"Found {len(entries)} entries to process")

# Set up ChromaDB (our vector database)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    chroma_client.delete_collection(name="my_writings")
except Exception:
    pass
collection = chroma_client.create_collection(name="my_writings")

# Get embeddings from Gemini's API instead of a local model
print("Creating embeddings via Gemini API...")
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=entries
)
embeddings = [e.values for e in result.embeddings]

collection.add(
    documents=entries,
    embeddings=embeddings,
    ids=[f"entry_{i}" for i in range(len(entries))]
)

print(f"Done! {len(entries)} entries stored in the database.")