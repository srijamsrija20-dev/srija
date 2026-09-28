# LegalEase AI

## AI-Powered Legal Document Assistant

LegalEase AI is a Generative AI-based application that helps users
understand, analyze, summarize, and generate legal documents easily.

## Team

- Srija M – Team Lead
- Srivarshini M S – Team Member
- Subashree G – Team Member
- Subiksha M – Team Member


LegalEasy AI/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   ├── ai_core/
│   │   ├── __init__.py
│   │   └── gemini_generator.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── document_exporters.py
│
├── frontend/
│   └── app.py
│
├── generated_documents/
│   └── [Generated legal documents]
│
├── uploads/
│   └── [Uploaded documents]
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE# LegalEase AI

## AI-Powered Legal Document Assistant

LegalEase AI is a Generative AI-based application that helps users
understand, analyze, summarize, and generate legal documents easily.

## Team

- Srija M – Team Lead
- Srivarshini M S – Team Member
- Subashree G – Team Member
- Subiksha M – Team Member

## Features

- Legal document analysis
- Document summarization
- AI-powered document generation
- Simple Gradio interface
- Document export
- Gemini AI integration

## Technologies

- Python
- Gradio
- FastAPI
- Google Gemini AI
- Uvicorn

## How to Run

### Backend

```bash
python -m uvicorn backend.main:app