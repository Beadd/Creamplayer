import os
import sys
import datetime
import argparse
import requests
import eyed3
from mutagen.flac import FLAC, Picture
from urllib.parse import unquote
import urllib.parse

# Define download directory
DOWNLOAD_DIR = "downloads"

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

# Generate file path
def generate_file_path(name, ext, counter=0):
    base = f"{DOWNLOAD_DIR}/{name}"
    return f"{base}({counter}).{ext}" if counter else f"{base}.{ext}"

# Download file
def download_file(url, path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(path, "wb") as file:
            file.write(response.content)
        return os.path.getsize(path) > 0
    except requests.RequestException:
        return False

# Save lyrics to a separate file
def save_lyrics(lyrics_url, song_title):
    try:
        lyrics_response = requests.get(lyrics_url)
        if lyrics_response.ok:
            lyrics = lyrics_response.json().get('lrc', {}).get('lyric', '')
            lyrics_path = generate_file_path(song_title, "lrc")
            with open(lyrics_path, "w", encoding="utf-8") as lyrics_file:
                lyrics_file.write(lyrics)
        else:
            print("Failed to download lyrics")
    except requests.RequestException as e:
        print(f"Error downloading lyrics: {e}")

# Set MP3 metadata
def set_mp3_metadata(path, metadata):
    audio = eyed3.load(path)
    if not audio:
        print(f"Unable to load file: {path}")
        return

    audio.initTag()  
    # Set cover
    if metadata['cover_url']:
        cover_data = requests.get(metadata['cover_url']).content
        mime_type = "image/jpeg" if metadata['cover_url'].endswith(('jpg', 'jpeg')) else "image/png"
        audio.tag.images.set(3, cover_data, mime_type)
    
    # Set lyrics
    if metadata['lyrics_url']:
        lyrics_url = metadata['lyrics_url']
        lyrics_response = requests.get(lyrics_url)
        if lyrics_response.ok:
            lyrics = lyrics_response.json().get('lrc', {}).get('lyric', '')
            audio.tag.lyrics.set(lyrics)

    # Set other metadata, ensuring UTF-8 encoding
    audio.tag.title = metadata['title']
    audio.tag.artist = metadata['artist']
    audio.tag.album = metadata['album']
    audio.tag.copyright = metadata['song_id']

    # Set publish time
    if metadata['publish_time']:
        try:
            publish_time = datetime.datetime.strptime(metadata['publish_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print("Invalid publish time format. Expected YYYY-MM-DD HH:MM:SS")
            sys.exit(1)

        release_time = publish_time.strftime('%Y-%m-%dT%H:%M:%S')
        audio.tag.recording_date = release_time
        audio.tag.release_time = release_time

    try:
        url_encoded_path = urllib.parse.quote(path)
        audio.tag.save(encoding='utf-8')
        print("MP3 metadata saved successfully:" + url_encoded_path)
    except Exception as e:
        print(f"Failed to save MP3 metadata: {e}")

# Set FLAC metadata
def set_flac_metadata(path, metadata):
    audio = FLAC(path)
    # Set cover
    if metadata['cover_url']:
        cover_data = requests.get(metadata['cover_url']).content
        mime_type = "image/jpeg" if metadata['cover_url'].endswith(('jpg', 'jpeg')) else "image/png"
        picture = Picture()
        picture.type = 3
        picture.mime = mime_type
        picture.data = cover_data
        audio.add_picture(picture)

    # Set other metadata, ensuring UTF-8 encoding
    audio['title'] = metadata['title']
    audio['artist'] = metadata['artist']
    audio['album'] = metadata['album']
    audio['copyright'] = metadata['song_id']

    # Set publish time
    if metadata['publish_time']:
        publish_time = metadata['publish_time']
        publish_time = datetime.datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        audio['date'] = publish_time.strftime('%Y-%m-%d')

    try:
        audio.save()
        print("FLAC metadata saved successfully:" + path)
    except Exception as e:
        print("Failed to save FLAC metadata:" + e)

# Main process
def main():
    args = parse_args()
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Ensure that the song download URL is provided
    if not args.u:
        print("Error: Song download URL (-u) is required.")
        sys.exit(1)

    # Decode the file name to handle any URL-encoded characters
    decoded_filename = unquote(args.f)

    # Get file extension and path
    file_extension = get_file_extension(args.u)
    file_path = generate_file_path(decoded_filename, file_extension)

    # Download music file
    if not download_file(args.u, file_path):
        print("Download failed or file is empty")
        sys.exit(1)

    # Prepare metadata dictionary
    metadata = {
        'cover_url': args.c,
        'lyrics_url': args.l,
        'song_id': args.i,
        'title': unquote(args.t),
        'artist': unquote(args.ar),
        'album': unquote(args.al),
        'publish_time': args.p
    }

    # Save lyrics to a separate file if requested
    if args.sl and args.l:
        save_lyrics(args.l, decoded_filename)

    # Set metadata for the downloaded file
    if file_extension == "mp3":
        set_mp3_metadata(file_path, metadata)
    elif file_extension == "flac":
        set_flac_metadata(file_path, metadata)
    else:
        print(f"Unsupported file type: {file_extension}")

if __name__ == "__main__":
    main()
