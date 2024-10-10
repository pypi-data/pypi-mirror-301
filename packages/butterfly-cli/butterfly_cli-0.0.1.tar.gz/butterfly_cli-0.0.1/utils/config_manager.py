import os
from dotenv import load_dotenv
from .encryption_utils import decrypt_prompt

def root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ConfigManager:
    def __init__(self):
        load_dotenv(os.path.join(root(), '.env'))  # Load .env file from project root
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Load prompts (they might not be encrypted yet)
        self.manager_prompt = decrypt_prompt('Your manager prompt here')
        self.architecture_prompt = decrypt_prompt('Your architecture prompt here')
        self.performance_prompt = decrypt_prompt('Your performance prompt here')
        self.static_prompt = decrypt_prompt('Your static analysis prompt here')
        self.code_quality_prompt = decrypt_prompt('Your code quality prompt here')
        self.dependency_prompt = decrypt_prompt('Your dependency analysis prompt here')

    def get_openai_api_key(self):
        return self.openai_api_key

    def get_manager_prompt(self):
        return self.manager_prompt

    def get_architecture_prompt(self):
        return self.architecture_prompt

    def get_performance_prompt(self):
        return self.performance_prompt

    def get_static_prompt(self):
        return self.static_prompt

    def get_code_quality_prompt(self):
        return self.code_quality_prompt

    def get_dependency_prompt(self):
        return self.dependency_prompt

# For backwards compatibility
config_manager = ConfigManager()