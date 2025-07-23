# WebMethods to Boomi Migration Tool

A full-stack application that helps migrate webMethods integration code to Boomi AtomSphere platform using AI-powered analysis.

## Overview

This tool consists of:
- **Frontend**: React TypeScript application with drag-and-drop file upload
- **Backend**: FastAPI server with LangChain and OpenRouter's Claude Opus 4 integration
- **AI Analysis**: Intelligent migration plan generation with web search capabilities

## Architecture

```
webmethods-to-boomi/
├── frontend/          # React TypeScript UI
│   ├── src/
│   │   ├── components/    # File uploader, status display
│   │   ├── services/      # API integration
│   │   └── config/        # Configuration
│   └── public/
│
└── backend/           # FastAPI server
    ├── app/
    │   ├── services/      # LangChain integration
    │   └── config/        # Prompt configuration
    └── prompts/           # Customizable migration prompts
```

## Features

- **Multi-file Upload**: Process multiple webMethods files in a single batch
- **AI-Powered Analysis**: Uses Claude Opus 4 via OpenRouter for intelligent migration planning
- **Automated Research Phase**: LLM automatically researches webMethods and Boomi architectures before analysis
- **Web Search Integration**: Gathers current best practices and migration patterns
- **Boomi AI Prompt Generation**: Creates specific, executable prompts for Boomi AI
- **Customizable Prompts**: Easily modify analysis behavior via properties file
- **Cross-Machine Support**: Full CORS configuration for distributed deployment
- **Automatic Download**: Generated Plan.md automatically downloads to user's machine

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenRouter API key

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

4. Run the server:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env if backend is on different machine
   ```

4. Start development server:
   ```bash
   npm start
   ```

5. Open http://localhost:3000 in your browser

## Usage

1. **Upload Files**: Drag and drop webMethods files (.html, .txt) onto the upload area
2. **Review Selection**: Check the list of selected files
3. **Generate Plan**: Click "Generate Migration Plan" button
4. **Wait for Processing**: The AI analyzes files and searches for best practices
5. **Download Result**: Plan.md automatically downloads when complete

## Configuration

### Backend Configuration
- **API Key**: Set `OPENROUTER_API_KEY` in `.env`
- **Model**: Default is `anthropic/claude-opus-4`
- **Prompt**: Edit `backend/prompts/migration_prompt.properties`

### Frontend Configuration
- **Backend URL**: Set `REACT_APP_BACKEND_URL` in `.env`
- **File Types**: Accepts `.html` and `.txt` files

## Deployment

### Local Network
- Backend runs on `0.0.0.0:8000` (accessible from network)
- Frontend can connect to backend using machine IP
- Current backend machine IP: `192.168.1.165`

To run frontend on a different machine:
1. Copy the frontend folder to the other machine
2. Update `frontend/.env` with backend machine IP:
   ```
   REACT_APP_BACKEND_URL=http://192.168.1.165:8000
   ```
3. Run `npm install` and `npm start` on the frontend machine

### Production
- Build frontend: `npm run build`
- Deploy backend with production ASGI server
- Configure proper CORS origins for security

## Customization

### Modifying the Migration Prompt
Edit `backend/prompts/migration_prompt.properties` to customize:
- Research phase instructions
- Analysis approach
- Boomi AI prompt templates
- Output format structure
- Migration recommendations
- Risk assessment criteria

The prompt includes three phases:
1. **Research Phase**: Automated web search for platform architectures
2. **Analysis Phase**: Deep analysis of webMethods files
3. **Generation Phase**: Creation of specific Boomi AI prompts

### Adding File Types
1. Update frontend validation in `FileUploader.tsx`
2. Update backend validation in `main.py`

## Troubleshooting

- **Connection Issues**: Ensure backend is running and accessible
- **API Errors**: Verify OpenRouter API key is valid
- **CORS Errors**: Check backend CORS configuration
- **File Upload Issues**: Ensure files are in supported formats

## Technology Stack

- **Frontend**: React, TypeScript, Axios
- **Backend**: FastAPI, LangChain, Python
- **AI Model**: Claude Opus 4 via OpenRouter
- **Search**: DuckDuckGo integration

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the individual README files in frontend/ and backend/
2. Ensure all prerequisites are installed
3. Verify API keys and network configuration
