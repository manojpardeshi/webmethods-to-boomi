import os
import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import Tool
from dotenv import load_dotenv

from ..models import FileUpload
from ..config.prompt_config import PromptConfig

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class LangChainService:
    def __init__(self):
        """Initialize LangChain service with OpenRouter configuration"""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.model_name = os.getenv("MODEL_NAME", "anthropic/claude-opus-4")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        # Initialize LLM with OpenRouter
        # Note: Headers are set via environment or passed differently in newer versions
        self.llm = ChatOpenAI(
            model=self.model_name,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
            temperature=0.7,
            max_tokens=4000  # Limit output tokens
        )
        
        # Initialize search tool
        self.search = DuckDuckGoSearchRun()
        
        # Load prompt configuration
        self.prompt_config = PromptConfig()
        
        logger.info(f"LangChain service initialized with model: {self.model_name}")
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough estimation of tokens (1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def _truncate_content(self, content: str, max_chars: int = 50000) -> str:
        """Truncate content to avoid token limits"""
        if len(content) > max_chars:
            logger.warning(f"Content truncated from {len(content)} to {max_chars} characters")
            return content[:max_chars] + "\n\n[Content truncated due to length...]"
        return content
    
    def _chunk_files(self, files: List[FileUpload], max_chars_per_chunk: int = 40000) -> List[List[FileUpload]]:
        """Split files into chunks to avoid token limits"""
        chunks = []
        current_chunk = []
        current_size = 0
        
        for file in files:
            file_size = len(file.content)
            
            # If single file is too large, truncate it
            if file_size > max_chars_per_chunk:
                truncated_file = FileUpload(
                    filename=file.filename,
                    content=self._truncate_content(file.content, max_chars_per_chunk)
                )
                chunks.append([truncated_file])
                continue
            
            # If adding this file would exceed limit, start new chunk
            if current_size + file_size > max_chars_per_chunk and current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_size = 0
            
            current_chunk.append(file)
            current_size += file_size
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _perform_research_phase(self) -> str:
        """Perform automated research on webMethods and Boomi architectures"""
        logger.info("Starting research phase...")
        
        # Skip research phase if rate limited or provide fallback content
        research_content = """
        ## Research Summary (Cached)
        
        ### webMethods Architecture:
        - Flow services use pipeline for data passing between steps
        - Built-in services for data transformation, branching, and looping
        - Adapter services for SAP, JDBC, JMS, REST, SOAP integrations
        - Document types define data structures
        - Error handling through try-catch blocks
        
        ### Boomi Architecture:
        - Processes use shapes connected by lines
        - Connectors for various systems (SAP, Database, HTTP, etc.)
        - Map shape for data transformation
        - Decision shape for branching logic
        - Try/Catch shape for error handling
        
        ### Migration Patterns:
        - webMethods BRANCH → Boomi Decision shape
        - webMethods MAP → Boomi Map shape
        - webMethods adapter services → Boomi connectors
        - webMethods pipeline → Boomi process properties
        - webMethods pub.flow:debugLog → Boomi Notify shape
        """
        
        # Try search but don't fail if rate limited
        try:
            # Limit to 2 queries to reduce rate limit issues
            priority_queries = [
                "webMethods to Boomi migration guide",
                "Boomi AI prompt examples"
            ]
            
            search_results = []
            for query in priority_queries[:1]:  # Only try one query
                try:
                    result = self.search.run(query)
                    search_results.append(f"\nLive Search - {query}:\n{result[:300]}...")
                    # Add delay to avoid rate limiting
                    import time
                    time.sleep(2)
                except Exception as e:
                    logger.warning(f"Search skipped for '{query}': {e}")
            
            if search_results:
                research_content += "\n\n### Live Search Results:\n" + "\n".join(search_results)
        except Exception as e:
            logger.warning(f"Research phase using cached content due to: {e}")
        
        return research_content
    
    def _analyze_chunk(self, files_chunk: List[FileUpload], research_context: str) -> str:
        """Analyze a chunk of files"""
        # Prepare file contents
        file_contents = "\n\n".join([
            f"=== File: {file.filename} ===\n{file.content}"
            for file in files_chunk
        ])
        
        # Get prompt template and replace placeholder
        prompt_template = self.prompt_config.get_prompt_template()
        
        # Create a more concise prompt to avoid token limits
        concise_prompt = f"""
You are an expert integration architect specializing in migrating webMethods to Boomi.

## Research Context (Summary)
{research_context[:2000]}...

## Files to Analyze
{file_contents}

## Task
Generate specific, executable Boomi AI prompts for migrating these webMethods integrations.

## Output Format
Provide a structured migration plan with:
1. Process overview
2. Specific Boomi AI prompts (ready to execute)
3. Implementation notes
4. Key considerations

Focus on actionable Boomi AI prompts, not general advice.
"""
        
        # Create messages
        messages = [
            SystemMessage(content="You are an expert in webMethods to Boomi migration."),
            HumanMessage(content=concise_prompt)
        ]
        
        # Get response from LLM
        response = self.llm.invoke(messages)
        return response.content
    
    def process_migration(self, files: List[FileUpload]) -> str:
        """Process webMethods files and generate migration plan"""
        try:
            logger.info(f"Processing {len(files)} files for migration")
            
            # Perform research phase (limited to save tokens)
            research_context = self._perform_research_phase()
            research_summary = research_context[:3000]  # Limit research context
            
            # Chunk files to avoid token limits
            file_chunks = self._chunk_files(files)
            logger.info(f"Split files into {len(file_chunks)} chunks")
            
            # Process each chunk
            chunk_results = []
            for i, chunk in enumerate(file_chunks):
                logger.info(f"Processing chunk {i+1}/{len(file_chunks)} with {len(chunk)} files")
                try:
                    result = self._analyze_chunk(chunk, research_summary)
                    chunk_results.append(result)
                except Exception as e:
                    logger.error(f"Error processing chunk {i+1}: {e}")
                    chunk_results.append(f"Error processing chunk {i+1}: {str(e)}")
            
            # Combine results
            if len(chunk_results) == 1:
                final_plan = chunk_results[0]
            else:
                # Summarize multiple chunks
                final_plan = self._combine_chunk_results(chunk_results)
            
            # Ensure the plan starts with proper markdown
            if not final_plan.startswith("# WebMethods to Boomi Migration Plan"):
                final_plan = "# WebMethods to Boomi Migration Plan\n\n" + final_plan
            
            return final_plan
            
        except Exception as e:
            logger.error(f"Error in process_migration: {e}")
            raise
    
    def _combine_chunk_results(self, chunk_results: List[str]) -> str:
        """Combine results from multiple chunks into a cohesive plan"""
        combined_content = "\n\n".join([
            f"## Part {i+1}\n{result}"
            for i, result in enumerate(chunk_results)
        ])
        
        # Use LLM to create a cohesive summary
        summary_prompt = f"""
Combine these migration plan parts into a single, cohesive migration plan:

{combined_content[:10000]}...

Create a unified Plan.md with:
1. Executive Summary
2. All identified processes
3. Consolidated Boomi AI prompts
4. Implementation strategy
"""
        
        messages = [
            SystemMessage(content="You are an expert in creating migration plans."),
            HumanMessage(content=summary_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
