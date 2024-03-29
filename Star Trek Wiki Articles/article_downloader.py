import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import argparse
import glob
from urllib.parse import urljoin

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

def download_article(series, wiki, output_dir, counter):
    base_url = URLS[wiki][series]
    print(f'Downloading URL: {base_url}')
    response = requests.get(base_url)
    print(f'Status code: {response.status_code}')
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links in the article
    for link in soup.find_all('a'):
        url = link.get('href')
        
        # Only download links to other articles
        if url and url.startswith('/wiki/'):
            article_url = urljoin(base_url, url)
            print(f'Downloading article: {article_url}')
            
            try:
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                content = article_soup.get_text()
                
                # Trim the content based on the wiki
                if wiki == 'MemAlpha':
                    start_index = content.find('View history')
                    end_index = content.find('External links')
                elif wiki == 'MemBeta':
                    start_index = content.find('View history')
                    end_index = content.find('External link')
                else:  # Wikipedia
                    start_index = content.find('From Wikipedia, the free encyclopedia')
                    end_index = content.find('Sources[edit]')
                
                if start_index != -1 and end_index != -1:
                    content = content[start_index:end_index]
                
                print(f'Content length: {len(content)}')
                
                # Use the article title as the filename
                full_title = article_soup.title.string.replace('/', '_')  # Replace / in titles to avoid file path issues
                title = full_title.split('|')[0].strip()  # Extract the article title from the full title
                filename = os.path.join(output_dir, f'{series} - {wiki} - {counter:04d} - {title}.txt')
                
                print(f'Filename: {filename}')
                
                os.makedirs(output_dir, exist_ok=True)
                with open(filename, 'w') as f:
                    f.write(content)
                print(f'Downloaded article: {title}')
                counter += 1
            except Exception as e:
                print(f'Error downloading article: {e}')
    return counter

def cleanup(output_dir, wiki, num_files_to_delete_from_start, num_files_to_delete_from_end=0):
    # Get a list of all files for the wiki
    files = sorted(glob.glob(os.path.join(output_dir, f'* - {wiki} - *.txt')))
    
    # Delete the first num_files files
    for file in files[:num_files_to_delete_from_start]:
        os.remove(file)
        print(f'Deleted file: {file}')
    
    # Delete the last num_files files
    for file in files[-num_files_to_delete_from_end:]:
        os.remove(file)
        print(f'Deleted file: {file}')

def main(series_abbreviations, wikis, output_dir):
    counters = {'MemAlpha': 1, 'MemBeta': 1, 'Wikipedia': 1}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for series in series_abbreviations.split(','):
            for wiki in wikis.split(','):
                counters[wiki] = executor.submit(download_article, series, wiki, output_dir, counters[wiki]).result()
    
    # Cleanup the first few files for each wiki
    cleanup(output_dir, 'MemAlpha', 11)
    cleanup(output_dir, 'Wikipedia', 15, 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download articles from specified wikis.')
    parser.add_argument('series_abbreviations', type=str, help='Comma-separated list of series abbreviations.')
    parser.add_argument('wikis', type=str, help='Comma-separated list of wikis.')
    parser.add_argument('output_dir', type=str, help='Path to the output directory.')
    args = parser.parse_args()
    main(args.series_abbreviations, args.wikis, args.output_dir)
