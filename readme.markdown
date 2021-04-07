# Editorial Images Predominant Colour

predominant_colour_local.py scans a given URL for thumbnails
matching a user-specified CSS class, calculates the average pixel value
for each RGB value of each thumbnail in that class, and saves the results 
for each image in a CSV file in a folder with the name of the website in 
the current working directory. Only the average colour values are saved, 
not the thumbnails.

The "_local" in the name specifies that the CSV file will be created
locally. I have adapted the code to run on AWS Lambda in another version,
so that it can potentially run automatically in regular intervals.

## Motivation
Sentiment analysis is widely used in data sciences. 
Averaging predominant colours of newsworthy images being licensed 
on a specific date and time can potentially be used to evaluate 
media influence on widespread sentiment.

## Usage
The code takes two variables: the URL and the CSS class. Supplied with
the code as an example is Getty Images editorial page's URL and CSS class
for the thumbnails.

```python
if __name__ == "__main__":
    # Replace url and css_class to the target url and css class
    url = "https://www.gettyimages.co.uk/editorial-images"
    css_class = "editorial-landing__img"
    main(url, css_class)
```

## Limitations
The CSV file folder path is specific for Macs and might not work on 
PCs.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)