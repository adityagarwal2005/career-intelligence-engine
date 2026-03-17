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
SQL data → Pickle vector store → Embedding retrieval → RAG reas
