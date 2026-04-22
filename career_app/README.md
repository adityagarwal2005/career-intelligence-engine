# Career Intelligence Engine

An AI-powered system that maps your skills to career roles
using embeddings, cosine similarity, and multi-agent reasoning.

## What It Does
- Accepts text input or resume (PDF)
- Extracts skill signals and generates OpenAI embeddings
- Matches against precomputed role embedding matrix
- Returns top 3 aligned career roles
- Skill gap analysis with readiness score
- 90-day execution roadmap
- 2-year career progression simulation
- REST API with 5 live endpoints via FastAPI

## Architecture
SQL data → Pickle vector store → Embedding retrieval → RAG reasoning → Structured output → REST API

## Tech Stack
Python, OpenAI API, NumPy, Pandas, pdfplumber, Streamlit, FastAPI, Pickle, RAG

## How To Run

### Streamlit App
1. Clone this repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a .env file and add:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

### REST API
1. Install FastAPI dependencies:
   ```
   pip install fastapi uvicorn python-multipart
   ```
2. Run the API server:
   ```
   uvicorn api:app --reload
   ```
3. Visit the interactive API explorer:
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze/text` | Analyze skills from text input |
| POST | `/api/analyze/resume` | Analyze skills from PDF resume |
| POST | `/api/gap` | Skill gap analysis for a target role |
| POST | `/api/roadmap` | Generate 90-day learning roadmap |
| POST | `/api/simulate` | Simulate 2-year career progression |

## Project Structure
```
├── app.py          # Streamlit frontend
├── api.py          # FastAPI REST layer
├── pipeline.py     # Core AI pipeline
├── data1.pkl       # Precomputed skill embeddings
├── data2.pkl       # Role mapping data
└── .env            # API keys (not committed)
```

---
Designed by Aditya Agarwal — Semantic intelligence • Structured AI reasoning • REST API