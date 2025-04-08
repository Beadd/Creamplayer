import os
import sys
import datetime
import argparse
import requests
import eyed3
from mutagen.flac import FLAC, Picture
from urllib.parse import unquote
import urllib.parse
import re

# Define download directory
DOWNLOAD_DIR = "downloads"

# Windows has a max path length of 260 characters
MAX_FILENAME_LENGTH = 200  # Leaving room for path and extension

# Initialize command-line argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Download and process music files")
    parser.add_argument('-s', help='Music source: netease or tencent')
    parser.add_argument('-f', help='Song file name')
    parser.add_argument('-u', help='Song download URL')
    parser.add_argument('-c', help='Song cover URL')
    parser.add_argument('-l', help='Lyrics URL')
    parser.add_argument('-i', help='Song ID')
    parser.add_argument('-t', help='Song title')
    parser.add_argument('-ar', help='Artist')
    parser.add_argument('-al', help='Album name')
    parser.add_argument('-p', help='Publish time in the format YYYY-MM-DD HH:MM:SS')
    parser.add_argument('-sl', action='store_true', help='Save lyrics to a separate file')
    return parser.parse_args()

# Get file extension from URL
def get_file_extension(url):
    return url.split('.')[-1].split('?')[0] if '.' in url else 'mp3'

# Sanitize filename by removing invalid characters
def sanitize_filename(filename):
    # Remove invalid Windows filename characters
    invalid_chars = r'[\\/*?:"<>|]'
    filename = re.sub(invalid_chars, '', filename)
    
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    return filename

# Generate a safe filename that doesn't exceed Windows limits
def generate_safe_filename(original_name, song_title, ext):
    # Sanitize both names
    sanitized_original = sanitize_filename(original_name)
    sanitized_title = sanitize_filename(song_title)
    
    # First try the sanitized original name
    test_name = f"{sanitized_original}.{ext}"
    if len(test_name) <= MAX_FILENAME_LENGTH:
        return test_name
    
    # If original is too long, try just the sanitized song title
    test_name = f"{sanitized_title}.{ext}"
    if len(test_name) <= MAX_FILENAME_LENGTH:
        return test_name
    
    # If still too long, truncate and add ellipsis
    max_title_length = MAX_FILENAME_LENGTH - len(ext) - 4  # Account for .ext and ...
    truncated_title = sanitized_title[:max_title_length] + "..."
    return f"{truncated_title}.{ext}"

# Generate file path
def generate_file_path(name, title, ext, counter=0):
    safe_name = generate_safe_filename(name, title, ext)
    base = f"{DOWNLOAD_DIR}/{safe_name}"
    
    # Handle duplicate filenames
    if counter:
        name_part, ext_part = os.path.splitext(safe_name)
        base = f"{DOWNLOAD_DIR}/{name_part}({counter}){ext_part}"
    
    return base

# Download file
def download_file(url, path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, "wb") as file:
            file.write(response.content)
        return os.path.getsize(path) > 0
    except requests.RequestException as e:
        print(f"Download error: {e}")
        return False
    except OSError as e:
        print(f"Filesystem error: {e}")
        return False

# [Rest of your existing functions remain the same...]

# Main process
def main():
    args = parse_args()
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Ensure that the song download URL is provided
    if not args.u:
        print("Error: Song download URL (-u) is required.")
        sys.exit(1)

    # Decode the file name and title to handle any URL-encoded characters
    decoded_filename = unquote(args.f) if args.f else ""
    decoded_title = unquote(args.t) if args.t else "unknown_title"

    # Get file extension
    file_extension = get_file_extension(args.u)
    
    # Generate file path with safe filename handling
    file_path = generate_file_path(decoded_filename, decoded_title, file_extension)

    # Handle duplicate filenames
    counter = 0
    while os.path.exists(file_path):
        counter += 1
        file_path = generate_file_path(decoded_filename, decoded_title, file_extension, counter)

    print(f"Attempting to download to: {file_path}")  # Debug output

    # Download music file
    if not download_file(args.u, file_path):
        print("Download failed or file is empty")
        sys.exit(1)

    # [Rest of your main function remains the same...]

if __name__ == "__main__":
    main()
