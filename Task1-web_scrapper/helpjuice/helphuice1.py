import csv
from bs4 import BeautifulSoup
import os
import requests
import pandas as pd
from datetime import datetime
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def scraper(url, start_page, end_page):
    helpjuice_dataset = []
    all_keywords = []

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
            
            # Extracting top 3 keywords from the title
            keywords = [word.lower() for word in blog_title.split() if word.lower() not in stopwords.words('english')][:3]
            all_keywords.extend(keywords)
            
            article = {
                'Title': blog_title,
                'publication_date': date_published,
                'Blog_author': author_name,
                'Keywords': ', '.join(keywords)
            }
            
            helpjuice_dataset.append(article)

    df = pd.DataFrame(helpjuice_dataset)
    df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
    
    # Creating a folder based on the URL
    folder_name = url.split('//')[1].replace('/', '_')
    os.makedirs(folder_name, exist_ok=True)

   # Saving to CSV with tab as the delimiter and specifying an escape character
    csv_filename = os.path.join(folder_name, 'helpjuice_dataset.csv')
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer.writerow(df.columns)
        for _, row in df.iterrows():
            writer.writerow(row)
            
    # Creating word clouds for every 3 months from 2021 Jan to 2023 Dec
    for year in range(2021, 2024):
        for month in range(1, 13, 3):
            subset = df[(df['publication_date'].dt.year == year) & (df['publication_date'].dt.month.between(month, month + 2))]
            if not subset.empty and 'Keywords' in subset.columns:
                generate_word_cloud(subset['Keywords'].str.cat(sep=' '), folder_name, f'wordcloud_{year}_{month}-{month + 2}.png')
            
def generate_word_cloud(text, folder_name, filename):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    wordcloud_filename = os.path.join(folder_name, filename)
    plt.savefig(wordcloud_filename)
    plt.show()


# Example usage:
url = "https://helpjuice.com/blog"
start_page = 1
end_page = 26
scraper(url, start_page, end_page)
