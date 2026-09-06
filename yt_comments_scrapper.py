import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

def get_and_clean_data(video_id=None): 
    # Fetch top comments for a given YouTube video
    
    YT_API_KEY = os.getenv("YT_API_KEY")

    if not video_id:
        video_id = input("Provide YT video ID (the part after 'v=' in the URL): ").strip()

    print(f"Downloading comments for video ID: {video_id}...")

    extracted_comments = []
    video_title = "Unknown Video"
    
    try:
        # Initialize API client
        youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

        # Fetch video metadata (title)
        vid_request = youtube.videos().list(part="snippet", id=video_id)
        vid_response = vid_request.execute()
        
        if vid_response.get('items'):
            video_title = vid_response['items'][0]['snippet']['title']

        # Fetch top level comments (sorted by relevance)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=10,
            order="relevance"
        )
        response = request.execute()

        for item in response.get('items', []): 
            comment_snippet = item['snippet']['topLevelComment']['snippet']
            extracted_comments.append({
                "comment": comment_snippet['textOriginal'],
                "likes": comment_snippet['likeCount']
            })
            
        df = pd.DataFrame(extracted_comments)

    except Exception as e:
        print(f"YouTube API connection error: {e}")
        # Fallback empty dataframe structure must match the expected output
        df = pd.DataFrame(columns=["comment", "likes"])

    # Data cleaning: Drop comments shorter than 10 characters
    if not df.empty:
        initial_count = len(df)
        df_clean = df[df['comment'].astype(str).str.len() > 10].copy()
        print(f"Downloaded {initial_count} comments. Retained {len(df_clean)} after cleaning.")
    else:
        df_clean = df.copy()
        print("No comments retrieved.")

    # Append video title for comparison grouping
    df_clean['video_title'] = video_title

    return df_clean