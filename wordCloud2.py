import csv
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from collections import Counter

# Read the CSV file
filename = 'C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\image_data.csv'
with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)

# Extract the titles from the CSV data
titles = [row[0] for row in data]

# Combine all the titles into a single string
text = ' '.join(titles)

# Split the text into words and count their frequency
word_counts = Counter(text.split())

# Load a mask image for the word cloud
mask = Image.open("cloud.png").convert("RGBA")

# Create a new image
canvas = Image.new('RGBA', mask.size, (255, 255, 255, 0))

# Draw the words onto the image
draw = ImageDraw.Draw(canvas)
for word, count in word_counts.items():
    font_size = 16 + int(count**0.5)
    font = ImageFont.truetype("arial.ttf", font_size)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.text((random.randint(0, mask.size[0]), random.randint(0, mask.size[1])),
              word, font=font, fill=color)

# Apply the mask to the word cloud image
canvas = Image.alpha_composite(canvas, mask)

# Display the word cloud
plt.imshow(canvas)
plt.axis('off')
plt.show()
