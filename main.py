import pandas as pd
from data_scrapper import get_and_clean_data
from local_ai import train_local_model, prediction_confidence
from classifier import classify_text
import time

def run_pipeline():


    #master data
    master_df = pd.read_excel("YT_comm.xlsx")
    local_model, vectorizer = train_local_model(master_df)

    print(f"Current DataBase has: {len(master_df['comment'])} comments")
    
    #data scraping
    new_data_df = get_and_clean_data()

    if new_data_df.empty:
        print("New data not avaible")
        return

    #LLM classification
    print(f"Classification of {len(new_data_df)} new comments\n")

    new_verified_rows = []

    for index, row in new_data_df.iterrows():
        text = row['comment']

        local_prediction, accuracy = prediction_confidence(text, local_model, vectorizer)

        #ACCURACY
        #local model prediction >
        if accuracy >= 0.6:
            print(f"[Local Model]: High confidence {accuracy:.2f} -> {local_prediction}")
            final_prediction = local_prediction
        #GROQ LLM verification
        else:
            print(f"[Local Model]: Low confidence ({accuracy:.2f}). Redirecting to LLM")
            llm_prediction = classify_text(text)

            valid_categories = ['substantive', 'emotional', 'offtopic']

            if llm_prediction in valid_categories:
                final_prediction = llm_prediction

            #HITL verification
            else:
                if llm_prediction == "unsure":
                    print(f"[LLM]: Low confidence. Redirecting to Human ({llm_prediction}).")
                else:
                    print(f"[LLM]: Format error. Redirecting to Human ({llm_prediction}).")
                while True:
                    print(f"[Text]: {row['comment']}")

                    category_map = {"s": "substantive", "e": "emotional", "o": "offtopic"}
                    human_answer = input("Verify prediction (s - substantive, e - emotional, o - offtopic) or press Enter if correct:").strip().lower()
                                
                    if human_answer == "":
                        final_prediction = llm_prediction
                        break
                    elif human_answer in category_map:
                        final_prediction = category_map[human_answer]
                        break      
                    else:
                        print("Error, choose between (s/e/o) or press Enter if correct")
        new_verified_rows.append({
        "comment": text,
        "category": final_prediction
    })

    time.sleep(0.5)

    #Results
    print("Saving data")
    new_df = pd.DataFrame(new_verified_rows)

    updated_master_df = pd.concat([master_df, new_df], ignore_index=True)
    updated_master_df.to_excel("YT_comm.xlsx", index=False)

    print(f"Classification finished. New master Data Frame size: {len(updated_master_df)}")
    

if __name__ == "__main__":
    run_pipeline()