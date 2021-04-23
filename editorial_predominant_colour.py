#! python3
# editorial_predominant_colour.py - averages RGB colours of all given thumbnail CSS class in given URL.

import requests
import csv
import os.path
from io import BytesIO
from bs4 import BeautifulSoup as bs
from PIL import Image
from numpy import asarray, mean
from datetime import datetime
import time


def img_to_array(thumb_file):
    img_array = asarray(thumb_file)
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


def check_folder(path):
    if os.path.exists('/'.join(path.split('/')[0:-1])):
        pass
    else:
        os.makedirs('/'.join(path.split('/')[0:-1]))


def save_to_csv(filepath, collated_avg):
    check_folder(filepath)
    with open(filepath, "a") as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow('')
        wr.writerow(get_date_time())
        for channel, values in zip([['R'], ['G'], ['B'], ['AVG']], collated_avg):
            wr.writerow(channel + values + [sum(values) / len(values)])
        print("Saved!")
    pass


def process_pipeline(thumbs, collated_avg):
    start = time.perf_counter()

    for image in range(len(thumbs)):
        res = get_url_info(thumbs[image]['src'])  # retrieves thumbnail pixel info

        img_array = img_to_array(Image.open(BytesIO(res.content)))  # converts thumbnail pixel info to array

        avg_per_channel = channel_avg(img_array)   # average each channel, store it in list

        for channel, value in enumerate(avg_per_channel):   # each average inside list
            collated_avg[channel].append(value)

    end = time.perf_counter()
    print(f'Synchronous processing took {str(end-start)} second(s).') 
    return collated_avg


def get_url_info(target_url):
    response = requests.get(target_url)
    response.raise_for_status()
    return response


def main(ed_url, target_class):
    averages_file = url.split('//')[1] + "/averages.csv"

    res = get_url_info(ed_url)
    soup = bs(res.text, 'html.parser')

    thumbs = soup.find_all(class_=target_class)
    collated_avg = [[] * len(thumbs) for _ in range(4)]  # num of images times 3 channels (RGB) + AVG row

    collated_avg = process_pipeline(thumbs, collated_avg)

    collated_avg = img_avg(collated_avg)  # compute resulting colour from avg per image

    save_to_csv(averages_file, collated_avg)  # save to file


if __name__ == "__main__":
    url = "https://www.gettyimages.co.uk/editorial-images"
    css_class = "editorial-landing__img"
    main(url, css_class)