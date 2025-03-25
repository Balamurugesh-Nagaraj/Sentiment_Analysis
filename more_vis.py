import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
import os

# ✅ Download stopwords if not available
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

# ✅ Load the dataset
df = pd.read_csv("youtube_sentiment_analysis.csv")

# ✅ Ensure correct column names
if "Sentiment" not in df.columns:
    df.rename(columns={col: "Sentiment" for col in df.columns if "sentiment" in col.lower()}, inplace=True)
if "Fully_Cleaned_Comments" not in df.columns:
    df.rename(columns={col: "Fully_Cleaned_Comments" for col in df.columns if "comment" in col.lower()}, inplace=True)

# ✅ Tamil Font Handling
possible_fonts = [
    r"C:\Windows\Fonts\Lohit-Tamil.ttf",   # Lohit Tamil
    r"C:\Windows\Fonts\Nirmala.ttf",       # Nirmala UI (Supports Tamil)
    r"C:\Windows\Fonts\Arial.ttf"          # Default (if Tamil fonts are missing)
]

tamil_font_path = next((font for font in possible_fonts if os.path.exists(font)), None)

if tamil_font_path:
    tamil_font = fm.FontProperties(fname=tamil_font_path)
    plt.rcParams["font.family"] = tamil_font.get_name()
    print(f"✅ Tamil font loaded: {tamil_font.get_name()}")
else:
    print("⚠️ Tamil font not found! Using default font.")

# --- 1️⃣ Sentiment Distribution ---
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="Sentiment", palette={"Positive": "red", "Negative": "blue", "Neutral": "green"})
plt.title("YouTube Comments Sentiment Distribution", fontproperties=tamil_font if tamil_font_path else None)
plt.xlabel("Sentiment", fontproperties=tamil_font if tamil_font_path else None)
plt.ylabel("Number of Comments", fontproperties=tamil_font if tamil_font_path else None)
plt.show()

# --- 2️⃣ WordCloud for Each Sentiment ---
for sentiment in ["Positive", "Negative", "Neutral"]:
    sentiment_df = df[df["Sentiment"] == sentiment]
    
    if sentiment_df.empty:
        print(f"⚠️ No comments found for sentiment: {sentiment}")
        continue
    
    words = " ".join(sentiment_df["Fully_Cleaned_Comments"].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white", 
                          stopwords=stop_words, font_path=tamil_font_path if tamil_font_path else None).generate(words)

    plt.figure(figsize=(8, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"WordCloud for {sentiment} Comments", fontproperties=tamil_font if tamil_font_path else None)
    plt.show()

# --- 3️⃣ Top 10 Most Frequent Words in Comments ---
all_words = " ".join(df["Fully_Cleaned_Comments"].astype(str))
filtered_words = [word.lower() for word in all_words.split() if word.lower() not in stop_words]
word_counts = Counter(filtered_words)

# ✅ If no words found, skip visualization
if not word_counts:
    print("⚠️ No frequent words found after filtering stopwords.")
else:
    top_words = pd.DataFrame(word_counts.most_common(10), columns=["Word", "Frequency"])

    plt.figure(figsize=(10, 5))
    sns.barplot(data=top_words, x="Frequency", y="Word", palette="viridis", dodge=False)
    plt.title("Top 10 Most Frequent Words in YouTube Comments", fontproperties=tamil_font if tamil_font_path else None)
    plt.xlabel("Frequency", fontproperties=tamil_font if tamil_font_path else None)
    plt.ylabel("Word", fontproperties=tamil_font if tamil_font_path else None)
    plt.show()
