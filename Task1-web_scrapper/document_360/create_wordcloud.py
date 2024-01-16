
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Load the dataset
df = pd.read_csv('document_360_dataset.csv', sep='\t')

# Function to extract keywords
def extract_keywords(title):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(title)
    keywords = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return keywords

# Extract top 3 keywords from each title
df['Keywords'] = df['Title'].apply(extract_keywords)
df['Top_3_Keywords'] = df['Keywords'].apply(lambda x: ', '.join(x[:3]))

# Create a folder based on the CSV file
csv_folder = 'document_360_dataset_wordclouds'
os.makedirs(csv_folder, exist_ok=True)

# Create word cloud for each 3-month period
start_date = '2021-01-01'
end_date = '2023-12-31'
date_range = pd.date_range(start=start_date, end=end_date, freq='3M')

for i in range(len(date_range) - 1):
    start_period = date_range[i].strftime('%Y-%m-%d')
    end_period = date_range[i+1].strftime('%Y-%m-%d')
    
    # Filter data for the current 3-month period
    period_data = df[(df['publication_date'] >= start_period) & (df['publication_date'] < end_period)]
    
    # Concatenate all titles in the current period
    all_titles = ' '.join(period_data['Title'])
    
    # Create word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
    
     # Save word cloud image to the folder
    image_filename = f'{csv_folder}/wordcloud_{start_period}_{end_period}.png'
    wordcloud.to_file(image_filename)
    
    # Display word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud - {start_period} to {end_period}')
    plt.axis('off')
    # plt.show()

# Display changes in keywords
for i in range(len(date_range) - 1):
    start_period = date_range[i].strftime('%Y-%m-%d')
    end_period = date_range[i+1].strftime('%Y-%m-%d')
    
    # Filter data for the current 3-month period
    period_data = df[(df['publication_date'] >= start_period) & (df['publication_date'] < end_period)]
    
    # Display changes in keywords
    print(f'Keywords from {start_period} to {end_period}:\n')
    print(period_data[['Title', 'Top_3_Keywords']])
    print('-' * 50)

