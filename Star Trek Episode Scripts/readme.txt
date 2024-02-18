# Star Trek Script Downloader

This Python script downloads Star Trek episode scripts from the [Chakoteya](http://www.chakoteya.net/) website.

## Supported Series

The script supports the following series and movies:

- The Original Series (TOS)
- The Next Generation (TNG)
- Deep Space Nine (DS9)
- Voyager (VOY)
- Enterprise (ENT)
- Movies (MOV)

## Usage

To use the script, you need to provide a comma-separated list of series abbreviations and the directory where you want to save the scripts. Here's an example:

```bash
python script_downloader.py 'TOS,TNG,DS9,VOY,ENT,MOV' '/path/to/output/directory'
```

This will download the scripts for all the specified series and save them in the provided directory.

## Requirements

The script requires the following Python libraries:

- os
- time
- argparse
- requests
- BeautifulSoup from bs4
- urljoin from urllib.parse

You can install these libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Note

The script sleeps for 1 second between requests to rate limit the requests and avoid getting blocked by the server.
```
