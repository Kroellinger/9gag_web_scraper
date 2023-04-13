import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("C:/Users/ASUS/OneDrive/Desktop/articleInfo/image_data.csv", encoding="utf8")

# Join all the image titles into one string
text = " ".join(df["image_titels"].astype(str))

# Generate the word cloud
wordcloud = WordCloud(width=800, height=800, background_color="white").generate(text)

# Display the generated image:
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 
