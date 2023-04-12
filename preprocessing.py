import csv
import spacy

# Load the spaCy model
nlp = spacy.load("de_core_news_sm")

# Define a function to preprocess the text
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower().strip() for token in doc if not token.is_stop and not token.is_punct and not token.is_digit]
    return ' '.join(tokens)

# Open the CSV file and iterate through the rows
with open('test.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    print(csv_reader.fieldnames)
    for row in csv_reader:
        # Preprocess the text in the desired column
        preprocessed_text = preprocess_text(row["\ufeffFisch"])
        # Do something with the preprocessed text, for example write it to a new CSV file
        with open('preprocessed_file.csv', mode='a', encoding='utf-8') as output_file:
            fieldnames = ['Text']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writerow({'Text': preprocessed_text})