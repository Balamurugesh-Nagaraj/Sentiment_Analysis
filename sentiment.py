import pandas as pd
from textblob import TextBlob

# Load the cleaned comments
file_path = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_comments_fully_cleaned.csv"
df = pd.read_csv(file_path)

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(str(text))  # Convert text to string
    polarity = analysis.sentiment.polarity  # Get polarity score
    
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
df["Sentiment"] = df["Fully_Cleaned_Comments"].apply(analyze_sentiment)

# Save the results to a new CSV
output_file = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_sentiment_analysis.csv"
df.to_csv(output_file, index=False)

print(f"✅ Sentiment Analysis Completed! Results saved at: {output_file}")
print(df["Sentiment"].value_counts())  # Show sentiment distribution
