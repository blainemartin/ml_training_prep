import os
import argparse
import subprocess
from collections import OrderedDict
import re

def download_subtitles(playlist_url, output_dir):
    # Download subtitles using yt-dlp
    command = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-format', 'vtt',
        '--sub-lang', 'en',
        '-o', os.path.join(output_dir, '%(title)s.%(ext)s'),
        playlist_url
    ]
    subprocess.run(command)

def clean_subtitles(output_dir):
    for filename in os.listdir(output_dir):
        if filename.endswith(".vtt"):
            with open(os.path.join(output_dir, filename), 'r') as file:
                lines = file.readlines()

            # Remove timestamps, metadata, and other formatting
            cleaned_lines = [re.sub('<.*?>', '', line) for line in lines if not line.startswith(('WEBVTT', 'Kind:', 'Language:', '00:', '<c>'))]

            # Remove duplicate or overlapping text
            cleaned_lines = list(OrderedDict.fromkeys(cleaned_lines))

            # Write cleaned subtitles to txt file
            with open(os.path.join(output_dir, filename.replace('.vtt', '.txt')), 'w') as file:
                file.writelines(cleaned_lines)

def main():
    parser = argparse.ArgumentParser(description='Download and clean YouTube playlist subtitles.')
    parser.add_argument('playlist_url', help='YouTube playlist URL')
    parser.add_argument('output_dir', help='Output directory for subtitle files')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    download_subtitles(args.playlist_url, args.output_dir)
    clean_subtitles(args.output_dir)

if __name__ == "__main__":
    main()
