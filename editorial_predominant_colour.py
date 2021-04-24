#! python3
# editorial_predominant_colour.py - averages RGB colours of all
# given thumbnail CSS class in given URL.

import requests
import csv
import os.path
from io import BytesIO
from bs4 import BeautifulSoup as bs
from PIL import Image
from numpy import asarray, mean
from datetime import datetime
import time
import concurrent.futures


class thumb_obj:
    def __init__(self, thumbs):
        self.thumb = thumbs
        # num of images times 3 channels (RGB) + 'average' row
        self.collated_avg = [[] * len(thumbs) for _ in range(4)]


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
    joined_path = os.path.join(*[parts for parts in os.path.split('/')[0:-1]])
    if os.path.exists(joined_path):
        pass
    else:
        os.makedirs(joined_path)


def save_to_csv(filepath, collated_avg):
    check_folder(filepath)
    with open(filepath, "a") as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow('')
        wr.writerow(get_date_time())
        for channel, values in zip([
                                ['R'], ['G'], ['B'], ['AVG']
                                ], collated_avg):
            wr.writerow(channel + values + [sum(values) / len(values)])
        print("Saved!")
    pass


def get_url_info(target_url):
    response = requests.get(target_url)
    response.raise_for_status()
    return response


def process_pipeline(thumb):
    # retrieves thumbnail pixel info
    res = get_url_info(thumb['src'])

    # converts thumbnail pixel info to array
    img_array = img_to_array(Image.open(BytesIO(res.content)))

    # average each channel, store it in list
    avg_per_channel = channel_avg(img_array)

    # each average inside list
    for channel, value in enumerate(avg_per_channel):
        thumbs.collated_avg[channel].append(value)


def main(ed_url, target_class, enable_multithread):
    start = time.perf_counter()  # just to check performance
    averages_file = ed_url.split('//')[1] + "/averages.csv"

    res = get_url_info(ed_url)
    soup = bs(res.text, 'html.parser')

    global thumbs
    thumbs = thumb_obj(soup.find_all(class_=target_class))

    if enable_multithread:  
    # faster, but saves results in the same order as 
    # the threads finish processing them.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_pipeline, thumbs.thumb)
    else:
    # slower, but results are saved in the  same order 
    # in which they appear on the webpage.
        for thumb in thumbs.thumb:
            process_pipeline(thumb)

    # compute resulting colour from avg per image
    thumbs.collated_avg = img_avg(thumbs.collated_avg)

    save_to_csv(averages_file, thumbs.collated_avg)

    end = time.perf_counter()  # just to check performance
    print(f'Processing took {str(end-start)} second(s).')


if __name__ == "__main__":
    url = "https://www.gettyimages.co.uk/editorial-images"
    css_class = "editorial-landing__img"
    enable_multithread = True
    main(url, css_class, enable_multithread)
