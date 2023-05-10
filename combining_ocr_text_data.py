import os
import json
import pandas as pd

# Load the CSV file into a DataFrame and create a copy
input_csv = 'path'
output_csv = 'path'

df = pd.read_csv(input_csv).copy()
print('Number of rows df: ' + str(len(df)))
df.loc[:, 'meme_text'] = "default_text"   
df.loc[:, 'meme_id'] = "default_id" 

# Loop through each JSON file in the directory
json_dir = r'C:\Users\ASUS\OneDrive\Desktop\daten\ocr_daten4'
json_count = 0  # Initialize the counter variable
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_file = os.path.join(json_dir, filename)
        
        # Load the JSON file into a dictionary
        with open(json_file) as f:
            entries = json.load(f)
            
        # Loop through each entry in the "data" list
        for entry in entries:            
            count_in_image_list = entry['count_in_image_list']
            text = entry['text']
            meme_id = entry['id']
            
            # Find the corresponding row in the DataFrame
            row_idx = int(count_in_image_list) - 1
            print('Number of rows df: ' + str(len(df)))
            row = df.loc[row_idx]
            
            # Update the "meme_text" column with the "text" value
            row['meme_text'] = text
            row['meme_id'] = str(meme_id)
            df.loc[row_idx] = row
            print('row_idx '+ str(row_idx))
            print('meme_text: ' + text)
            print('ROW_meme_text: ' + str(row['meme_text']))

# Save the updated DataFrame to a new CSV file
df.to_csv(output_csv, encoding='utf-8')