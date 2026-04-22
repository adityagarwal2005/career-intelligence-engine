# Career Intelligence Suite

An AI-powered platform for career planning, role discovery, and resume optimization. This comprehensive tool leverages OpenAI's language models to analyze careers, identify skill gaps, create growth roadmaps, and optimize resumes for target positions.

## Overview

Career Intelligence Suite combines a user-friendly Streamlit frontend with a robust FastAPI backend to deliver:
- **Career Discovery**: Identify suitable career roles based on skills and experience
- **Skill Gap Analysis**: Understand the gap between current and target role requirements
- **Career Roadmaps**: Generate actionable 90-day plans for skill development
- **Career Simulation**: Model 2-year career progression scenarios
- **Resume Optimization**: Tailor resumes to job descriptions with AI-powered matching

## Architecture

The application follows a client-server architecture:

```
User Interface (Streamlit)
        ↓
HTTP Requests (FastAPI)
        ↓
Backend Services (LLM + Resume Optimization)
        ↓
OpenAI API (gpt-4o-mini)
```

## Core Modules

### 1. Career App (`career_app/`)
**Streamlit-based user interface** for career intelligence workflows

**Key Components:**
- `app.py` - Main Streamlit application and UI orchestration
- `pipeline.py` - Career analysis pipeline with:
  - Embedding-based role discovery using pre-computed embeddings
  - Skill gap analysis with readiness signals
  - 90-day actionable roadmap generation
  - Career path simulation (2-year projection)
- `api.py` - Integration with FastAPI backend for resume optimization
- `data1.pkl` & `data2.pkl` - Pre-computed embeddings for career roles and skills

**Features:**
- Resume upload (PDF, DOCX, TXT, MD)
- Text-based career analysis
- Real-time skill gap visualization
- Interactive career progression simulation
- Resume optimization with AI matching

### 2. Optimizer Backend (`optimizer_backend/backend/`)
**FastAPI service** for resume analysis and optimization

**Architecture:**
```
optimizer_backend/backend/
├── main.py                    # FastAPI app factory
├── app/
│   ├── config.py             # Settings and configuration
│   ├── factory.py            # Service initialization
│   ├── schemas.py            # Request/response models
│   ├── prompts.py            # LLM prompts for optimization
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── services/
│   │   ├── llm_service.py    # OpenAI API interactions
│   │   ├── optimizer_service.py # Resume optimization logic
│   │   └── project_scorer.py  # Project relevance scoring
│   └── utils/
│       ├── resume_parser.py  # PDF, DOCX, TXT parsing
│       └── formatter.py      # Text formatting utilities
└── data/
    └── projects_dataset.json # Reference projects for matching
```

**API Endpoints:**
- `GET /health` - Health check and service status
- `POST /analyze` - Analyze resume against job description (text input)
- `POST /analyze-upload` - Analyze uploaded resume file against job description

**Services:**
- **LLM Service**: Manages OpenAI API calls with configurable temperature settings
- **Resume Optimizer**: Generates optimized resume suggestions based on job descriptions
- **Project Scorer**: Scores and ranks projects by relevance
- **Resume Parser**: Extracts text from PDF, DOCX, TXT, and MD files

## Project Structure

```text
career-intelligence-suite/
├── README.md                           # This file
├── career_app/
│   ├── app.py                         # Main Streamlit app
│   ├── api.py                         # Backend API integration
│   ├── pipeline.py                    # Career analysis pipeline
│   ├── data1.pkl                      # Role embeddings
│   ├── data2.pkl                      # Skill embeddings
│   └── requirements.txt               # Python dependencies
│
└── optimizer_backend/
    └── backend/
        ├── main.py                    # FastAPI app factory
        ├── requirements.txt           # Backend dependencies
        ├── .env.example               # Environment template
        └── app/
            ├── __init__.py
            ├── config.py              # Configuration and settings
            ├── factory.py             # App initialization
            ├── schemas.py             # Pydantic request/response models
            ├── prompts.py             # LLM prompt templates
            ├── api/
            │   ├── __init__.py
            │   └── routes.py          # API route handlers
            ├── services/
            │   ├── llm_service.py     # OpenAI service
            │   ├── optimizer_service.py # Resume optimization
            │   └── project_scorer.py  # Project scoring
            ├── utils/
            │   ├── resume_parser.py   # Document parsing
            │   └── formatter.py       # Text formatting
            └── data/
                └── projects_dataset.json # Reference data
```

## Technology Stack

**Frontend:**
- Streamlit 1.x - Interactive UI framework
- pandas, numpy - Data manipulation
- pdfplumber - PDF extraction

