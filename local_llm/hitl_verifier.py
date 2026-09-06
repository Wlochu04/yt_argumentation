def run_hitl_verification(df):
    # Human-in-the-Loop verification loop for comment categorization 
    df['human_verified'] = ""
    category_map = {"s": "substantive", "e": "emotional", "o": "offtopic"}

    for index, row in df.iterrows():
        print(f"Text: {row['text']}")
        print(f"LLM prediction: {row['llm_prediction']}")

        while True:
            print("Verify prediction (s - substantive, e - emotional, o - offtopic) or press Enter if correct:")
            human_answer = input().strip().lower()
            
            if human_answer == "":
                df.at[index, 'human_verified'] = row['llm_prediction']
                break 
                
            elif human_answer in category_map:
                df.at[index, 'human_verified'] = category_map[human_answer]
                break 
                
            else:
                print("Error, choose between (s/e/o) or press Enter if correct")
                    
    return df