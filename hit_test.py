import pandas as pd

#training data
df = pd.DataFrame({
    'text': ["Great problem analysis", "He's such a moron 🤡", "Buy my crypto"],
    'llm_prediction': ["substantive", "substantive", "offtopic"]
})

#bucket for human verdict and categories
df['human_verified'] = ""

category_map = {
    "s": "substantive",
    "e": "emotional",
    "o": "offtopic"
    }

#human verification
print("Verification...")

for index, row in df.iterrows():
    print(f"Tekst: {row['text']}")
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

print("\nVerified DataBase")
print(df[['text', 'llm_prediction', 'human_verified']])