

# import google.generativeai as genai
# from config.config import GEMINI_API_KEY

# try:
#     genai.configure(api_key="AIzaSyA0XkLtOhUgwooQ0eT8niaPqyYTmptTHjQ")
#     # List available models to verify
#     available_models = [m.name for m in genai.list_models()]
#     print(f"Available models: {available_models}")
    
#     # Use a supported model from the list (e.g., gemini-1.5-pro-001)
#     model = genai.GenerativeModel('gemini-1.5-pro-001')
# except Exception as e:
#     raise Exception(f"Failed to configure Gemini API: {str(e)}")

# def get_learning_response(prompt):
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         raise Exception(f"Error generating response: {str(e)}")




import os
from dotenv import load_dotenv
import requests

# Load API keys from .env
load_dotenv()

# Get the OpenRouter API Key
API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"  # Popular model available on OpenRouter

# Core function to get response from OpenRouter
def get_learning_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }
        
        response = requests.post(OPENROUTER_BASE_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Unexpected response format: {result}")
            
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")
