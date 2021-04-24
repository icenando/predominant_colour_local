# Editorial Images Predominant Colour

predominant_colour_local.py scans a given URL for thumbnails matching a user-specified CSS class, calculates the average pixel value for each RGB value of each thumbnail in that class, and saves the results  for each image in a CSV file in a folder with the name of the website in the current working directory. Only the average colour values are saved, not the thumbnails.

The "_local" in the name specifies that the CSV file will be created locally. I have adapted the code to run on AWS Lambda in another version, so that it can potentially run automatically in regular intervals.

It uses multithreading to boost speeds. In my local machine, the programme ran in around 7 secs using a synchronous approach, and in around 1.5 secs using an asynchronous approach.

## Motivation
Sentiment analysis is widely used in data sciences. Averaging predominant colours of newsworthy images being licensed 
on a specific date and time can potentially be used to evaluate media influence on widespread sentiment.

## Usage
The code takes two variables: the URL and the CSS class. Supplied with the code as an example is Getty Images editorial page's URL and CSS class for the thumbnails.

```python
if __name__ == "__main__":
    # Replace url and css_class to the target url and css class
    url = "https://www.gettyimages.co.uk/editorial-images"
    css_class = "editorial-landing__img"
    main(url, css_class)
```

## Output file
A CSV file named "averages.csv" will be saved in the following format:
 <table style="width:100%">
  <tr>
    <td>yyyy-mm-dd</td>
    <td>hh:mm:ss</td>
    <td></td>
    <td>...</td>
  </tr>
  <tr>
    <td>R</td>
    <td>red channel average for image 1</td>
    <td>red channel average for image 2</td>
    <td>...</td>
  </tr>
  <tr>
    <td>G</td>
    <td>green channel average for image 1</td>
    <td>green channel average for image 2</td>
    <td>...</td>
  </tr>
  <tr>
    <td>B</td>
    <td>blue channel average for image 1</td>
    <td>blue channel average for image 2</td>
    <td>...</td>
  </tr>
  <tr>
    <td>AVG</td>
    <td>average pixel colour value for image 1</td> 
    <td>average pixel colour value for image 2</td>
    <td>...</td>
  </tr>
</table> 


## Output location
Creates a folder (if it doesn't already exist) with the website address, and subfolder for subdomains. For instance, if the URL is https://www.homepage.com/editorial-images-page, the folder structure will be "www.homepage.com/editorial-images-page".

The CSV file will be saved inside this folder.

## Limitations
TODO: The CSV file folder path is specific for Macs and might not work on PCs.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)