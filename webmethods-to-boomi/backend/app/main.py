import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List
import io
import logging
import traceback
from dotenv import load_dotenv

from .models import MigrationRequest, MigrationResponse, FileUpload
from .services.langchain_service import LangChainService

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="WebMethods to Boomi Migration Tool",
    description="API for migrating webMethods code to Boomi using AI",
    version="1.0.0"
)

# Configure CORS - Allow all origins for cross-machine access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize LangChain service
langchain_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global langchain_service
    try:
        langchain_service = LangChainService()
        logger.info("LangChain service initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing LangChain service: {e}")
        logger.error(traceback.format_exc())
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "WebMethods to Boomi Migration Tool API",
        "version": "1.0.0",
        "endpoints": {
            "migrate": "/migrate",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WebMethods to Boomi Migration Tool",
        "langchain_initialized": langchain_service is not None
    }


@app.post("/migrate")
async def migrate_files(files: List[UploadFile] = File(...)):
    """
    Process multiple webMethods files and generate a migration plan
    """
    try:
        # Validate files
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Read and validate file contents
        file_uploads = []
        for file in files:
            # Check file extension
            if not (file.filename.endswith('.html') or file.filename.endswith('.txt')):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid file type: {file.filename}. Only .html and .txt files are allowed."
                )
            
            # Read file content
            content = await file.read()
            try:
                content_str = content.decode('utf-8')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unable to decode file {file.filename}. Please ensure it's a valid text file."
                )
            
            file_uploads.append(FileUpload(
                filename=file.filename,
                content=content_str
            ))
        
        # Process migration using LangChain
        logger.info(f"Processing {len(file_uploads)} files for migration")
        logger.debug(f"Files: {[f.filename for f in file_uploads]}")
        
        migration_plan = langchain_service.process_migration(file_uploads)
        
        logger.info("Migration plan generated successfully")
        logger.debug(f"Plan length: {len(migration_plan)} characters")
        
        # Create response as downloadable file
        plan_content = migration_plan.encode('utf-8')
        plan_file = io.BytesIO(plan_content)
        plan_file.seek(0)
        
        return StreamingResponse(
            plan_file,
            media_type="text/markdown",
            headers={
                "Content-Disposition": "attachment; filename=Plan.md",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in migrate_files: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing migration: {str(e)}")


@app.post("/migrate/json")
async def migrate_files_json(request: MigrationRequest):
    """
    Alternative endpoint that accepts JSON payload instead of multipart files
    """
    try:
        if not request.files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Process migration using LangChain
        migration_plan = langchain_service.process_migration(request.files)
        
        return MigrationResponse(
            success=True,
            plan_content=migration_plan,
            filename="Plan.md"
        )
        
    except Exception as e:
        return MigrationResponse(
            success=False,
            error=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)
