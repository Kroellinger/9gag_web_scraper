import cv2
import pytesseract
import os
import csv

# Set the path to the folder containing the images
folder_path = r"C:\Users\ASUS\Desktopd\9gag_images"

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open the existing CSV file for reading and create a new CSV file for writing
with open("C:/Users/ASUS/OneDrive/Desktop/articleInfo/image_data.csv", "r", newline="") as input_file, \
        open("C:/Users/ASUS/OneDrive/Desktop/articleInfo/image_data_with_text.csv", "w", newline="") as output_file:

    # Create CSV reader and writer objects
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Read the header row from the input file and add a new "image_text" column header to the output file
    header_row = next(reader)
    header_row.append("image_text")
    writer.writerow(header_row)

    # Loop over each row in the input file (excluding the header row)
    for row in reader:
        # Extract the filename from the "image_source" column
        filename = os.path.basename(row[2])

        # Check if the file is an image (i.e. has a .jpg extension)
        if filename.endswith(".jpg"):
            # Read the image using OpenCV
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)

            # Perform OCR using Tesseract
            result = pytesseract.image_to_string(img)

            # Append the OCR result to the current row and write it to the output file
            row.append(result)
            writer.writerow(row)