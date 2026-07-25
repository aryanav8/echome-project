# EchoMe

**Live demo:** https://echome-project.vercel.app/

EchoMe is a Retrieval-Augmented Generation (RAG) web app that answers questions using a curated dataset of my own real thoughts, opinions, and writing style — instead of generic AI responses. Ask it something, and it retrieves the most relevant pieces of my past writing, then generates an answer grounded in that context.

## How it works

1. **Data** — A collection of my own short personal writings (opinions, reflections, everyday thoughts) stored as plain text entries.
2. **Embedding** — Each entry is converted into a vector embedding using Google's Gemini Embedding API (`gemini-embedding-001`).
3. **Storage** — Embeddings are stored in a local ChromaDB vector database.
4. **Retrieval** — When a question comes in, it's embedded the same way, and ChromaDB returns the most semantically similar entries (not just keyword matches).
5. **Generation** — The retrieved entries are passed as context to Gemini (`gemini-3.5-flash`), which generates a natural-sounding answer grounded only in that retrieved context — and is instructed to say so honestly if the data doesn't cover the question, rather than making something up.

## Tech stack

**Backend**
- FastAPI (Python) — REST API
- ChromaDB — vector database
- Google Gemini API — embeddings + generation
- Deployed on Render

**Frontend**
- React (Vite)
- Deployed on Vercel

## Architecture

```
User question
     |
     v
React frontend  --POST /ask-->  FastAPI backend
                                       |
                                       v
                          Embed question (Gemini API)
                                       |
                                       v
                       Query ChromaDB for top matches
                                       |
                                       v
                  Build prompt with retrieved context
                                       |
                                       v
                    Generate answer (Gemini API)
                                       |
                                       v
                  Return {answer, sources} to frontend
```

## Running locally

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# Add a .env file with: GEMINI_API_KEY=your_key_here
python build_database.py     # builds the vector database
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

## Notes

- The dataset is a small, curated seed set (~44 entries) covering everyday opinions, habits, and personality traits. It's intentionally personal and honest rather than exhaustive — the architecture is built to scale with more data over time.
- This project started out exploring WhatsApp chat exports as a data source, but personal chat data raised privacy concerns (other people's messages, sensitive content), so the final version uses a self-authored dataset instead.

## Future improvements

- Expand the dataset with more entries for richer retrieval
- Add a lightweight evaluation step (faithfulness/relevance scoring) to catch hallucinated answers
- Support follow-up/multi-turn conversation instead of single-question queries
