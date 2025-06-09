from fastapi import FastAPI
from fastapi.responses import JSONResponse
import scrap 
import sentiment
from sheet import save_to_sheet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# scraping was happening but there was a problem in fetching data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, GET, etc.
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def home():
    return {"message": "Welcome to Daraz Review Sentiment API"}

@app.post("/scrape")
def process_scrape_and_sentiment():
    # Step 1: Scrape data
    df_scraped = scrap.get_scraped_data()
    print('scrap done')

    # Step 2: Analyze sentiment
    df_result = sentiment.analyze_sentiment(df_scraped)
    print("sentiment analysis done")

    # Step 3: Save to Google Sheets
    save_to_sheet(df_result, sheet_name="daraz_sentiments")
    print("Saved to Google Sheets")

    # Step 4: Convert to list of dicts for JSON output
    # these are titles at the frontend
    df_result.rename(columns={
    "Product Title": "product",
    "Rating": "rating",
    "Review": "review",
    "Sentiment": "sentiment"
}, inplace=True)

    result_json = df_result.to_dict(orient="records")

    return JSONResponse(content=result_json)
