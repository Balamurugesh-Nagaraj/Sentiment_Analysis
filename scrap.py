import pandas as pd
from googleapiclient.discovery import build

# Replace with your YouTube API Key
API_KEY = "AIzaSyDtm50WQ19o8-72mbfYaZT4dAAq3E8pbHQ"  # Replace this with your API Key
VIDEO_ID = "MDeOZdbSBCU"  # Extracted from the video URL

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Function to get all comments
def get_all_youtube_comments(video_id):
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # Max allowed per request
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # Check if there are more pages of comments
        next_page_token = response.get("nextPageToken")

        # Stop when there are no more comments to fetch
        if not next_page_token:
            break

    return comments

# Scrape all comments
comments = get_all_youtube_comments(VIDEO_ID)

# Save to CSV
df = pd.DataFrame({"Comments": comments})
df.to_csv("youtube_comments.csv", index=False)
print(f"✅ {len(comments)} Comments saved successfully!")
