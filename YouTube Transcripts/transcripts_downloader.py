import os
import sys
import subprocess
import webvtt
from collections import OrderedDict

def download_subtitles(playlist_url, output_dir):
    command = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-format', 'vtt',
        '--output', f'{output_dir}/%(title)s.%(ext)s',
        playlist_url
    ]
    subprocess.run(command, check=True)

def convert_vtt_to_txt(output_dir):
    for filename in os.listdir(output_dir):
        if filename.endswith(".vtt"):
            vtt = webvtt.read(os.path.join(output_dir, filename))
            text = ' '.join([caption.text for caption in vtt])
            text = ' '.join(OrderedDict((w,w) for w in text.split()).keys())
            with open(os.path.join(output_dir, filename.replace('.vtt', '.txt')), 'w') as f:
                f.write(text)

def main():
    playlist_url = sys.argv[1]
    output_dir = sys.argv[2]

    download_subtitles(playlist_url, output_dir)
    convert_vtt_to_txt(output_dir)

if __name__ == "__main__":
    main()
