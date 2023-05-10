import pandas as pd
from langdetect import detect

input_csv_path = 'path'
output_csv_path = 'path'


df = pd.read_csv(input_csv_path).copy()
df.loc[:, 'lang'] = "no_lang"   

for index, row in df.iterrows():
    print('The current index is: ' + str(index))
    meme_text = row['meme_text']
    try:
        language = detect(meme_text)
        df.loc[index, 'lang'] = language
    except:
        print(f"Could not detect language for row {index}")

df.to_csv(output_csv_path, encoding='utf-8', index=False)