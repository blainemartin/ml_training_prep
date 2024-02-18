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

        # Check if output directory exists, create it if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Send a GET request to the base URL
        response = requests.get(base_url)

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links in the table
        links = soup.select('td[valign="top"] a[href]')

        for link in links:
            try:
                episode_url = urljoin(base_url, link['href'])
                episode_name = link.text

                # Load the episode page
                response = requests.get(episode_url)

                # If the GET request is successful, the status code will be 200
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract the script
                    script = soup.select_one('td[align="left"]').text

                    # Write the script to a file
                    with open(os.path.join(output_dir, f'{series.upper()} - {episode_name}.txt'), 'w') as f:
                        f.write(script)
                else:
                    print(f"Failed to retrieve page: {episode_url}")

                # Sleep for 1 second to rate limit the requests
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Star Trek episode scripts.')
    parser.add_argument('series', type=str, help='Comma-separated list of series abbreviations.')
    parser.add_argument('output_dir', type=str, help='The directory where the scripts will be saved.')

    args = parser.parse_args()
    series_list = args.series.split(',')

    scrape_episode_scripts(series_list, args.output_dir)
