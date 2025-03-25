import pandas as pd
import re
import os
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

print("✅ Script started...")

# Ensure language detection is consistent
DetectorFactory.seed = 0

# File Paths
input_file = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_comments.csv"
output_file = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_comments_cleaned_translated.csv"

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
    text = re.sub(r"@\w+|\#", "", text)  # Remove mentions and hashtags
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters and punctuation
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

# ✅ Step 4: Function to Detect Language and Translate
def detect_and_translate(text):
    try:
        lang = detect(text)  # Detect language
        if lang != "en":  # If not English, translate
            text = GoogleTranslator(source=lang, target="en").translate(text)
        return text
    except:
        return text  # Return original text if detection fails

# ✅ Step 5: Apply Cleaning Function
df["Cleaned_Comments"] = df["Comments"].apply(clean_text)

# ✅ Step 6: Apply Language Detection & Translation
df["Translated_Comments"] = df["Cleaned_Comments"].apply(detect_and_translate)

# ✅ Step 7: Save Cleaned and Translated Comments to a New CSV File
df.to_csv(output_file, index=False)

print(f"✅ {len(df)} Comments cleaned, translated, and saved successfully!")
print(f"📂 Output file saved at: {output_file}")
