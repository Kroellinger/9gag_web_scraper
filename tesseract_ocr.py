import os
import json
import pytesseract
from PIL import Image, UnidentifiedImageError
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
# Set the path to the images directory
images_path = "C:/Users/ASUS/OneDrive/Desktop/daten/bilder"
output_dir = "C:/Users/ASUS/OneDrive/Desktop/daten/ocr_daten4"
# Set the path to the Tesseract installation directory
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Initialize an empty list to store the data
data = []
isError = False
# Loop through all the image files in the directory
numberOfErrors = 0
runNum = 0
batch_size = 1000  # Set the batch size
batch_num = 1  # Initialize the batch number
for filename in os.listdir(images_path):
    runNum += 1
    if filename.endswith('.jpg'):
        # Extract the id from the filename
        id = filename.split('_')[1].split('.')[0]
        count_in_image_list = filename.split('_')[0]
        # Open the image file
        try:
            image = Image.open(os.path.join(images_path, filename))
        except UnidentifiedImageError as e:
            numberOfErrors += 1
            print("An exception occurred while opening file", filename, ":", e)
            isError = True

        if isError:
            data.append({"count_in_image_list": count_in_image_list, "runNum": runNum, "id": id, "text": ""})
        else:
            try:
                # Extract the text from the image
                text = pytesseract.image_to_string(image, lang='deu')

                # Remove special characters, commas, and newlines
                text = re.sub(r'[^\w\s]', '', text)
                text = re.sub(r',', '', text)
                text = re.sub(r'\n', ' ', text)
                text = re.sub(r"\s+", " ", text)
            except Exception as e:
                numberOfErrors += 1
                print("An exception occurred while processing file", filename, ":", e)
                # handle the exception here as appropriate for your use case

            # Append the id and text as a dictionary to the data list
            data.append({"count_in_image_list": count_in_image_list, "runNum": runNum, "id": id, "text": text})

        isError = False
        # Check if the batch size has been reached and write the data to a JSON file
        if len(data) >= batch_size:
            # Write the data to a JSON file with a name based on the batch number
            filename = f"{output_dir}/output_batch{batch_num}.json"
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)

            # Reset the data list and increment the batch number
            data = []
            batch_num += 1

# Check if there is remaining data and write it to a JSON file
if len(data) > 0:
    # Write the data to a JSON file with a name based on the batch number
    filename = f"{output_dir}/output_batch{batch_num}.json"
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)
