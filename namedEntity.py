import spacy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the spaCy model
nlp = spacy.load("de_core_news_sm")

# Read the CSV file
df = pd.read_csv("C:/Users/ASUS/OneDrive/Desktop/articleInfo/image_data.csv", encoding="utf8")

# Perform named entity recognition on the "image_titels" column
entities = []
for text in df["image_titels"].astype(str):
    doc = nlp(text)
    for ent in doc.ents:
        entities.append(ent.text)

# Get the top 10 entities
top_entities = pd.Series(entities).value_counts().nlargest(10)

# Create a bar chart of the top 10 entities
fig, ax = plt.subplots()
ax.bar(top_entities.index, top_entities.values)
ax.set_xlabel("Entities")
ax.set_ylabel("Frequency")
ax.set_title("Top 10 Entities in Image Titles")

# Rotate the x-axis labels
plt.xticks(rotation=45, ha="right")

# Adjust the y-axis to show only whole numbers
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# Save the chart as a PNG file
plt.savefig("C:/Users/ASUS/OneDrive/Desktop/articleInfo/entity_chart.png", bbox_inches="tight")
