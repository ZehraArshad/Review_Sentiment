import pandas as pd
from textblob import TextBlob

def analyze_sentiment(df: pd.DataFrame)-> pd.DataFrame:
    review_columns = [col for col in df.columns if col.startswith("Review")]

    def get_sentiment(text):
        if pd.isna(text):
            return "neutral"
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            return "positive"
        elif polarity< - 0.1:
            return "negative"
        else:
            return "neutral"
    
    rows = []
    for _, row in df.iterrows():
        product_title = row['Product Title']
        rating = row['Rating']
        for col in review_columns:
            review = row[col]
            if pd.notna(review):
                sentiment= get_sentiment(review)
                rows.append({
                    "Product Title":product_title,
                    "Rating": rating,
                    "Review": review,
                    "Sentiment": sentiment
                    })
    flattened_df= pd.DataFrame(rows)
    return flattened_df
            


