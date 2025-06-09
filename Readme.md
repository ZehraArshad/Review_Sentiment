## Daraz Product Reviews Sentiment Analysis

### Project Goal

- Building a pipeline that scrapes reviews from an e-commerce site and performs sentiment analysis on those reviews.

---

### How to Run?

#### Divide the terminal into two:

##### 1st terminal
- cd backend  
- uvicorn main:app --reload

##### 2nd terminal 
- cd frontend  
- cd daraz-review_dashboard  
- npm run dev

---

### Backend

#### Scraper (scrapper.py)

- **Tools**: Selenium  
- Scraped 50 products, their average ratings, and customer reviews.  
- To automate, I extracted the href of each product using the common class `'RfADt'`.  
- On each product page, I grabbed:
  - the average rating using its class,
  - and reviews using the div class `'item-content'`.
- Scraped 5 reviews per product.  
- Returned the data as a DataFrame.

#### Sentiment Analysis (sentiment.py)

- **Library**: TextBlob  
- Based on polarity, I labeled each review as:
  - `'positive'`, `'negative'`, or `'neutral'`.  
- Returned the data as a DataFrame.

#### scrapper.py

- A test script to check `scrapper.py` and `sentiment.py` before integration.

#### Integration using Google Sheets API

- Created a project on Google Cloud Console.  
- Enabled **Google Sheets API** and **Drive API**.  
- Created a **service account**.  
- Generated a **JSON key**.  
- Downloaded and renamed it to `credentials.json`.  
- Shared an empty Google Sheet with the email from the `credentials.json` file.

#### FASTAPI Backend

- Created a POST endpoint (`/scrape`) to trigger scraping when a button is clicked from the frontend.

---

### Frontend

- Created a Next.js app using the following configuration:

![alt text](<nextjs_setting.png>)

#### page.js

- This is the main frontend page from which the `/scrape` endpoint is triggered.
- The returned data is displayed in a table on the same page.


![alt text](<chart.png>)

![alt text](<table.png>)