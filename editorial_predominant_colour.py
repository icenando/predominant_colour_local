#! python3
# editorial_predominant_colour.py - averages RGB colours 
# of all given thumbnail CSS class in given URL.

import csv
import os.path
from io import BytesIO
from bs4 import BeautifulSoup as bs
from PIL import Image
from numpy import asarray, mean
from datetime import datetime
import time

import asyncio
import httpx



def img_avg(array):
    for image in range(len(array[0])):
        array[3].append(int((array[0][image] + \
            array[1][image] + array[2][image]) // 3))
    return array


def get_date_time():
    return (datetime.today()).strftime('%Y-%m-%d'), \
            (datetime.today().strftime('%H:%M:%S'))


def check_folder(path):
    joined_path = os.path.join(
        *[parts for parts in os.path.split('/')[0:-1]]
    )
    if os.path.exists(joined_path):
        pass
    else:
        os.makedirs(joined_path)
    return None


def save_to_csv(filepath, collated_avg):
    
    check_folder(filepath)

    with open(filepath, "a") as output:
        wr = csv.writer(output, dialect='excel')
        wr.writerow('')
        wr.writerow(get_date_time())

        for channel, values in zip([
                ['R'], ['G'], ['B'], ['AVG']
                ], collated_avg):
            wr.writerow(
                channel + values + [sum(values) / len(values)]
            )
        print("Saved!")
    pass


async def get_url_info(target_url):
    async with httpx.AsyncClient() as client:
        res = await client.get(target_url)
    return res


async def process_pipeline(thumb, collated_avg):
    # retrieves thumbnail pixel info
    res = await get_url_info(thumb['src'])

    # converts thumbnail pixel info to numpy array
    with BytesIO(res.content) as content:
        with Image.open(content) as img:
            img_array = asarray(img, dtype=float)

    # average each channel: averages RGB channels 
    # for each row (axis=0) x column (axis=1) "sheet"
    avg_per_channel = mean(img_array, axis=(0, 1))

    # each average inside list
    for channel, value in enumerate(avg_per_channel):
        collated_avg[channel].append(value)


async def main(ed_url, target_class):
    start = time.perf_counter()  # just to check performance
    averages_file = ed_url.split('//')[1] + "/averages.csv"

    res = await get_url_info(ed_url)

    soup = bs(res.text, 'html.parser')

    thumbs = soup.find_all(class_=target_class)

    # num of images * 3 channels + 'average' row
    collated_avg = [[] * len(thumbs) for _ in range(4)]

    tasks = asyncio.gather(
                *[process_pipeline(thumb, collated_avg) for thumb in thumbs]
            )
    await tasks

    # compute resulting colour from avg per image
    collated_avg = img_avg(collated_avg)

    save_to_csv(averages_file, collated_avg)

    # just to check speed
    end = time.perf_counter()
    print(f'Processing took {(end-start):.2f} second(s).')


if __name__ == "__main__":
    url = "https://www.gettyimages.co.uk/editorial-images"
    css_class = "editorial-landing__img"
    asyncio.run(main(url, css_class))
