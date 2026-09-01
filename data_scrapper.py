import pandas as pd
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

#scraping comments from reddit post
def get_and_clean_data():

    #source data
    YT_API_KEY = os.getenv("YT_API_KEY")

    VIDEO_ID = input("Provide YT video ID for new comments: ")

    print("Downloading comments")

    #bucket for comments
    extracted_comments = []
    
    try:
        youtube = build('youtube', 'v3', developerKey = YT_API_KEY)
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = VIDEO_ID,
            maxResults = 50,
            order = "relevance"
        )
        response = request.execute()

        #iterating through comments
        for item in response['items']: 
            comment = item['snippet']['topLevelComment']['snippet']
            extracted_comments.append({
                "comment": comment['textOriginal'],
                "likes": comment['likeCount']
            })
        #creating a dataframe
        df = pd.DataFrame(extracted_comments)

    #in case of error
    except Exception as e:
        print(f"Błąd przy łączeniu z YT: {e}")
        df = pd.DataFrame(columns=["author", "comment", "score"])

    #counting data
    print(f"Downloaded {len(df)} comments")
    df_clean = df[df['comment'].str.len() > 10].copy()

    #deleting short comments
    if not df.empty:
        df_clean = df[df['comment'].str.len() > 10].copy()
    else:
        df_clean = df.copy()
        
    return df_clean