import os
import sys
import time
import pandas as pd

# Add root directory to system path to import shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_dir, "YT_comments.xlsx")

from yt_comments_scrapper import get_and_clean_data
from local_llm.local_ai import train_local_model, prediction_confidence
from local_llm.classifier import classify_text

def run_pipeline():
    # Load dataset and train local model
    master_df = pd.read_excel(excel_path)
    local_model, vectorizer = train_local_model(master_df)

    print(f"Current database has: {len(master_df['comment'])} comments")
    
    # Fetch new comments
    new_data_df = get_and_clean_data()

    if new_data_df.empty:
        print("New data not available")
        return

    # Filter out duplicates against master dataset
    initial_new_count = len(new_data_df)
    existing_comments = master_df['comment'].tolist()
    new_data_df = new_data_df[~new_data_df['comment'].isin(existing_comments)]
    
    dropped_count = initial_new_count - len(new_data_df)
    if dropped_count > 0:
        print(f"Cleaned {dropped_count} duplicates.")

    print(f"Classifying {len(new_data_df)} new comments\n")

    results = []
    valid_categories = ['substantive', 'emotional', 'offtopic']

    # Classification workflow: Local Model -> Groq LLM -> HITL Verification
    for index, row in new_data_df.iterrows():
        text = row['comment']
        local_prediction, accuracy = prediction_confidence(text, local_model, vectorizer)

        if accuracy >= 0.6:
            print(f"[Local Model]: High confidence {accuracy:.2f} -> {local_prediction}")
            assigned_category = local_prediction
        else:
            print(f"[Local Model]: Low confidence ({accuracy:.2f}). Redirecting to LLM")
            llm_prediction = classify_text(text)

            if llm_prediction in valid_categories:
                assigned_category = llm_prediction
            else:
                print(f"[LLM]: Resolution required ({llm_prediction}). Redirecting to Human.")
                
                while True:
                    print(f"[Text]: {text}")
                    category_map = {"s": "substantive", "e": "emotional", "o": "offtopic"}
                    human_answer = input("Verify prediction (s - substantive, e - emotional, o - offtopic) or press Enter if correct: ").strip().lower()
                                
                    if human_answer == "":
                        assigned_category = llm_prediction if llm_prediction in valid_categories else "offtopic"
                        break
                    elif human_answer in category_map:
                        assigned_category = category_map[human_answer]
                        break      
                    else:
                        print("Error, choose between (s/e/o) or press Enter if correct")

        results.append({
            "comment": text,
            "category": assigned_category
        })

    time.sleep(0.5)

    # Append and save updated master dataset
    print("Saving data")
    new_df = pd.DataFrame(results)
    updated_master_df = pd.concat([master_df, new_df], ignore_index=True)
    updated_master_df.to_excel(excel_path, index=False)

    print(f"Classification finished. New master database size: {len(updated_master_df)}")

if __name__ == "__main__":
    run_pipeline()