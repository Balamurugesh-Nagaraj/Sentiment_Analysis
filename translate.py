import pandas as pd
import re

# Load the uploaded CSV file
file_path = "youtube_comments_cleaned_translated.csv"
df = pd.read_csv(file_path)

# Function to clean text further (removing @ and other special characters)
def final_clean_text(text):
    text = str(text)  # Ensure text is a string
    text = re.sub(r"@\w+", "", text)  # Remove @mentions
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters except space
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

# Apply cleaning function to the translated comments
df["Fully_Cleaned_Comments"] = df["Translated_Comments"].apply(final_clean_text)

# Save the fully cleaned file
cleaned_file_path = "youtube_comments_fully_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

# Show the first few cleaned comments
df.head()
import pandas as pd
import re
import os
import time
import emoji
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
from tqdm import tqdm  # For progress bar

print("✅ Script started...")

# Ensure language detection is consistent
DetectorFactory.seed = 0

# File Paths
input_file = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_comments.csv"
output_file = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_comments_fully_cleaned.csv"

# ✅ Step 1: Check if the Input File Exists
if not os.path.exists(input_file):
    print("❌ ERROR: File not found! Check the file path.")
    exit()
else:
    print("✅ Input file found!")

# ✅ Step 2: Load YouTube Comments CSV File
df = pd.read_csv(input_file)

if df.empty:
    print("❌ ERROR: The CSV file is empty!")
    exit()
else:
    print(f"✅ Loaded {len(df)} comments from CSV.")

# ✅ Step 3: Function to Clean Text
def clean_text(text):
    text = str(text)  # Ensure text format
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove @mentions
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters and punctuation
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    text = emoji.replace_emoji(text, replace="")  # Remove emojis
    return text

# ✅ Step 4: Function to Detect Language and Translate (Optimized)
def detect_and_translate(text):
    try:
        lang = detect(text)  # Detect language
        if lang == "en":
            return text  # Skip translation if it's already English
        
        # Add delay to prevent hitting API rate limits
        time.sleep(0.2)  

        # Translate non-English text
        translated_text = GoogleTranslator(source=lang, target="en").translate(text)
        return translated_text
    except:
        return text  # Return original text if detection fails

# ✅ Step 5: Apply Cleaning Function
df["Cleaned_Comments"] = df["Comments"].apply(clean_text)

# ✅ Step 6: Apply Language Detection & Translation with Progress Bar
df["Translated_Comments"] = [detect_and_translate(comment) for comment in tqdm(df["Cleaned_Comments"], desc="🔄 Translating")]

# ✅ Step 7: Save Cleaned and Translated Comments to a New CSV File
df.to_csv(output_file, index=False)

print(f"✅ {len(df)} Comments fully cleaned, translated, and saved successfully!")
print(f"📂 Output file saved at: {output_file}")
