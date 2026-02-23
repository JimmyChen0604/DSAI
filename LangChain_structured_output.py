import os
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

# 0. Setup #################################

## 0.1 Load .env ############################

def load_env_file(filepath=".env"):
    """Load variables from .env file into environment."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
    else:
        print(".env file not found. Make sure it exists in the project root.")

load_env_file()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file. Please set it up first.")

## 0.2 Schema and LLM ######################

class Itinerary(BaseModel):
    """Structured itinerary: morning, afternoon, evening activities."""
    morning: str
    afternoon: str
    evening: str

llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
structured_llm = llm.with_structured_output(Itinerary)

# 1. Invoke and print ######################

result = structured_llm.invoke("Create a 1-day Tokyo itinerary.")
print(result)