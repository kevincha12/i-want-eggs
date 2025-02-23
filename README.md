# i-want-eggs
A basic egg price detector for the cheapest eggs in Virginia relative to gas prices.

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