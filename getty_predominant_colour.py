#! python3
# getty_predominant_colour.py - averages the colour of each thumbnail in https://www.gettyimages.co.uk/editorial-images
# regularly, and uses it to compose a graphical representation of it.

import requests
import csv
import os
from bs4 import BeautifulSoup as bs
from PIL import Image
from numpy import asarray, mean
from datetime import datetime


def img_to_array(thumb_file_path):
    img = Image.open(thumb_file_path)
    img_array = asarray(img)
    img_array = img_array.astype(float)
    return img_array


def channel_avg(array):
    array = mean(array, axis=(0, 1))
    return array


def img_avg(array):
    for image in range(len(array[0])):
        array[3].append(int((array[0][image] + array[1][image] + array[2][image]) // 3))
    return array


def get_date_time():
    return (datetime.today()).strftime('%Y-%m-%d'), (datetime.today().strftime('%H:%M:%S'))


def save_to_csv(filepath, collated_avg):
    with open(filepath, "a") as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow('')
        wr.writerow(get_date_time())
        for channel, values in zip([['R'], ['G'], ['B'], ['AVG']], collated_avg):
            wr.writerow(channel + values + [sum(values) / len(values)])
        print("Saved!")
    pass


def save_thumbnail(filepath, res):
    image_file = open(filepath, 'wb')
    for chunk in res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()


def main():
    getty_ed_url = "https://www.gettyimages.co.uk/editorial-images"
    target_class = "editorial-landing__img"
    thumb_file = "getty_thumb/getty_thumb.jpg"
    averages_file = "getty_averages/getty_averages.csv"

    res = requests.get(getty_ed_url)
    res.raise_for_status()
    soup = bs(res.text, 'html.parser')

    thumbs = soup.find_all(class_=target_class)  # find all thumbnails of target_class
    collated_avg = [[] * len(thumbs) for _ in range(4)]  # num of images times 3 channels (RGB) + AVG row

    for image in range(len(thumbs)):
        thumb_source = thumbs[image]['src']  # find thumbnail links
        res = requests.get(thumb_source)  # download thumbnail
        res.raise_for_status()

        # Save thumbnail
        save_thumbnail(thumb_file, res)

        # open thumbnail as array
        img_array = img_to_array(thumb_file)

        # average each channel, store it in list
        avg_per_channel = channel_avg(img_array)

        # each average inside list
        for channel, value in enumerate(avg_per_channel):
            collated_avg[channel].append(value)

    # compute resulting colour from avg per image
    collated_avg = img_avg(collated_avg)

    # save to file
    save_to_csv(averages_file, collated_avg)

    # delete thumbnail
    os.remove(thumb_file)


if __name__ == "__main__":
    main()