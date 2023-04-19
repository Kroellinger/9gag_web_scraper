import json
from bs4 import BeautifulSoup
import sys
import csv

sys.stdout.reconfigure(encoding='utf-8')

def save_to_csv(source, author, tags, date, upvotes, downvotes):
    headers = ["img_src", "author", "meme_tags", "meme_date", "meme_upvotes", "meme_downvotes"]
    data = zip(source, author, tags, date, upvotes, downvotes)
    with open(r'C:\Users\ASUS\OneDrive\Desktop\articleInfo\pr0grammMetaData.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)


def getMetaData(soup):

    # Get source
    img_element = soup.find('img', {'class': 'item-image-actual'})
    img_src = img_element.get('src')

    # Get tags
    meme_tags_html = soup.find_all('a', {'class': 'tag-link'})
    meme_tags = []
    for tag in meme_tags_html:
        meme_tags.append(tag.text)     

    # Get time
    item_details = soup.find(class_='item-details')
    time_element = item_details.find('a', class_='time')
    meme_date = time_element.get('title')

    # Get author
    a_author = soup.find('a', class_='user')
    author = a_author.text

    # Get upvotes and downvotes
    item_vote_div = soup.find('div', class_='item-vote')
    score_span = item_vote_div.find('span', class_='score')
    score_contents = score_span.get('title')
    upvote_string, downvote_string = score_contents.split(', ')
    meme_upvote = int(''.join(filter(str.isdigit, upvote_string)))
    meme_downvote = int(''.join(filter(str.isdigit, downvote_string)))

    return img_src, author, meme_tags, meme_date, meme_upvote, meme_downvote

import json

# Open the JSON file
with open('C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\pr0grammJson2.json', 'r') as f:
    # Attempt to load the JSON data
    try:
        data = json.load(f)
    # If there's a problem with the JSON data, skip over the problematic data
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        # Move the file pointer back to the beginning of the file
        f.seek(0)
        # Initialize an empty list to store the valid JSON objects
        valid_data = []
        # Iterate through the file line by line
        for line in f:
            # Attempt to load each line as a JSON object
            try:
                obj = json.loads(line)
                valid_data.append(obj)
            # If there's a problem with a line, skip over it and continue processing
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON line: {e}")
        # Set the data variable to the list of valid JSON objects
        data = valid_data
    


# Data Lists
memes_source = []
memes_tags = []
memes_date = []
memes_author = []
memes_upvotes = []
memes_downvotes = []

# Process each HTML block
for html in data:
    block = json.loads(html)

    soup = BeautifulSoup(block, 'html.parser')
    img_element = soup.find('img', {'class': 'item-image-actual'})

    if img_element:
        img_src, author, meme_tags, meme_date, meme_upvote, meme_downvote = getMetaData(soup)

        memes_source.append(img_src)
        memes_author.append(author)
        memes_tags.append(meme_tags)
        memes_date.append(meme_date)
        memes_upvotes.append(meme_upvote)
        memes_downvotes.append(meme_downvote)

        print(img_src)
        print(author)
        print(meme_tags)
        print(meme_date)
        print(meme_upvote)
        print(meme_downvote)

    # Do something with the metadata, such as storing it in a database or writing it to a file

save_to_csv(memes_source, memes_author, memes_tags, memes_date, memes_upvotes, memes_downvotes)
