import os
import time
import requests
from bs4 import BeautifulSoup

def scrape_episode_scripts(base_url, output_dir):
    # Send a GET request to the base URL
    response = requests.get(base_url)
    
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links in the table
    links = soup.select('td[valign="top"] a[href]')

    for link in links:
        try:
            episode_url = os.path.join(base_url, link['href'])
            episode_name = link.text

            # Load the episode page
            response = requests.get(episode_url)
            
            # If the GET request is successful, the status code will be 200
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the script
                script = soup.select_one('td[align="left"]').text

                # Write the script to a file
                with open(os.path.join(output_dir, f'{episode_name}.txt'), 'w') as f:
                    f.write(script)
            else:
                print(f"Failed to retrieve page: {episode_url}")
            
            # Sleep for 1 second to rate limit the requests
            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")

# Usage
scrape_episode_scripts('http://www.chakoteya.net/NextGen/', '/path/to/output/dir')
