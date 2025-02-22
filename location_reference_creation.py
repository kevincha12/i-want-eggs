import kaggle
import pandas as pd

def load_walmart_csvs():
    kaggle.api.dataset_download_files('timmofeyy/-walmart-stores-location', path='./data', unzip=True)
    walmart_store_location = pd.read_csv('./data/walmart_store_locaction.csv')
    virginia_only = walmart_store_location[walmart_store_location['State'] == 'VA']
    return virginia_only

def load_target_csvs():
    kaggle.api.dataset_download_files('locationscloudsdata/target-store-location-data-usa', path='./data', unzip=True)
    target_store_location = pd.read_csv('./data/target_store_locaction.csv')
    virginia_only = target_store_location[target_store_location['Address.FormattedAddress'].str.contains(', VA ')]    
    return virginia_only