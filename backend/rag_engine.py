import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="my_writings")

def get_answer(question: str):
    # Step 1: Embed the question via Gemini API
    query_result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )
    query_embedding = [query_result.embeddings[0].values]

    # Step 2: Find the most relevant past writings
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    retrieved_entries = results["documents"][0]

    # Step 3: Build a prompt that grounds Gemini in those entries
    context = "\n".join(f"- {entry}" for entry in retrieved_entries)
    prompt = f"""You are answering as this person, based ONLY on their real past writing below.
Match their tone and personality. Keep the answer natural and conversational, 2-4 sentences.
If the past writing doesn't really cover the question, say so honestly instead of making things up.

Past writing:
{context}

Question: {question}

Answer as this person:"""

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

    return {
        "answer": response.text,
        "sources": retrieved_entries
    }

if __name__ == "__main__":
    result = get_answer("How do you feel about mornings?")
    print("\nAnswer:", result["answer"])
    print("\nSources used:")
    for s in result["sources"]:
        print("-", s)