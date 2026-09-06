import pandas as pd

def clean_database():
    # Remove duplicate entries from the master database based on comment text 
    file_name = "YT_rethorics.xlsx"
    
    df = pd.read_excel(file_name)
    initial_count = len(df)
    print(f"Initial database size: {initial_count} comments.")

    # Drop duplicates based solely on the comment column
    df_cleaned = df.drop_duplicates(subset=['comment'], keep='first')
    
    final_count = len(df_cleaned)
    removed_count = initial_count - final_count

    print(f"Removed {removed_count} duplicates.")
    print(f"New database size: {final_count} unique comments.")

    df_cleaned.to_excel(file_name, index=False)
    print("Database cleaned and saved successfully.")

if __name__ == "__main__":
    clean_database()