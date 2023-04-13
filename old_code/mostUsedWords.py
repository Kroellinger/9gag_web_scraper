import pandas as pd
import spacy
from collections import Counter
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\image_data.csv")

# Combine all titles into a single string
titles = ' '.join(df['image_titels'].astype(str).tolist())

# Preprocess the data
titles = titles.lower()
titles = ''.join([c for c in titles if c.isalpha() or c.isspace()])

# Filter out stop words using spaCy
nlp = spacy.load("de_core_news_sm")
doc = nlp(titles)
filtered_titles = ' '.join([token.text for token in doc if not token.is_stop])

# Count the frequency of each word
word_counts = Counter(filtered_titles.split())

# Plot the most frequent words
most_common_words = word_counts.most_common(10) # Change 10 to number of words you want to plot
words, counts = zip(*most_common_words)
plt.bar(words, counts)
plt.xticks(rotation=45)  # Rotate x-tick labels by 45 degrees
plt.title("Most Common Words in Image Titles")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.gcf().subplots_adjust(bottom=0.2)
plt.show()
