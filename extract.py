import os
import time
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon', quiet=True)

# Configure a Session object for connection pooling
session = requests.Session()

def scrape_url(url_id, url):
    try:
        response = session.get(url, timeout=(10, 30))  # setting connect and read timeout
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article_text = ' '.join(p.get_text() for p in soup.find_all('p'))
            return url_id, article_text
        else:
            print(f"Failed to retrieve {url}")
            return url_id, None
    except Exception as e:
        print(f"Exception for {url}: {e}")
        return url_id, None

def analyze_text(text):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)['compound']

# Process the URLs in parallel and then write results at once
def process_urls(df, save_path):
    articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scrape_url, row['URL_ID'], row['URL']): row for _, row in df.iterrows()}
        for future in concurrent.futures.as_completed(future_to_url):
            url_id, article_text = future.result()
            if article_text:
                sentiment_score = analyze_text(article_text)
                articles.append((url_id, article_text, sentiment_score))
    
    # Write the results after all threads are done to minimize disk I/O time
    for url_id, article_text, sentiment_score in articles:
        file_path = os.path.join(save_path, f"{url_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(article_text)
            f.write(f"\nSentiment Score: {sentiment_score}")

# Load the URLs from an Excel file
df = pd.read_excel('D:/PROJECTS/BlackCoffer_Assignment/Input.xlsx')

# Specify the directory where text files will be saved
save_path = 'D:/PROJECTS/BlackCoffer_Assignment/text_files'
os.makedirs(save_path, exist_ok=True)

# Start the processing
start_time = time.time()
process_urls(df, save_path)
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
