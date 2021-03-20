#! python3
# getty_predominant_colour.py - averages the colour of each thumbnail in https://www.gettyimages.co.uk/editorial-images
# regularly, and uses it to compose a graphical representation of it.

import requests, os
from bs4 import BeautifulSoup as bs
from PIL import Image
from numpy import asarray, mean

def div_mult_by_255(array, key):
    if key=="div":
        return array/255
    elif key=='mult':
        return array*255

def img_to_array():
    img = Image.open("getty_thumb/saved_thumb.jpg")
    img_array = asarray(img)
    img_array = img_array.astype(float)
    img_array = div_mult_by_255(img_array, 'div')
    return img_array

def compute_avg(array):
    array = mean(array, axis=(0,1))
    return array

def main():
    getty_ed_url = "https://www.gettyimages.co.uk/editorial-images"
    target_class = "editorial-landing__img"
    dir_name = "getty_thumb"
    current_thumb = "saved_thumb.jpg"
    os.makedirs(dir_name, exist_ok = True)   # One thumbnail at any one time in this directory for processing.

    res = requests.get(getty_ed_url)
    res.raise_for_status()
    soup = bs(res.text, 'html.parser')

    thumbs = soup.find_all(class_=target_class)  # find all thumbnails of target_class

    #for i in range(len(thumbs)):
    thumb_source = thumbs[9]['src']  # find thumbnail links
    res = requests.get(thumb_source)  # download thumbnail
    res.raise_for_status()
    # Save thumbnail
    image_file = open(dir_name+"/"+current_thumb, 'wb')
    for chunk in res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()
    # open each thumbnail as array
    img_array = img_to_array()

    # average each channel, store it in linked list
    avg_per_channel=compute_avg(img_array)

    # compute array back to 256 colours
    avg_per_channel=div_mult_by_255(avg_per_channel, 'mult')
    print(avg_per_channel)

if __name__=="__main__":
    main()