# Career Intelligence Suite

An AI-powered platform for career planning, role discovery, and resume optimization. All features run locally in a single Streamlit application powered by OpenAI's language models.

## Features

- 🎯 **Career Discovery** - Identify suitable career roles based on skills and experience
- 📊 **Skill Gap Analysis** - Understand gaps between current and target role requirements
- 🛣️ **90-Day Roadmap** - Generate actionable plans for skill development
- 📈 **Career Simulation** - Model 2-year career progression scenarios
- ✨ **Resume Optimization** - Tailor resumes to job descriptions with AI-powered matching

## Quick Start

### Prerequisites

- **Python 3.11+**
- **OpenAI API Key** (for gpt-4o-mini model)

### Installation

1. **Navigate to project directory:**
```bash
cd career-intelligence-suite
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r src/requirements.txt
```

4. **Configure API key (Local Development):**

Edit `src/services/.env`:
```env
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
TEMP_ANALYSIS=0.2
TEMP_COMPOSITION=0.35
TEMP_QA=0.1
MAX_RETRIES=2
```

**For Streamlit Cloud:** Add secrets through the dashboard instead (see Streamlit Cloud Deployment section below).

### Run the Application

**Option 1 - Direct Streamlit command (Recommended for local development):**
```bash
streamlit run src/ui/app.py
```

**Option 2 - Using the run script:**
```bash
python run.py
```

The app will be available at: **http://localhost:8501**

## Streamlit Cloud Deployment

Deploy this application to Streamlit Cloud to get a shareable public link for your resume:

### Steps to Deploy

1. **Push your code to GitHub:**
   ```bash
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to `src/ui/app.py`
   - Click "Deploy"

3. **Add your OpenAI API Key:**
   - In your Streamlit Cloud app dashboard, go to **Settings** → **Secrets**
   - Add your environment variables:
     ```
     OPENAI_API_KEY = "sk-your_actual_openai_api_key_here"
     OPENAI_MODEL = "gpt-4o-mini"
     TEMP_ANALYSIS = 0.2
     TEMP_COMPOSITION = 0.35
     TEMP_QA = 0.1
     MAX_RETRIES = 2
     ```
   - Click "Save"

4. **Your app is live!** You can now share the Streamlit Cloud URL in your resume and portfolio.

**Note:** The `.streamlit/config.toml` and `.streamlit/secrets.toml.example` files are configured for Streamlit Cloud deployment.

## Project Structure

```
career-intelligence-suite/
├── run.py                          # Main entry point
├── README.md                       # This file
├── src/requirements.txt            # Python dependencies
│
└── src/                            # Unified application source
    ├── __init__.py
    ├── ui/                         # Streamlit UI
    │   ├── __init__.py
    │   └── app.py                  # Main application
    │
    ├── pipeline/                   # Career analysis pipeline
    │   ├── __init__.py
    │   └── pipeline.py             # Analysis logic
    │
    ├── services/                   # Optimizer & LLM services
    │   ├── .env                    # API configuration
    │   ├── __init__.py
    │   ├── config.py               # Settings management
    │   ├── prompts.py              # LLM prompt templates
    │   ├── schemas.py              # Data models
    │   ├── services/
    │   │   ├── llm_service.py      # OpenAI API calls
    │   │   ├── optimizer_service.py # Resume optimization
    │   │   └── project_scorer.py    # Project relevance
    │   └── utils/
    │       ├── resume_parser.py    # PDF parsing
    │       └── formatter.py        # Text formatting
    │
    └── data/                       # Application data
        ├── data1.pkl               # Role embeddings
        ├── data2.pkl               # Skill embeddings
        └── projects_dataset.json   # Reference projects
```

## Usage Workflows

### 1. Resume Analyzer
1. Open the app → "Resume Analyzer" tab
2. Upload a resume (PDF) or enter text description
3. Click "Generate Insights"
4. Choose a role to explore:
   - **Analyze Skill Gap** - See readiness score and missing skills
   - **Generate 90 Day Roadmap** - Get week-by-week action plan
   - **Simulate 2-Year Growth** - Project career evolution

### 2. Resume Optimization
1. Go to "Resume Optimization" tab
2. Upload your resume (PDF)
3. Enter the target job description
4. Choose optimization mode:
   - **🤖 AI Match** - Full AI-powered intelligent matching
   - **📁 My Dataset** - Match against internal projects
5. Review suggestions and download (TXT or PDF)

## Configuration

### Temperature Settings

Control LLM creativity:
- `TEMP_ANALYSIS=0.2` - Low (consistent analysis)
- `TEMP_COMPOSITION=0.35` - Medium (balanced suggestions)
- `TEMP_QA=0.1` - Very low (precise Q&A)

### API Settings

- `MAX_RETRIES=2` - Retry failed API calls
- `OPENAI_MODEL=gpt-4o-mini` - Model selection (fixed)

## Troubleshooting

### OpenAI API Key Issues
```bash
# Verify .env file exists
cat src/services/.env | grep OPENAI_API_KEY

# Check key format (should start with sk-)
```

### Port Already in Use
```bash
# Run on different port
python -m streamlit run src/ui/app.py --server.port 8502
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r src/requirements.txt --force-reinstall
```

### Data Files Missing
```bash
# Verify data files exist
ls -la src/data/
# Should show: data1.pkl, data2.pkl, projects_dataset.json
```

## Architecture

```
User Input
    ↓
Streamlit UI (src/ui/app.py)
    ↓
Career Pipeline (src/pipeline/)
    ├→ Role Discovery
    ├→ Skill Gap Analysis
    ├→ Roadmap Generation
    └→ Career Simulation
    ↓
Optimizer Services (src/services/)
    ├→ LLM Service (OpenAI API)
    ├→ Resume Optimizer
    └→ Project Scorer
    ↓
OpenAI API (gpt-4o-mini)
```

## Technology Stack

- **Frontend:** Streamlit 1.55+
- **Backend Services:** Python 3.11+
- **AI/LLM:** OpenAI API (gpt-4o-mini)
- **Data:** Pandas, NumPy, Scikit-learn
- **File Handling:** PyPDF2, python-docx

## Development

### Adding New Features

1. **UI Changes** → Edit `src/ui/app.py`
2. **Analysis Logic** → Update `src/pipeline/pipeline.py`
3. **LLM Prompts** → Modify `src/services/prompts.py`
4. **API Configuration** → Check `src/services/config.py`

### Testing Imports
```bash
source .venv/bin/activate
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from services.config import get_settings
from pipeline.pipeline import career_agent_pipeline
print('✓ All imports working')
"
```

## License

Built by Aditya Agarwal

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify `src/services/.env` configuration
3. Ensure OpenAI API key is valid
4. Check that all data files exist in `src/data/`
