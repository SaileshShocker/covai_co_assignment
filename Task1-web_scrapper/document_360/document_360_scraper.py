import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd


document_360_dataset = []
for x in range(1,61):
    url = "https://document360.com/blog/page/"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    r = requests.get(url+str(x), headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    articles = soup.find_all("aside",class_='col-md-6 col-lg-4 mb-4')
    # print(articles)
    for item in articles:
        Blog_title = ' '.join(item.find('h5', 'pb-2').stripped_strings)
        date_and_name = item.find_all('p','text-xs')[1].text
        
        # Spliting the combined string into date and name
        publication_date, Blog_author = map(str.strip, date_and_name.split('•'))
        
        # print("Title:", Blog_title)
        # print("Date:", publication_date)
        # print("Name:", Blog_author)
        # print("\n")
        
        article = {
            'Title':Blog_title,
            'publication_date':publication_date,
            'Blog_author':Blog_author
                
            
        }
        document_360_dataset.append(article)
        
df = pd.DataFrame(document_360_dataset)
df['publication_date'] = pd.to_datetime(df['publication_date'], errors='coerce')

# print(df.head())

# Saving to CSV with tab as the delimiter and specifying an escape character
with open('document_360_dataset.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t', escapechar='\\', quoting=csv.QUOTE_NONE)
    writer.writerow(df.columns)
    for _, row in df.iterrows():
        writer.writerow(row)