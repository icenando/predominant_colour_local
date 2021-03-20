#! python3
# getty_predominant_colour.py - averages the colour of each thumbnail in https://www.gettyimages.co.uk/editorial-images
# regularly, and uses it to compose a graphical representation of it.

import requests, os
from bs4 import BeautifulSoup as bs

getty_ed_url = "https://www.gettyimages.co.uk/editorial-images"
target_class = "editorial-landing__img"

os.makedirs("getty_thumb", exist_ok = True)   # One thumbnail at any one time in this directory for processing.
res = requests.get(getty_ed_url)
res.raise_for_status()

soup = bs(res.text, 'html.parser')

# find thumbnails
thumbs = soup.find_all(class_=target_class)
print(thumbs[0])

# TODO: find thumbnail links
source = thumbs[0].find_all('src')
print(source)

# TODO: download each thumbnail
# TODO: open each thumbnail as array
# TODO: divide array by 255
# TODO: average each channel, store it in linked list

