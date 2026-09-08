import os
import json
from dotenv import load_dotenv
import time
from groq import Groq

load_dotenv()

# Initialize Groq client
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

def classify_rhetoric(comment_text):
    # Analyze a single comment using an Argument Mining taxonomy
    # Returns a structured JSON response with classification and reasoning

    system_prompt = """
    You are an expert in Computational Argumentation and Argument Mining. 
    Your task is to classify the dominant argumentative strategy in a short, noisy YouTube comment.
    
    Use ONLY the following taxonomy:
    1. Rhetorical: Emotive Expression, spam, sarcasm, or pure emotional outbursts without logical claims.
    2. Policy: Claims explicitly proposing, requesting, or advocating for a specific course of action (e.g., "Ban this").
    3. Value: Subjective propositions expressing moral judgments, ethical opinions, or value-laden evaluations.
    4. Testimony: Anecdotal evidence, first-person narrative accounts, or personal lived experiences.
    5. Fact: Verifiably objective claims about reality (even if scientifically incorrect).
    
    Follow this Checklist Scaffolding:
    Step 1: Is this purely Rhetorical/sarcasm/spam? If yes, classify as Rhetorical.
    Step 2: If no, does it demand an action? If yes, classify as Policy.
    Step 3: If no, does it recount a personal lived experience? If yes, classify as Testimony.
    Step 4: If no, is it a verifiably objective assertion (Fact) or a subjective moral/ethical judgment (Value)?
    
    You must output your response in strict JSON format with the following keys:
    - "quote": The exact verbatim phrase from the comment that justifies your decision.
    - "rejected_category": Name one taxonomy category you considered but ruled out.
    - "rejection_reason": Briefly explain the logical mechanism of why you rejected it.
    - "classification": Your final chosen category (must be exactly one of: Rhetorical, Policy, Value, Testimony, Fact).
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this comment:\n\n{comment_text}"}
            ],
            model="qwen/qwen3.8-27b",
            response_format={"type": "json_object"},
            temperature=0.1 # Low temperature for more deterministic, analytical outputs
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error during API call: {e}")
        return {"classification": "Error", "quote": "", "rejected_category": "", "rejection_reason": ""}

def classify_text(df):
    # Process a DataFrame of comments, applying rhetorical classification to each row
    # Returns the updated DataFrame

    rhetoric_classes = []
    
    print("Classifying comments via Groq...")
    for comment_text in df['comment']:
        result_json = classify_rhetoric(comment_text)
        
        # Extract only the classification label for the dataframe output
        category = result_json.get("classification", "Error")
        rhetoric_classes.append(category)

        time.sleep(1)
        
    df['rhetoric_class'] = rhetoric_classes
    
    return df