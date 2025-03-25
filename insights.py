import pandas as pd
from collections import Counter

# ✅ Load the dataset
df = pd.read_csv("youtube_sentiment_analysis.csv")

# ✅ Check if 'Sentiment' column exists
if "Sentiment" not in df.columns:
    df.rename(columns={col: "Sentiment" for col in df.columns if "sentiment" in col.lower()}, inplace=True)

# ✅ Check for missing values
df["Sentiment"] = df["Sentiment"].fillna("Neutral")  # Treat missing as neutral

# --- 1️⃣ Sentiment Percentage Breakdown ---
sentiment_counts = df["Sentiment"].value_counts(normalize=True) * 100
print("\n🔹 Sentiment Percentage Breakdown:")
print(sentiment_counts)

# --- 2️⃣ Most Common Words in Positive & Negative Comments ---
def get_top_words(sentiment, top_n=10):
    comments = df[df["Sentiment"] == sentiment]["Fully_Cleaned_Comments"].dropna().astype(str)
    words = " ".join(comments).split()
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

top_positive_words = get_top_words("Positive", 10)
top_negative_words = get_top_words("Negative", 10)

print("\n🔹 Top 10 Words in Positive Comments:")
for word, freq in top_positive_words:
    print(f"{word}: {freq}")

print("\n🔹 Top 10 Words in Negative Comments:")
for word, freq in top_negative_words:
    print(f"{word}: {freq}")

# --- 3️⃣ Trending Topics in Comments (Movie-Related Words) ---
trending_keywords = ["movie", "film", "actor", "scene", "story", "trailer", "music", "direction"]
trending_counts = {word: 0 for word in trending_keywords}

for comment in df["Fully_Cleaned_Comments"].dropna().astype(str):
    for word in trending_keywords:
        if word in comment.lower():
            trending_counts[word] += 1

print("\n🔹 Trending Topics in Comments:")
for topic, count in trending_counts.items():
    print(f"{topic}: {count} mentions")

print("\n✅ Insights extraction completed!")
