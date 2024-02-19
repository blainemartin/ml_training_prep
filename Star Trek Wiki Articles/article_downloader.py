import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import argparse

# Define the URLs for each series/wiki combination
URLS = {
    'MemAlpha': {
        'TOS': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_The_Original_Series',
        'TNG': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_The_Next_Generation',
        'VOY': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_Voyager',
        'DS9': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_Deep_Space_Nine',
        'ENT': 'https://memory-alpha.fandom.com/wiki/Star_Trek:_Enterprise'
    },
    'MemBeta': {
        'TOS': 'https://memory-beta.fandom.com/wiki/Star_Trek:_The_Original_Series',
        'TNG': 'https://memory-beta.fandom.com/wiki/Star_Trek:_The_Next_Generation',
        'VOY': 'https://memory-beta.fandom.com/wiki/Star_Trek:_Deep_Space_Nine',
        'DS9': 'https://memory-beta.fandom.com/wiki/Star_Trek:_Deep_Space_Nine',
        'ENT': 'https://memory-beta.fandom.com/wiki/Star_Trek:_Enterprise'
    },
    'Wikipedia': {
        'TOS': 'https://en.wikipedia.org/wiki/Star_Trek:_The_Original_Series',
        'TNG': 'https://en.wikipedia.org/wiki/Star_Trek:_The_Next_Generation',
        'VOY': 'https://en.wikipedia.org/wiki/Star_Trek:_Voyager',
        'DS9': 'https://en.wikipedia.org/wiki/Star_Trek:_Deep_Space_Nine',
        'ENT': 'https://en.wikipedia.org/wiki/Star_Trek:_Enterprise'
    }
}

def download_article(series, wiki, output_dir):
    url = URLS[wiki][series]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text()
    filename = os.path.join(output_dir, f'{series} - {wiki} - {soup.title.string}.txt')
    with open(filename, 'w') as f:
        f.write(content)
    print(f'Downloaded article: {soup.title.string}')

def main(series_abbreviations, wikis, output_dir):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for series in series_abbreviations.split(','):
            for wiki in wikis.split(','):
                executor.submit(download_article, series, wiki, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download articles from specified wikis.')
    parser.add_argument('series_abbreviations', type=str, help='Comma-separated list of series abbreviations.')
    parser.add_argument('wikis', type=str, help='Comma-separated list of wikis.')
    parser.add_argument('output_dir', type=str, help='Path to the output directory.')
    args = parser.parse_args()
    main(args.series_abbreviations, args.wikis, args.output_dir)