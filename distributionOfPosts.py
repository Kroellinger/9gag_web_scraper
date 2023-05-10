import pandas as pd
import matplotlib.pyplot as plt

input_csv = 'path'
# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv)

# Calculate the total number of posts
total_posts = len(df)

# Calculate the number of posts made by each author
author_counts = df['author'].value_counts()

# Calculate the cumulative sum of the number of posts made by each author, sorted in descending order
cumulative_counts = author_counts.sort_values(ascending=False).cumsum()

# Calculate the percentage of posts made by each author
cumulative_percentages = cumulative_counts / total_posts * 100

# Plot the cumulative distribution of posts by author
fig = plt.figure(figsize=(10, 5))
plt.plot(cumulative_percentages.values)
plt.xticks(rotation=90)
plt.xlabel('Authors')
plt.ylabel('% of posts')
plt.title('Cumulative distribution of posts by author')
plt.show()
