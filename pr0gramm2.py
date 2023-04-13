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

# Load the HTML blocks from the JSON file
with open('C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\pr0grammJson.json', 'r') as f:
    data = json.load(f)

# Data Lists
memes_source = []
memes_tags = []
memes_date = []
memes_author = []
memes_upvotes = []
memes_downvotes = []

# Process each HTML block
for html in data:
    soup = BeautifulSoup(html, 'html.parser')
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
