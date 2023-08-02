import datetime
import os
import re
import sys
import argparse
import eyed3
import requests
from mutagen.flac import FLAC, Picture

parser = argparse.ArgumentParser()
parser.add_argument('-s', help='netease or tencent')
parser.add_argument('-f', help='song file name')
parser.add_argument('-u', help='song download url')
parser.add_argument('-c', help='song cover url')
parser.add_argument('-l', help='song lyrics')
parser.add_argument('-i', help='song id')
parser.add_argument('-t', help='song title')
parser.add_argument('-ar', help='song artist')
parser.add_argument('-al', help='song album')
parser.add_argument('-p', help='song publish time')

args = parser.parse_args()
song_source = args.s
song_filename = args.f
song_download_url = args.u
song_cover_url = args.c 
song_lyrics_url = args.l
song_id = args.i
song_title = args.t
song_artist = args.ar
song_album = args.al
song_publish_time = args.p

music_dir_name = "downloads"
if not os.path.exists(music_dir_name): os.mkdir(music_dir_name)

def name_get_music_path(name, music_type, name_counter = 0):
    music_path = music_dir_name + '/' + name + '.' + music_type
    if name_counter != 0:
        music_path = music_dir_name + '/' + name + "(" + str(name_counter) + ")" + "." + music_type
    return music_path

def url_get_type(url):
    """ 
    Matches the character after a dot (.), excluding the dot itself, 
    and stops matching when encountering a question mark (?).
    """
    pattern = r'((?!.*\.))([^?]+)'
    matches = re.search(pattern, url)
    if matches:
        return matches.group(0)
    return 'mp3'

music_type = url_get_type(song_download_url)
music_path = name_get_music_path(song_filename, music_type)

song_response = requests.get(song_download_url, timeout=10)
if song_response.content == None or song_response.content == b'':
    print('vip')
    sys.exit()
    
with open(music_path, "wb") as code:
    code.write(song_response.content)

if not os.path.getsize(music_path):
    print('vip')
    sys.exit()

print('success')
if music_type == 'mp3':
    audiofile = eyed3.load(music_path)
    if song_cover_url:
        cover_response = requests.get(song_cover_url)
        cover_content = cover_response.content
        image_type = song_cover_url[-3:]
        if image_type == 'jpg' or image_type == 'peg':
            audiofile.tag.images.set(3, cover_content, "image/jpeg")
        elif image_type  == 'png':
            audiofile.tag.images.set(3, cover_content, "image/png")
        
    if song_lyrics_url and song_source:
        lyric_response = requests.get(song_lyrics_url, timeout=10)
        if lyric_response.text != '':
            if song_source == 'netease':
                lyric_json = lyric_response.json()
                lyric = lyric_json['lrc']['lyric']
                audiofile.tag.lyrics.set(lyric)

    if song_id is not None: audiofile.tag.copyright = song_id

    if song_title is not None: audiofile.tag.title = song_title

    if song_artist is not None: audiofile.tag.artist = song_artist

    if song_album is not None: audiofile.tag.album = song_album
    
    if song_publish_time is not None: 
        publish_time = datetime.datetime.strptime(song_publish_time, '%Y-%m-%d %H:%M:%S')

        audiofile.tag.release_date = publish_time.strftime('%Y-%m-%d %H:%M:%S')
        audiofile.tag.recording_date = publish_time.strftime('%Y')
    
    if song_filename is not None: 
        try: audiofile.tag.save(encoding='utf-8')
        except: print('file save failed')
        

if music_type == 'flac':
    audiofile = FLAC(music_path)
    if song_cover_url:
        cover_response = requests.get(song_cover_url)
        cover_content = cover_response.content
        image_type = song_cover_url[-3:]
        if image_type == 'jpg' or image_type == 'peg':
            picture = Picture()
            picture.type = 3  # Front cover
            picture.mime = 'image/jpeg'  # MIME type of the image file
            picture.data = cover_content
            audiofile.add_picture(picture)
        elif image_type  == 'png':
            picture = Picture()
            picture.type = 3  # Front cover
            picture.mime = 'image/png'  # MIME type of the image file
            picture.data = cover_content
            audiofile.add_picture(picture)

    if song_lyrics_url and song_source:
        lyric_response = requests.get(song_lyrics_url, timeout=10)
        if lyric_response.text != '':
            if song_source == 'netease':
                lyric_json = lyric_response.json()
                lyric = lyric_json['lrc']['lyric']
                audiofile['lyrics'] = lyric

    if song_id is not None: audiofile['copyright'] = song_id

    if song_title is not None: audiofile['title'] = song_title

    if song_artist is not None: audiofile['artist'] = song_artist

    if song_album is not None: audiofile['album'] = song_album
    
    if song_publish_time is not None: 
        publish_time = datetime.datetime.strptime(song_publish_time, '%Y-%m-%d %H:%M:%S')

        audiofile['date'] = publish_time.strftime('%Y-%m-%d')

    if song_filename is not None: 
        try: audiofile.save()
        except: print('file save failed')