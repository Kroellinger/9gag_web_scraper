import pandas as pd
import spacy
from wordcloud import WordCloud
import pandas as pd

df = pd.read_csv('C:/Users/ASUS/OneDrive/Dokumente/Studium/NLP/pr0gramm_data.csv').copy()   

nlp = spacy.load('de_core_web_sm')
nlp.max_length = 10000000
# Load the CSV file into a Pandas dataframe

# Fill the missing values in the 'de_ocr_meme_text' column with an empty string
df['en_ocr_meme_text'] = df['en_ocr_meme_text'].fillna('')

# Preprocess text in 'de_ocr_meme_text' column
preprocessed_text = ''
for index, text in enumerate(df['en_ocr_meme_text']):
    print(index)
    if df.at[index, 'en_ocr_lang'] == 'en':
        doc = nlp(text)
        for token in doc:
            if not token.is_stop and token.is_alpha and len(token.text) > 1:
                tokenLemma = token.lemma_ + ' '
                preprocessed_text += tokenLemma

output_path = r'C:\Users\ASUS\OneDrive\Desktop\daten\finaleDaten\pr0gramm_data.csv'    
df.to_csv(output_path, index=False, encoding='utf-8')

# Generate word cloud
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=set()).generate(preprocessed_text)

# Save word cloud image
wordcloud.to_file('wordcloud.png')
