import os
import re
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import json

PATH = "C:\Program Files\chromedriver.exe"
url = 'https://pr0gramm.com/new/!%20meme' 
DEFAULT_WAIT_TIME = 2

def element_has_class(driver, locator, class_name):
    element = driver.find_element(*locator)
    if class_name in element.get_attribute("class"):
        return element
    else:
        return False   

def get_html_from_links(driver):
    # Open the CSV file and read the links
    with open('F:\\nlp\\urls_pr0gramm.csv', 'r') as f:
        reader = csv.reader(f)
        links = [row[0] for row in reader]

    j = 0
    file_num = 1
    image_num = 1
    image_dir = 'F:\\nlp\\daten\\bilder'
    times_continued = 0

    for i in range(0, len(links), 100):
        batch = links[i:i+100]

        # Create an empty list to store the HTML code blocks for this batch
        html_blocks = []

        # Iterate through the links in this batch and retrieve the HTML from each link
        k = 0
        for link in batch:
            start_index = link.find('/new/') + 5
            print(link)
            id = link[start_index:]
            html = None
            while True:
                try:
                    driver.get(link)
                    time.sleep(0.5)
                    html = driver.page_source
                    break  # Break out of the while loop if the `driver.get()` method is successful
                except Exception as e:
                    print(f"Error occurred while retrieving link {link}: {str(e)}")
                    driver.refresh() # Refresh the page to try again
                    time.sleep(0.5)

            try_count = 0  # initialize the try_count to 0
            response = None
            while try_count < 3:  # try to download the image up to 3 times
                try:
                     # Parse the HTML and extract the image URL
                    soup = BeautifulSoup(html, 'html.parser')
                    image_elem = soup.find('img', {'class': 'item-image-actual'})
                    if image_elem is None:
                        break
                    image_url = image_elem['src']
                    image_name = f'{image_num}_{id}.jpg'
                    image_path = os.path.join(image_dir, image_name)
                    # Download the image and save it to disk
                    response = requests.get('https:' + image_url)
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    html_blocks.append(html)
                    break  # exit the while loop if the image is downloaded successfully
                except Exception as e:
                    print(f"Error downloading image: {e}")
                    try_count += 1  # increment the try_count if an exception occurs
            if response is None:
                times_continued += 1
                print('times continued: ' + str(times_continued))
            else:
                print('image_num: ' + str(image_num))
                image_num += 1
                j += 1
                print('json global number(j): ' + str(j))
                k += 1
                print('batch number(k): ' + str(k))
     
        # Create a new JSON file for this batch
        filename = f'F:\\nlp\\daten\\test\\pr0grammJson{file_num}.json'
        print('file_num: ' + str(file_num))
        file_num += 1
        print('html_blocks length: ' + str(len(html_blocks)))
        # Convert each HTML block to a JSON-encoded string and write to the new file
        with open(filename, 'w') as f:
            json_blocks = [json.dumps(block) for block in html_blocks]
            json.dump(json_blocks, f, indent=4)

opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

get_html_from_links(driver)

# Close the webdriver
driver.quit()


