import os
import time
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SERIES_URLS = {
    'TNG': 'http://www.chakoteya.net/NextGen/episodes.htm',
    'DS9': 'http://www.chakoteya.net/DS9/episodes.htm',
    'TOS': 'http://www.chakoteya.net/StarTrek/episodes.htm',
    'VOY': 'http://www.chakoteya.net/Voyager/episode_listing.htm',
    'ENT': 'http://www.chakoteya.net/Enterprise/episodes.htm',
    'MOV': 'http://www.chakoteya.net/movies/index.htm',
}

def scrape_episode_scripts(series_list, output_dir):
    for series in series_list:
        base_url = SERIES_URLS.get(series.upper())
        if not base_url:
            print(f"Unknown series abbreviation: {series}")
            continue

        # Rest of your code here...

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Star Trek episode scripts.')
    parser.add_argument('series', type=str, help='Comma-separated list of series abbreviations.')
    parser.add_argument('output_dir', type=str, help='The directory where the scripts will be saved.')

    args = parser.parse_args()
    series_list = args.series.split(',')

    scrape_episode_scripts(series_list, args.output_dir)
