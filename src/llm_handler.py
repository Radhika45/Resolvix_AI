import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from src.logger import logger

load_dotenv()


def get_inference_engine(provider: str = "groq", model_name: str = None, temperature: float = 0.2):
    """
    Returns an inference engine instance based on the selected provider.
    
    Providers supported:
    - 'groq': Cloud inference via ChatGroq
    - 'ollama': Local inference via ChatOllama
    """
    provider_clean = provider.lower().strip()

    if provider_clean == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ_API_KEY not found in environment variables.")
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        # Default model setup
        selected_model = model_name or os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
        
        logger.info(f"Initializing Groq Chat Engine (Model: {selected_model}, Temp: {temperature})...")
        return ChatGroq(
            groq_api_key=api_key,
            model=selected_model,
            temperature=temperature,
            max_tokens=1000,          # Keeps token footprint under Groq limits
            max_retries=6,            # Automatically retries when hitting 429 rate limits
            request_timeout=30.0      # Timeout buffer for queued requests
        )
        
    elif provider_clean == "ollama":
        selected_model = model_name or os.getenv("OLLAMA_MODEL", "llama3.2")
        
        logger.info(f"Initializing Ollama Engine (Model: {selected_model}, Temp: {temperature})...")
        return ChatOllama(
            model=selected_model,
            temperature=temperature
        )
        
    else:
        raise ValueError(f"Unsupported provider: '{provider}'. Choose 'groq' or 'ollama'.")


if __name__ == "__main__":
    try:
        # Initializing Groq Engine Test
        llm = get_inference_engine(provider="groq")
        response = llm.invoke("Summarize the purpose of an AI document processor in one sentence.")
        print("Groq Response:\n", response.content)
    except Exception as e:
        print("Error initializing engine:", e)