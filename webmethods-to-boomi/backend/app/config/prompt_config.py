import os
from pathlib import Path


class PromptConfig:
    def __init__(self):
        self.prompt_file = Path(__file__).parent.parent.parent / "prompts" / "migration_prompt.properties"
        self._load_prompt()
    
    def _load_prompt(self):
        """Load prompt template from properties file"""
        if not self.prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
        
        with open(self.prompt_file, 'r') as f:
            content = f.read()
        
        # Extract prompt_template value
        self.prompt_template = ""
        in_prompt = False
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            # Check if this is the start of prompt_template
            if line.startswith('prompt_template='):
                self.prompt_template = line[len('prompt_template='):]
                in_prompt = True
            elif in_prompt:
                # Continue reading multi-line prompt
                self.prompt_template += '\n' + line
    
    def get_prompt_template(self):
        """Get the loaded prompt template"""
        return self.prompt_template.strip()
