# WebMethods to Boomi Migration Tool - Backend

FastAPI backend service that uses LangChain and OpenRouter's Claude Opus 4 model to analyze webMethods files and generate Boomi migration plans.

## Features

- FastAPI REST API with full CORS support
- LangChain integration with OpenRouter API
- Claude Opus 4 model for intelligent migration analysis
- Three-phase analysis process:
  - **Research Phase**: Automated web search for webMethods and Boomi architectures
  - **Analysis Phase**: Deep analysis of webMethods integration patterns
  - **Generation Phase**: Creation of specific Boomi AI prompts
- Web search integration for current best practices
- Customizable prompts via properties file
- Batch file processing
- Automatic Plan.md generation with executable Boomi AI prompts

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

3. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /migrate` - Upload files and get migration plan (multipart/form-data)
- `POST /migrate/json` - Alternative JSON endpoint

## Customizing the Prompt

Edit `prompts/migration_prompt.properties` to customize the migration analysis prompt. The application will automatically load changes without requiring a restart.

The prompt structure includes:
- **Phase 1**: Research instructions for web search
- **Phase 2**: File analysis guidelines
- **Phase 3**: Boomi AI prompt generation templates
- **Output Format**: Structured Plan.md template

The LLM will:
1. Research both platforms using web search
2. Analyze your webMethods files
3. Generate specific Boomi AI prompts that can be directly executed in Boomi

## CORS Configuration

The backend is configured to accept requests from any origin (`*`) to support cross-machine access. For production, update the CORS settings in `app/main.py` to restrict to specific origins.

## File Support

- Accepts `.html` and `.txt` files
- Multiple files processed as a batch
- Returns a single comprehensive Plan.md file
