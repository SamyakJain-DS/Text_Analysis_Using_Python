from newspaper import Article
import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
from nltk.corpus import cmudict

# Downloading all the necessary resources.
nltk.download('cmudict')
nltk.download('punkt_tab')
d = cmudict.dict()
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Cleaning dataset for extraction purpose.
urls = pd.read_excel('Input.xlsx').dropna(how='all')
urls= urls.iloc[:,[0,1]]
 
extracted_texts = dict()

def extract_text(url):
# This extracts article title and content from a url.
    # Might throw network or server errors.
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title + '\n' + article.text
    
    except Exception as e:   
        return {"error": str(e)}

# Iterating over the urls dataset.
for index,row in urls.iterrows():  

    url_id = row['URL_ID']
    url = row['URL']
    file_name = f"ArticlesTextFiles/{url_id}.txt"
    
    # Creates a seperate text file for each URL in a seperate folder.
    if not os.path.exists(file_name):  
           with open(file_name, "w",encoding='utf-8') as f:
               try:
                   f.write(extract_text(url))
               except:
                   print(f'Encountered an error,\n {extract_text(url)}')