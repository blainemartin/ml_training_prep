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

        print(f"Processing series: {series}")

        # Check if output directory exists, create it if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Send a GET request to the base URL
        response = requests.get(base_url)

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links in the table
        links = soup.select('td a[href]')
        total_episodes = len(links)
        print(f"Total episodes to process for {series}: {total_episodes}")

        for i, link in enumerate(links, start=1):
            try:
                episode_url = urljoin(base_url, link['href'])
                episode_name = link.text

                print(f"Processing episode {i} of {total_episodes}:
