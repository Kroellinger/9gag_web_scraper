import pandas as pd

csv_with_en_ocr = 'path'
csv_with_de_ocr = 'path'
output_csv = 'path'
df_en = pd.read_csv(csv_with_en_ocr).copy()
df_de = pd.read_csv(csv_with_de_ocr).copy()

# Select only the 'meme_text' and 'lang' columns and rename them
df_en = df_en[['meme_text', 'lang']]
df_en = df_en.rename(columns={'meme_text': 'en_ocr_meme_text', 'lang': 'en_ocr_lang'})

# Join the two dataframes on their index
df_merged = df_de.join(df_en, how='outer')

# Rename the 'lang' column to 'de_ocr_lang'
df = df_merged.rename(columns={'lang': 'de_ocr_lang'})

# Rename the 'meme_text' column to 'de_meme_text'
df = df_merged.rename(columns={'meme_text': 'de_ocr_meme_text'})

# Write the merged dataframe to a CSV file
df_merged.to_csv(output_csv, index=False)