**Backend:**
- FastAPI 0.115+ - High-performance API framework
- Uvicorn - ASGI server
- Pydantic 2.x - Data validation

**AI & LLM:**
- OpenAI API (gpt-4o-mini) - Language model
- text-embedding-3-small - Semantic embeddings

**Data Processing:**
- pypdf / PyPDF2 - PDF parsing
- python-docx - DOCX parsing
- python-multipart - File upload handling

## Prerequisites

- **Python 3.11+**
- **OpenAI API Key** (for gpt-4o-mini model)
- **pip** or equivalent package manager

## Installation

### 1. Clone Repository

```bash
cd /Users/adityaagarwal/Downloads/career-intelligence-suite
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install career app dependencies
.venv/bin/python -m pip install -r career_app/requirements.txt

# Install backend dependencies
.venv/bin/python -m pip install -r optimizer_backend/backend/requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in `optimizer_backend/backend/`:

```bash
cp optimizer_backend/backend/.env.example optimizer_backend/backend/.env
```

Edit `optimizer_backend/backend/.env` and set:

```env
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
TEMP_ANALYSIS=0.2
TEMP_COMPOSITION=0.35
TEMP_QA=0.1
MAX_RETRIES=2
```

**Settings Explanation:**
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (fixed to gpt-4o-mini)
- `TEMP_ANALYSIS` - Temperature for analytical tasks (0.0-1.0)
- `TEMP_COMPOSITION` - Temperature for text generation (0.0-1.0)
- `TEMP_QA` - Temperature for Q&A tasks (0.0-1.0)
- `MAX_RETRIES` - Number of retry attempts on API failure

## Running the Application

### Option 1: Using Two Terminals (Recommended)

**Terminal 1 - Start Backend Server:**

```bash
cd /Users/adityaagarwal/Downloads/career-intelligence-suite
source .venv/bin/activate
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 --app-dir optimizer_backend
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Terminal 2 - Start Streamlit App:**

```bash
cd /Users/adityaagarwal/Downloads/career-intelligence-suite
source .venv/bin/activate
python -m streamlit run career_app/app.py
```

Expected output:
```
Local URL: http://127.0.0.1:8501
Network URL: http://xxx.xxx.xxx.xxx:8501
```

### Option 2: Using Process Manager (Production)

Use tools like `supervisord` or `systemd` to manage both services.

## Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Streamlit UI** | `http://127.0.0.1:8501` | Main application interface |
| **Backend Health** | `http://127.0.0.1:8000/health` | Server status check |
| **API Docs** | `http://127.0.0.1:8000/docs` | Swagger UI documentation |
| **ReDoc** | `http://127.0.0.1:8000/redoc` | Alternative API documentation |

## Usage Workflows

### 1. Career Discovery
1. Open Streamlit UI
2. Enter resume or relevant text
3. System identifies suitable career roles
4. View ranked recommendations with match scores

### 2. Skill Gap Analysis
1. Select a target career role
2. System analyzes current vs. required skills
3. View gap visualization and readiness signals
4. Identify high-priority skill areas

### 3. Generate 90-Day Roadmap
1. Choose target role and skill gaps
2. System generates actionable milestones
3. View week-by-week action items
4. Export or save roadmap

### 4. Career Simulation
1. Select target role and learning parameters
2. System models 2-year career progression
3. View projected growth and outcomes
4. Analyze different scenarios

### 5. Resume Optimization
1. Upload resume and job description
2. Select optimization mode:
   - `ai_match` - AI-powered intelligent matching
   - `my_dataset` - Match against internal dataset
3. Review optimized suggestions
4. Download optimized resume

## API Documentation

### Health Check
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

### Analyze Resume (Text Input)
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Your resume text here",
    "job_description": "Job description here",
    "mode": "ai_match"
  }'
```

### Analyze Resume (File Upload)
```bash
curl -X POST "http://127.0.0.1:8000/analyze-upload" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Job description here" \
  -F "mode=ai_match"
```

## Troubleshooting

### Backend Connection Issues
**Problem:** Streamlit shows "Backend offline"
```bash
# Test backend health
curl http://127.0.0.1:8000/health

# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### OpenAI API Key Issues
**Problem:** "OPENAI_API_KEY is missing" error
- Verify `.env` file exists at `optimizer_backend/backend/.env`
- Check that OPENAI_API_KEY is set correctly (no spaces)
- Ensure file permissions allow reading
```bash
cat optimizer_backend/backend/.env | grep OPENAI_API_KEY
```

