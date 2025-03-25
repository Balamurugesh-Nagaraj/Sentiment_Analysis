import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the sentiment analysis results
file_path = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\youtube_sentiment_analysis.csv"
df = pd.read_csv(file_path)

# Count the number of each sentiment type
sentiment_counts = df["Sentiment"].value_counts()

# ✅ Plot the sentiment distribution
plt.figure(figsize=(8, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=["green", "red", "blue"])

# ✅ Customize the plot
plt.title("YouTube Comments Sentiment Analysis", fontsize=14)
plt.xlabel("Sentiment", fontsize=12)
plt.ylabel("Number of Comments", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# ✅ Save the graph as an image
output_image = r"C:\Users\Admin\OneDrive\Desktop\Data analyst\Sentiment Analysis\sentiment_analysis_chart.png"
plt.savefig(output_image)

# ✅ Show the graph
plt.show()

print(f"📊 Sentiment analysis visualization saved at: {output_image}")
