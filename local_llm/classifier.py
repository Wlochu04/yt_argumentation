import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

def classify_text(text):
    # Classify a comment into basic categories or flag for human verification 
    prompt = f"""
    You are a research assistant. Classify the given political comment into one of the following categories:
    1. 'substantive' 
    2. 'emotional' 
    3. 'offtopic' 

    RULE: If the comment is highly sarcastic, ambiguous, or if you are NOT 100% SURE about its intent, you must return the word: 'unsure'.
    Respond ONLY with one of these 4 words. Do not add any punctuation.
    
    Comment: "{text}"
    Reply ONLY with the category word in lowercase.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="qwen/qwen3.8-27b",
            temperature=0.0
        )
        # Strip whitespaces and enforce lowercase to match validation logic
        return response.choices[0].message.content.strip().lower()
    
    except Exception as e:
        return "error"