### Port Already in Use
**Problem:** "Address already in use" error
```bash
# Kill existing processes
pkill -f "uvicorn"  # Backend
pkill -f "streamlit"  # Frontend

# Or specify different ports
python -m uvicorn backend.main:app --port 8001 --app-dir optimizer_backend
streamlit run career_app/app.py --server.port 8502
```

### Resume Parsing Issues
**Problem:** "Resume text is too short" error
- Ensure resume has at least 40 characters
- Try different file formats (PDF, DOCX, TXT)
- Check file integrity

### Dependencies Installation Issues
```bash
# Upgrade pip
.venv/bin/python -m pip install --upgrade pip

# Clear cache and reinstall
.venv/bin/python -m pip install --no-cache-dir -r career_app/requirements.txt
.venv/bin/python -m pip install --no-cache-dir -r optimizer_backend/backend/requirements.txt
```

## Configuration & Environment

### Temperature Settings
The LLM temperature controls response randomness:
- **0.0** - Deterministic, consistent responses
- **0.1-0.2** - Analytical tasks (low variation)
- **0.3-0.5** - Balanced tasks (moderate variation)
- **0.7-1.0** - Creative tasks (high variation)

### Performance Tuning
- Increase `MAX_RETRIES` for unstable networks
- Adjust temperatures based on use case
- Monitor OpenAI API usage and costs

## Security Considerations

⚠️ **Critical Security Guidelines:**

1. **API Keys**
   - Never commit `.env` files to version control
   - Never hardcode API keys in source code
   - Use environment variables exclusively
   - Add `.env` to `.gitignore`:
     ```
     optimizer_backend/backend/.env
     career_app/.env
     .venv/
     __pycache__/
     *.pkl
     ```

2. **File Uploads**
   - Validate file types and sizes
   - Sanitize file names
   - Store uploads in temporary directories
   - Implement file size limits

3. **API Security**
   - Use HTTPS in production
   - Implement rate limiting
   - Add authentication for deployment
   - Enable CORS appropriately

4. **Data Privacy**
   - Never log sensitive resume data
   - Implement data retention policies
   - Encrypt sensitive information in transit
   - Consider GDPR/privacy regulations

## Development Guide

### Project Structure Overview
- **Frontend**: Streamlit handles UI, session state, and user interactions
- **Backend**: FastAPI provides REST endpoints and business logic
- **Pipeline**: LLM-powered career analysis with embedding-based matching
- **Services**: Modular service layer for maintainability

### Adding New Features

**Adding API Endpoint:**
1. Define schema in `app/schemas.py`
2. Implement logic in `app/services/`
3. Add route in `app/api/routes.py`
4. Test with `curl` or FastAPI docs

**Adding Streamlit Page:**
1. Create new function in `career_app/app.py`
2. Use session state for data persistence
3. Call API endpoints as needed
4. Add UI components with `st.` functions

### Testing
```bash
# Test backend with pytest
pytest optimizer_backend/

# Manual API testing
python -m pytest -v --tb=short
```

## Performance Optimization

- **Embeddings**: Pre-computed and cached in pickle files
- **API Calls**: Batch requests where possible
- **Streamlit**: Use `@st.cache_data` for expensive operations
- **Database**: Consider SQLite for larger datasets

## Deployment

### Production Deployment Checklist
- [ ] Set environment variables on server
- [ ] Use production ASGI server (Gunicorn + Uvicorn)
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Implement authentication
- [ ] Set up automated backups
- [ ] Use process manager (systemd/supervisord)

### Docker Support (Optional)
Create `Dockerfile` for containerization:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes and test thoroughly
3. Commit with clear messages: `git commit -m "Add feature X"`
4. Push and create pull request
5. Ensure all tests pass before merging

## License

[Add your license here]

## Support & Contact

For issues, questions, or suggestions:
- Open an issue on the repository
- Contact the development team
- Check existing documentation

## Changelog

### Version 1.0.0 (Current)
- ✅ Career discovery with embedding-based matching
- ✅ Skill gap analysis with readiness signals
- ✅ 90-day action roadmap generation
- ✅ Career path simulation (2-year projection)
- ✅ Resume optimization with AI matching
- ✅ Multi-format resume parsing (PDF, DOCX, TXT, MD)
- ✅ FastAPI backend with health monitoring
- ✅ Streamlit interactive UI

## Roadmap

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and profiles
- [ ] Resume template library
- [ ] Interview preparation module
- [ ] Job market analytics dashboard
- [ ] Mobile application support
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
