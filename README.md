# ⚖️ LegalGPT - Hybrid RAG Legal Judgment Assistant

LegalGPT is a Hybrid Retrieval-Augmented Generation (RAG) system for Indian legal judgments. It combines traditional keyword search (BM25), semantic vector search, Elasticsearch, and Claude AI to retrieve, rank, and explain relevant legal judgments through an interactive chat interface.

---

## Features

- Hybrid Retrieval (BM25 + Semantic Search)
- Elasticsearch-based legal document indexing
- Claude AI powered judgment reranking
- AI-generated judgment explanations
- Modern React frontend
- Markdown-based responses
- Explain judgments with metadata
- Conversation memory (basic)
- Hybrid Legal AI architecture

---

## Architecture

```
                    User Query
                         │
                         ▼
                  Intent Detection
                         │
                         ▼
               Metadata Extraction
                         │
                         ▼
          ┌────────────────────────┐
          │                        │
          ▼                        ▼
     Metadata Search         Semantic Search
       (BM25)              (SentenceTransformer)
          │                        │
          └──────────────┬─────────┘
                         ▼
              Reciprocal Rank Fusion
                         │
                         ▼
               Claude AI Reranker
                         │
                         ▼
                Top Relevant Cases
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
  Explain Judgment              Continue Search
          │
          ▼
     Claude AI Explanation
          │
          ▼
      React Frontend
```

---

## Tech Stack

### Backend

- Python
- Flask
- Elasticsearch
- Sentence Transformers
- Anthropic Claude API

### Frontend

- React
- Vite
- React Markdown
- Lucide React

### AI Components

- Claude Haiku 4.5
- Hybrid RAG
- Semantic Search
- Metadata Search

---

## Project Structure

```
BETA-Architecture/

│── app.py
│── config.py
│── requirements.txt
│── README.md

├── llm/
│   └── claude_client.py

├── memory/
│   └── conversation_memory.py

├── metadata/
│   ├── create_index.py
│   ├── document_lookup.py
│   ├── index_docs.py
│   └── search.py

├── query_processor/
│   ├── explain.py
│   ├── intent.py
│   ├── metadata_extractor.py
│   ├── prompts.py
│   ├── reranker.py
│   └── rerank_prompt.py

├── retrieval/
│   ├── hybrid_pipeline.py
│   ├── merge.py
│   └── metadata_pipeline.py

├── semantic/
│   ├── embeddings.py
│   ├── search.py
│   └── index_docs.py

└── frontend/
```

---

## Retrieval Pipeline

```
User Query
      │
      ▼
Metadata Extraction
      │
      ▼
BM25 Search
      │
      ▼
Semantic Search
      │
      ▼
Result Fusion
      │
      ▼
Claude Reranking
      │
      ▼
Top Legal Judgments
```

---

## Explanation Pipeline

```
Selected Judgment
        │
        ▼
Retrieve Judgment
        │
        ▼
Claude AI
        │
        ▼
Facts

Legal Issues

Court's Reasoning

Final Decision

Key Legal Principles
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/LegalGPT.git

cd LegalGPT
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Update `config.py` with:

- Anthropic API Key
- Elasticsearch URL
- Elasticsearch Username
- Elasticsearch Password

---

## Run Backend

```bash
python app.py
```

Backend runs at

```
http://localhost:5000
```

---

## Run Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

## Current Capabilities

- Hybrid Legal Search
- AI Judgment Ranking
- AI Judgment Explanation
- Elasticsearch Integration
- Semantic Search
- Metadata Search
- React Chat Interface
- Markdown Rendering

---

## Future Improvements

- Conversational Legal Assistant
- Multi-turn Dialogue
- Explain from Conversation Memory
- Compare Multiple Judgments
- Citation Graph
- Case Timeline
- Bookmark Judgments
- Export Explanations
- PDF Upload Support
- Streaming Responses
- Authentication
- User Profiles

---

## Screenshots

Add screenshots here.

```
frontend/
backend/
judgment cards/
explanation/
```

---

## License

This project is intended for educational and research purposes.

---

## Author

Developed as part of an AI Legal Research internship project.

```

---

### One suggestion before you push

Your project will look much more professional if you rename the repository from something like:

```
BETA-Architecture
```

to:

```
LegalGPT
```

or

```
LegalGPT-Hybrid-RAG
```

It immediately tells people what the repository is about and looks cleaner on GitHub.