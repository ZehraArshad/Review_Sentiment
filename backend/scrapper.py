from scrap import get_scraped_data
from sentiment import analyze_sentiment

df = get_scraped_data()
sentiment_df = analyze_sentiment(df)

print(sentiment_df.head())
# Optional: sentiment_df.to_excel("sentiment_output.xlsx", index=False)
