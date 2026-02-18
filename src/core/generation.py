import ollama
from typing import List
from src.config import get_settings

settings = get_settings()

def generate_answer(query: str, context: List[str], use_local: bool = True) -> dict:
    """
    Generates an answer based on the query and context.
    Returns the answer and inference metadata.
    """
    context_str = "\n\n".join(context)
    
    prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the following context. If the answer is not in the context, say "I don't know based on the provided documents."
    
    Context:
    {context_str}
    
    Question:
    {query}
    """
    
    if use_local:
        try:
            # Using Ollama
            # Make sure OLLAMA_HOST is set if running in Docker/remote
            # The python ollama library reads OLLAMA_HOST env var, 
            # but we can also configure client if needed. 
            # For now, we rely on environment/default.
            
            # Explicitly set host if provided in settings, though library does check env
            client = ollama.Client(host=settings.OLLAMA_BASE_URL)
            
            response = client.chat(model=settings.LLM_MODEL_NAME, messages=[
                {'role': 'user', 'content': prompt},
            ])
            
            return {
                "answer": response['message']['content'],
                "model": settings.LLM_MODEL_NAME,
                "provider": "ollama"
            }
        except Exception as e:
            return {
                "answer": f"Error generating response with Ollama: {str(e)}",
                "model": settings.LLM_MODEL_NAME,
                "provider": "ollama_error"
            }
    else:
        # Fallback to OpenAI (if key provided)
        if not settings.OPENAI_API_KEY:
            return {
                "answer": "OpenAI API key not configured.",
                "model": "none",
                "provider": "openai_error"
            }
        
        try:
            import openai
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "answer": completion.choices[0].message.content,
                "model": "gpt-3.5-turbo",
                "provider": "openai"
            }
        except Exception as e:
             return {
                "answer": f"Error generating response with OpenAI: {str(e)}",
                "model": "gpt-3.5-turbo",
                "provider": "openai_error"
            }
