
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

## Architecture
SQL data → Pickle vector store → Embedding retrieval → RAG reasoning → Structured output

## Tech Stack
Python, OpenAI API, NumPy, Pandas, pdfplumber, Streamlit, Pickle, RAG

## How To Run

1. Clone this repo
2. Install dependencies:
   pip install -r requirements.txt
3. Create a .env file and add:
   OPENAI_API_KEY=your_openai_key_here
4. Run the app:
   streamlit run app.py
