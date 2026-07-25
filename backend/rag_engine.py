import os
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv

# Load our secret API key from .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load embedding model and database (loaded once, reused for every question)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="my_writings")

def get_answer(question: str):
    # Step 1: Find the most relevant past writings
    query_embedding = embedding_model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    retrieved_entries = results["documents"][0]

    # Step 2: Build a prompt that grounds Gemini in those entries
    context = "\n".join(f"- {entry}" for entry in retrieved_entries)
    prompt = f"""You are answering as this person, based ONLY on their real past writing below.
Match their tone and personality. Keep the answer natural and conversational, 2-4 sentences.
If the past writing doesn't really cover the question, say so honestly instead of making things up.

Past writing:
{context}

Question: {question}

Answer as this person:"""

    # Step 3: Generate the answer
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "sources": retrieved_entries
    }

# Quick test when running this file directly
if __name__ == "__main__":
    result = get_answer("How do you feel about mornings?")
    print("\nAnswer:", result["answer"])
    print("\nSources used:")
    for s in result["sources"]:
        print("-", s)