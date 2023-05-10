from matplotlib import pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import collections
from tabulate import tabulate

# Load the CSV file into a Pandas dataframe
input_csv_path = 'path'
df = pd.read_csv(input_csv_path).copy()

# Combine all the tags into a single string
# Iterate over the dataframe rows and apply the explode() method to the 'meme_tags' column of each row
tags_list = [tag for row in df['meme_tags'] for tag in eval(row)]
tags_list_lower = [s.lower() for s in tags_list]

len_df = len(df)
print('len df: '+ str(len_df))
tag_counts = collections.Counter(tags_list_lower)
top_20_tags = tag_counts.most_common(20)

tag_percentages = [(tag, str(round(count/len_df*100, 2)) + '%') for tag, count in top_20_tags]
print(tag_percentages)

df = pd.DataFrame(tag_percentages, columns=['Tag', 'Frequency'])
print(df)

table = tabulate(tag_percentages, headers=['Tags', 'Frequency'], tablefmt='latex')
print(table)
