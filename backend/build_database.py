import os
import time
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Read our writings file
with open("data/my_writings.txt", "r", encoding="utf-8") as f:
    content = f.read()

entries = [e.strip() for e in content.split("\n\n") if e.strip()]
print(f"Found {len(entries)} entries to process")

chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    chroma_client.delete_collection(name="my_writings")
except Exception:
    pass
collection = chroma_client.create_collection(name="my_writings")

# Process in small batches to avoid rate limits
print("Creating embeddings via Gemini API (in batches)...")
all_embeddings = []
batch_size = 10

for i in range(0, len(entries), batch_size):
    batch = entries[i:i + batch_size]
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=batch
    )
    all_embeddings.extend([e.values for e in result.embeddings])
    print(f"Processed {min(i + batch_size, len(entries))}/{len(entries)}")
    time.sleep(2)  # small pause to stay under rate limits

collection.add(
    documents=entries,
    embeddings=all_embeddings,
    ids=[f"entry_{i}" for i in range(len(entries))]
)

print(f"Done! {len(entries)} entries stored in the database.")