This script scrapes http://www.chakoteya.net/NextGen/episodes.htm, then parses all of the script pages listed in the index to individual txt files in a configurable output directory.

This script includes a 1-second delay between requests to the server, which should prevent the script from overloading the server. It also includes basic error handling: if an error occurs while processing an episode (for example, if the page fails to load), the script will print an error message and continue with the next episode.

You can specify the output directory as a command line argument when you run the script:
ex. python episodedownload.py /path/to/output/dir

Replace /path/to/output/dir with the path to the directory where you want to save the scripts.

Please note that web scraping should be done responsibly. Make sure to check the website’s robots.txt file and terms of service to ensure that you’re allowed to scrape it.
