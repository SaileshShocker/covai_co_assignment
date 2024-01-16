import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def scraper(url, start_page, end_page):
    helpjuice_dataset = []

    for x in range(start_page, end_page + 1):
        current_url = f"{url}?page={x}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        r = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")

        articles = soup.find_all("a", class_='post')
        for item in articles:
            blog_title = ' '.join(item.find('h2', class_='post-title').stripped_strings)
            author_info = item.find('div', class_='author-info')
            author_name = author_info.find('strong').text
            date_published = author_info.find('span').text
            
            article = {
                'Title': blog_title,
                'publication_date': date_published,
                'Blog_author': author_name
            }
            
            helpjuice_dataset.append(article)

    df = pd.DataFrame(helpjuice_dataset)
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')

    # Saving to CSV with tab as the delimiter and specifying an escape character
    with open('helpjuice_dataset.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer.writerow(df.columns)
        for _, row in df.iterrows():
            writer.writerow(row)

# Example usage:
url = "https://helpjuice.com/blog"
start_page = 1
end_page = 26
scraper(url, start_page, end_page)
