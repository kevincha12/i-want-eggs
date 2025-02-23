# i-want-eggs
A basic egg price detector for the cheapest eggs in Virginia relative to gas prices.

## How it works
We used a Kaggle dataset for target and walmart locations. This part can be done with the google maps API, but due to time constraints a dataset was used to get location data. Then, we scrape using playwright to deal with dynamic loading, along with IP proxies from Oxylabs to get nearby grocery data. We spoof the geolocation of different walmarts and targets to get the egg prices from there. Then, using the google maps API, we calculate distance and calculate the cheapest eggs based on price + gas prices!

## Setup

To get started using this codebase yourself, you'll need a couple things:

1. A kaggle API key + properly setup .kaggle folder with the kaggle.json
2. A google maps API key to allow distance calculations
3. IP proxy credentials - Oxylabs was used but any is fine
4. A PostgreSQL database - this must be setup prior to any data persistence

The latter three of these need their credentials filled in a .env file that is of the following format:

> ROUTE_API_KEY = ''  
> PROXY_USERNAME = ''  
> PROXY_PASSWORD = ''  
> PROXY_SERVER = ''  
> DB_NAME = ''  
> DB_USER = ''  
> DB_PW = ''  

Likewise, a requirements.txt has been included, and can be run with:
```sh
python -m pip install -r requirements.txt
```
and you'll also need playwright's headless chromium browser for the scraping portion:
```sh
python -m playwright install chromium
```

And that should be enough to run all the files!

## Contact Us
This project was completed for WICS hack downtown 2025 by co-authors Andy Zeng and Kevin Cha. If you are curious about the design choices or further expansion of this project, please contact us at xxd8nb@virginia.edu or hpb2gv@virginia.edu respectively.

## Issues
Due to time constraints, there were a couple of shortcuts made for this project:

1. Instead of being able to request API keys for multiple retailers, we didn't have time for approvals so we stuck to scraping walmart + target.
2. Target is slow to dynamically load their products via javascript, so while the functionality is semi-in place to scrape + handle target elements it could not be completed in the time constraints of the hackathon.