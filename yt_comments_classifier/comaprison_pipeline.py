import os
import sys
import pandas as pd

# Add root directory to system path to import shared modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from yt_comments_scrapper import get_and_clean_data
from rhetoric_classifier import classify_text
from compare_graphs import generate_comparison_graphs

def run_comparison_pipeline():
    # Fetch, classify, merge comments, and generate rhetorical network graphs 
    print("COMPARE DISCOURSES")
    
    url_1 = input("Provide 1st YT video ID (the part after 'v=' in the URL): ").strip()
    url_2 = input("Provide 2nd YT video ID (the part after 'v=' in the URL): ").strip()
    
    # Process first video
    print(f"\nClassifying 1st video: {url_1}")
    df_1 = get_and_clean_data(url_1)
    df_1 = classify_text(df_1)
    df_1['source_video'] = 'Video_1' 
    
    # Process second video
    print(f"\nClassifying 2nd video: {url_2}")
    df_2 = get_and_clean_data(url_2)
    df_2 = classify_text(df_2)
    df_2['source_video'] = 'Video_2' 
    
    # Merge datasets
    df_comparison = pd.concat([df_1, df_2], ignore_index=True)
    
    output_file = "YT_comparison.xlsx"
    df_comparison.to_excel(output_file, index=False)
    
    print(f"\nData saved to: {output_file}")
    print(f"Video 1: {len(df_1)} comments | Video 2: {len(df_2)} comments")
    
    # Trigger graph generation automatically
    print("\nGenerating comparative network graphs...")
    generate_comparison_graphs(data_file=output_file)

if __name__ == "__main__":
    run_comparison_pipeline()