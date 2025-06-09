import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_scraped_data():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Optional: run without opening window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q=headphones")
    time.sleep(5)

    products = driver.find_elements(By.CLASS_NAME, "RfADt")
    scraped_data = []

    for i, product in enumerate(products[:10], 1):  # Limit to 10 for speed
        try:
            title_element = product.find_element(By.TAG_NAME, "a")
            title = title_element.get_attribute("title")
            link = title_element.get_attribute("href")

            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(4)

            for scroll in range(3):
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.content"))
                )
            except:
                print(f"⚠️ Reviews not found for: {title}")

            try:
                rating_element = driver.find_element(By.CSS_SELECTOR, "span.score-average")
                rating = rating_element.text.strip()
            except:
                rating = "N/A"

            review_elements = driver.find_elements(By.CSS_SELECTOR, "div.item-content:not(.item-content--seller-reply) div.content")
            review_texts = []

            for r in review_elements:
                text = r.text.strip()
                if text and "Seller Response" not in text and text not in review_texts:
                    review_texts.append(text)
                if len(review_texts) == 5:
                    break

            review_texts += [""] * (5 - len(review_texts))
            scraped_data.append([title, rating] + review_texts)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"{i}. Error: {e}")
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    # input("Press Enter to close the browser...")

    driver.quit()

    # Convert to DataFrame
    df = pd.DataFrame(scraped_data, columns=["Product Title", "Rating", "Review 1", "Review 2", "Review 3", "Review 4", "Review 5"])
    # print(df.head(10))
    return df
