"""
@repo: github.com/Beadd/MusicDownloader
为方便使用,只有一个文件,空20行分割成多段
注意: 
- 全局变量在开头添加g_前缀
- 除注释外,禁用全角
"""
# coding=UTF-8
# pylint: disable=W0702
# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=line-too-long
# pylint: disable=global-statement
# pylint: disable=multiple-statements
# pylint: disable=trailing-whitespace
# pylint: disable=consider-using-dict-items
# pylint: disable=anomalous-backslash-in-string

import argparse
import base64
import datetime
import json
import logging
import os
import re
import secrets
import sys
import time

import rsa.core
import rsa.common
import rsa.randnum
import rsa.transform
import rsa
import requests
from Crypto.Cipher import AES
from colorama import init
from termcolor import colored
from mutagen.flac import FLAC, Picture

# 有时eyed3会不太妙，使文件可以脱离eyed3运行
try: import eyed3; g_eyed3_exist = True
except ImportError: g_eyed3_exist = False


# 设置选项，使用set_代替g_，在mode_setting函数里被更改
set_name_add_artist = False
set_artist_add_name = False
set_download_lyric = True
set_download_cover_image_height = True
set_api_server = "https://api.injahow.cn/meting/"

g_music_dir_name = "MusicB"
g_log_dir = "MusicLogB"
g_log_path = g_log_dir + "/" + str(
    time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + ".log"
g_width = os.get_terminal_size().columns # 为了打印一整行的分隔符
g_base62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
g_iv = '0102030405060708'
g_presetKey = '0CoJUm6Qyw8W8jud'
g_publicKey = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgtQn2JZ34ZC28NWYpAUd98iZ37BUrX/aKzmFbt7clFSs6sXqHauqKWqdtLkF2KexO40H1YTX8z2lSgBBOAxLsvaklV8k4cBFK9snQXE9/DDaFt6Rr7iVZMldczhC0JNgTz+SHXT6CBHuX3e9SdB1Ua44oncaTWz7OBGLbCiK45wIDAQAB\n-----END PUBLIC KEY-----'
g_anonymous_token = "bf8bfeabb1aa84f9c8c3906c04a04fb864322804c83f5d607e91a04eae463c9436bd1a17ec353cf780b396507a3f7464e8a60f4bbc019437993166e004087dd32d1490298caf655c2353e58daa0bc13cc7d5c198250968580b12c1b8817e3f5c807e650dd04abd3fb8130b7ae43fcc5b"
g_proxies = { "http": None, "https": None }
g_header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    #,'cookie':
}
g_header163 = { # 直接请求网易云API所需
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    ,
    'cookie':'NMTID=00OHBEMpFi3cPSpAUnopJGHYmwKAB4AAAGIpKYnhA; JSESSIONID-WYYY=xV6q1IBuTol/Q8TMPvfmnccbq74W7YgzZmNfXDNt/vhGlkCdganO6\d/GpkkYwH74gsVfa+uuul1mQQbQn3rX1eF\RrQ29ickeByMbi4D98r0JBuy5KVsmpQs3neElqiIPfJ/eItmnGGsJqPQbmcwtT86M\Gy4udsP5U\zy2b+rpE8dx:1686391392103; _iuqxldmzr_=32; _ntes_nnid=b674c540d5a48ced68899908703b64fb,1686389592122; _ntes_nuid=b674c540d5a48ced68899908703b64fb; WEVNSM=1.0.0; WNMCID=qnoprd.1686389596766.01.0; WM_NI=JWOh0m9He9qvHbSw3Sd/RVKfvzx96SmUvn3l+VAELjyjvoauGwN9FhhH+QgoDzDnMm1sAMqtundYnjEIFtdS00WS7LURXuvQaZDIfzF9qeNBvHGQWx6eezmnCGCZkAQlUlI=; WM_NIKE=9ca17ae2e6ffcda170e2e6eed6ea34908c8785f934bceb8ab2c15f979e8b86d83ba8a9a59bc26dae86bbbbef2af0fea7c3b92a8a898189b367fb98abdaf47e8cbe9d98b259a8f19eb7ca6eb6a6b8dab559af8bba8fb268e98a8fa6cf62bbb6ba90e47f85a982dac564ac98e5b2e66588a68c8fd067f3ad8faef480b7b2acbaed6287978a95e759f4f099b4b648978e9896f55ba3868caae57286e7bf86cd4ab69889b2d674f6bbab9bf06681998dbbea4b93b49b8dcc37e2a3; WM_TID=rp0OaTRccD1BABEEFEPB0MlxmT02I/Y1'
}


def print_log(*args, sep=' ', end='\n', file=None):
    """ 与print绑定,将print输出作为日志存储 """
    message = sep.join(str(arg) for arg in args) + end
    logging.debug(message)
    if file is None:
        built_in_print(*args, sep=sep, end=end)

def plog(pinfo):
    """ 用来输入没有换行符的内容 """
    print(pinfo, end = '')

def split_line():
    """ 打印分割线 """
    print("=" * (g_width-1))

def name_check_and_replace(name):
    """ 将无法用于命名的符号更换成-并返回 """
    for i in "\/:*?\"<>|":
        if i in name: name = name.replace(i, "-")
    return name

def json_get_music_name(data):
    """ 从 api json 中返回可用名称 """
    name = data['name']
    name = name_check_and_replace(name)
    if set_name_add_artist:
        artist = data['artist']
        artist = name_check_and_replace(artist)
        name = name + " - " + artist
    if set_artist_add_name:
        artist = data['artist']
        artist = name_check_and_replace(artist)
        name = artist + " - " + name
    return name

def apiurl_get_id(music_url):
    """ 识别 api json 里的 url 并获取里面的歌曲ID """
    sid = re.findall(r'id=(.*?)$', music_url) 
    return str(sid[0])

def url_get_id(music_url):
    """ 识别各平台链接里的ID """
    if "id=" in music_url:
        music_url = re.findall(r'id=(.*?)$', music_url) 
        return music_url[0]
    if "songDetail/" in music_url:
        music_url = re.findall(r"songDetail/(\w+)", music_url)
        return music_url[0]
    if "playlist/" in music_url:
        music_url = re.findall(r"playlist/(\w+)", music_url)
        return music_url[0]
    return music_url

def url_get_platform(music_url):
    """ 通过URL识别平台 """
    if "song?id=" in music_url:
        return "netease_music"
    if "playlist?id=" in music_url:
        return "netease_playlist"
    if "album?id=" in music_url:
        return "netease_album"
    if "artist?id=" in music_url:
        return "netease_artist"
    if "songDetail/" in music_url:
        return "qq_music"
    if "playlist/" in music_url:
        return "qq_playlist"

def id_isdigit(music_id):
    """ 检测是否存在ID,并进行报错 """
    if music_id.isdigit() == 0: 
        print("=" * g_width, end='')
        print("\033[33m请输入合法ID!\033[0m")
        return True
    return False

def name_get_music_path(name, music_type, name_counter = 0):
    """ 通过名称获取路径 """
    music_path = g_music_dir_name + '/' + name + '.' + music_type
    if name_counter != 0:
        music_path = g_music_dir_name + '/' + name + "(" + str(
                name_counter) + ")" + "." + music_type
    return music_path

def path_get_lyric_path(path, music_type):
    """ 通过歌曲路径获得音乐路径 """
    lyric_path  = path.replace("." + music_type, ".lrc")
    return lyric_path

def path_check_exist(path, sid, name):
    ''' 检测歌曲是否存在,存在返回True,不存在返回path '''
    if not g_eyed3_exist:
        if os.path.exists(path):
            return True
        else: return path
    counter = 1
    music_type = url_get_type(path)
    while os.path.exists(path):
        try: audiofile = eyed3.load(path)
        except:  
            print(colored("检测音乐eyed3失败,自动跳过", "yellow"))
            return True
        try: music_id = audiofile.tag.copyright 
        except:
            print(colored("检测音乐eyed3失败,自动跳过", "yellow"))
            return True
        if music_id == sid: return True
        path = name_get_music_path(name, music_type, counter)
        counter += 1
    return path

def get_redirected_url(url, headers, proxies):
    """ redirect rul and return """
    response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    redirected_url = response.url
    return redirected_url

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



















def json_download_music(data, headers, proxies):
    """ 此函数接受api json并进行下载,返回path,失败返回错误信息 """
    name = json_get_music_name(data)

    music_url = data['url']
    sid = apiurl_get_id(music_url)

    redirected_url = get_redirected_url(music_url, headers, proxies)
    music_type = url_get_type(redirected_url)

    music_path = name_get_music_path(name, music_type)
    print(name)
    # 检测歌曲文件存在
    music_path = path_check_exist(music_path, sid, name)
    if music_path is True:
        print(colored("歌曲已存在,自动跳过", "yellow"))
        return "exist"
    music_req = requests.get(music_url, headers=headers, proxies=proxies, 
            timeout=10)
    if music_req.content == None or music_req.content == b'': # pylint: disable=singleton-comparison
        print(colored("下载失败,自动跳过,可能是vip歌曲", "yellow"))
        return "exit"
    with open(music_path, "wb") as code:
        code.write(music_req.content)
    if not os.path.getsize(music_path):
        print(colored("getsize失败,自动跳过,可能是vip歌曲", "yellow"))
        return "getsize"
    print('  ' + str(os.path.getsize(music_path)) + '字节')
    return music_path

def json_download_lyric(data, music_path, headers, proxies):
    """  此函数接受api json并进行下载歌词"""
    music_type = url_get_type(music_path)
    lyric_path = path_get_lyric_path(music_path, music_type)
    lyric_url = data['lrc']
    lyric_response = requests.get(lyric_url, headers=headers, proxies=proxies,
            timeout=10)
    if lyric_response.text == '':
        print(colored("错误:歌词文件为空,自动跳过", "yellow"))
        return 
    with open(lyric_path, "wb") as code:
        code.write(lyric_response.content)
    print("  歌词已保存至" + g_music_dir_name)
    return

def ID_add_high_cover(music_id, audiofile, music_type, header163, proxies):
    """ 此函数接受id调用网易云接口并对歌曲添加高清封面 """
    music_url163 = "http://music.163.com/api/song/detail/?id=" +\
            music_id +"&ids=%5B" + music_id + "%5D"
    music_url163_response = requests.get(music_url163, headers=header163,
            proxies=proxies, timeout=10)
    music_data163 = json.loads(music_url163_response.text)
    music_cover_url = music_data163['songs'][0]['album']['blurPicUrl']
    audio_image = requests.get(music_cover_url, headers=header163,
            proxies=proxies, timeout=10)
    if audio_image.ok is False:
        print(colored("  网易云封面API出错", "yellow"))
        raise ValueError
    image_type = music_cover_url[-3:]
    if image_type == 'jpg' or type == 'peg':
        if music_type == 'mp3':
            audiofile.tag.images.set(3, audio_image.content, "image/jpeg")
        if music_type == 'flac':
            picture = Picture()
            picture.type = 3  # Front cover
            picture.mime = 'image/jpeg'  # MIME type of the image file
            picture.data = audio_image.content
            audiofile.add_picture(picture)
    if image_type == 'png':
        if music_type == 'mp3':
            audiofile.tag.images.set(3, audio_image.content, "image/png")
        if music_type == 'flac':
            picture = Picture()
            picture.type = 3  # Front cover
            picture.mime = 'image/png'  # MIME type of the image file
            picture.data = audio_image.content
            audiofile.add_picture(picture)

def ID_add_high_cover_qq(music_id, audiofile, music_type, headers, proxies):
    """ 此函数接收id调用QQ音乐接口并对歌曲添加高清封面 """
    music_qq_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=' + music_id + '&tpl=yqq_song_detail&format=json&callback=getOneSongInfoCallback&g_tk=1928093487&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    music_qq_response = requests.get(music_qq_url, headers=headers, proxies=proxies, timeout=10)
    music_qq_data = json.loads(music_qq_response.text)
    music__qq_pmid = music_qq_data['data'][0]['album']['mid']
    music_qq_cover_url = 'https://y.qq.com/music/photo_new/T002R500x500M000' + music__qq_pmid + '.jpg?max_age=2592000'
    
    audio_image = requests.get(music_qq_cover_url, headers=headers, proxies=proxies, timeout=10)
    if audio_image.ok is False:
        music__qq_pmid = music_qq_data['data'][0]['singer'][0]['mid']
        music_qq_cover_url = 'https://y.qq.com/music/photo_new/T001R500x500M000' + music__qq_pmid + '.jpg?max_age=2592000'
        audio_image = requests.get(music_qq_cover_url, headers=headers, proxies=proxies, timeout=10)
    if audio_image.ok is False:
        print(colored("  QQ音乐封面API出错", "yellow"))
        raise ValueError
    
    if music_type == 'mp3':
        audiofile.tag.images.set(3, audio_image.content, "image/jpeg")
    if music_type == 'flac':
        picture = Picture()
        picture.type = 3  # Front cover
        picture.mime = 'image/jpeg'  # MIME type of the image file
        picture.data = audio_image.content
        audiofile.add_picture(picture)

def json_add_low_cover(data, music_type, audiofile):
    """ 此函数接受json向歌曲添加封面 """
    if data['pic'] is None: return
    audio_Image = requests.get(data['pic'], timeout=10)
    if audio_Image.ok is not False:
        if music_type == 'mp3':
            audiofile.tag.images.set(3, audio_Image.content, "image/jpeg")
        if music_type == 'flac':
            picture = Picture()
            picture.type = 3  # Front cover
            picture.mime = 'image/jpeg'  # MIME type of the image file
            picture.data = audio_Image.content
            audiofile.add_picture(picture)

def ID_get_music_album_id(music_id, header163, proxies):
    """ 此函数接受id调用网易云接口返回歌曲对应的专辑ID """
    music_url163_song = "http://music.163.com/api/song/detail/?id=" +\
            music_id +"&ids=%5B" + music_id + "%5D"
    music_url163_song_response = requests.get(music_url163_song, 
            headers=header163, proxies=proxies, timeout=10)
    music_data163_song = json.loads(music_url163_song_response.text)
    music_album_id = music_data163_song['songs'][0]['album']['id']
    return music_album_id

def ID_add_publish_time(music_id, audiofile, header163, proxies):
    """ 此函数接受id调用网易云接口并对音乐添加发布日期 """
    music_album_id = ID_get_music_album_id(music_id, header163, proxies)
    music_url163_album ="http://music.163.com/api/album/" + str(music_album_id) +\
            "?ext=true&id=" + str(music_album_id) + "&offset=0&total=true&limit=10"
    music_url163_album_response = requests.get(music_url163_album, 
            headers = header163, proxies = proxies, timeout=10)
    music_data163_album = json.loads(music_url163_album_response.text)
    if music_data163_album['status_code'] != 200:
        plog(colored("  API调用失败!", "yellow"))
        return
    music_public_time = music_data163_album['album']['publishTime']
    time_stamp = music_public_time / 1000
    date_time = datetime.datetime.fromtimestamp(time_stamp)

    music_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
    audiofile.tag.release_date = music_date
    music_date = date_time.strftime('%Y')
    audiofile.tag.recording_date = music_date
    return

def ID_add_publish_time_qq(music_id, audiofile, headers, proxies):
    """ 此函数调用QQ音乐接口并对音乐添加发行日期 """
    music_qq_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=' + music_id + '&tpl=yqq_song_detail&format=json&callback=getOneSongInfoCallback&g_tk=1928093487&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    music_qq_response = requests.get(music_qq_url, headers=headers, proxies=proxies, timeout=10)
    music_qq_data = json.loads(music_qq_response.text)
    music_date = music_qq_data['data'][0]['time_public']

    audiofile.tag.release_date = music_date
    music_date = datetime.datetime.strptime(music_date, "%Y-%m-%d")
    music_date = music_date.strftime('%Y')
    audiofile.tag.recording_date = music_date
    return

def ID_get_music_album_name(music_id, header163, proxies):
    """ 此函数接受id调用网易云接口返回歌曲对应的专辑名称 """
    music_url163_song = "http://music.163.com/api/song/detail/?id=" +\
            music_id +"&ids=%5B" + music_id + "%5D"
    music_url163_song_response = requests.get(music_url163_song, 
            headers=header163, proxies=proxies, timeout=10)
    music_data163_song = json.loads(music_url163_song_response.text)
    music_album_name = music_data163_song['songs'][0]['album']['name']
    return music_album_name

def ID_get_music_album_name_qq(music_id, headers, proxies):
    """ 此函数接收id调用QQ音乐接口返回对应的专辑名称 """
    music_qq_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid=' + music_id + '&tpl=yqq_song_detail&format=json&callback=getOneSongInfoCallback&g_tk=1928093487&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    music_qq_response = requests.get(music_qq_url, headers=headers, proxies=proxies, timeout=10)
    music_qq_data = json.loads(music_qq_response.text)
    music_album_name = music_qq_data['data'][0]['album']['name']
    return music_album_name


def json_add_eyed3(data, music_path, music_type, headers, proxies, header163):
    """ 此函数将音乐添加eyed3元素 """
    try: audiofile = eyed3.load(music_path)
    except: 
        plog("\n\033[33mEyed3: 打开音乐音乐失败,自动跳过\033[0m")
        return
    # title
    if data['name'] is not None:
        audiofile.tag.title = data['name']
        plog("  已内嵌名称")
    # artist
    if data['artist'] != 'NoneType':
        audiofile.tag.artist = data['artist']
        plog("  已内嵌歌手")
    # id
    if data['url'] != 'NoneType':
        sid = apiurl_get_id(data['url'])
        audiofile.tag.copyright = str(sid)
        plog("  已内嵌id")
    # image
    if set_download_cover_image_height:
        music_id = url_get_id(data['url'])
        try: 
            ID_add_high_cover(music_id, audiofile, music_type, header163, proxies)
            plog("  已内嵌高清封面")
        except: 
            try:
                ID_add_high_cover_qq(music_id, audiofile, music_type, headers, proxies)
                plog("  已内嵌高清封面")
            except:
                json_add_low_cover(data, music_type, audiofile)
                plog("  已内嵌封面")
    if not set_download_cover_image_height:
        json_add_low_cover(data, music_type, audiofile)
    # lyrics
    lyric_response = requests.get(data['lrc'], headers=headers, 
            proxies=proxies, timeout=10)
    if lyric_response.text != '':
        audiofile.tag.lyrics.set(lyric_response.text)
        plog("  已内嵌歌词")
    else:
        plog("\n\033[33m歌词为空,eyed3嵌入失败,自动跳过\033[0m\n")
    # album
    if audiofile.tag.copyright is not None:
        music_id = audiofile.tag.copyright
        try:
            music_album_name = ID_get_music_album_name(music_id, header163, proxies)
            audiofile.tag.album = music_album_name
            plog("  已内嵌专辑")
        except: 
            try:
                music_album_name = ID_get_music_album_name_qq(music_id, headers, proxies)
                audiofile.tag.album = music_album_name
                plog("  已内嵌专辑")
            except: pass
    # public time
    if audiofile.tag.copyright is not None:
        music_id = audiofile.tag.copyright
        try: 
            ID_add_publish_time(music_id, audiofile, header163, proxies)
            plog("  已内嵌发行日期")
        except: 
            try: 
                ID_add_publish_time_qq(music_id, audiofile, headers, proxies)
                plog("  已内嵌发行日期")
            except: pass
    #save alright
    if data['name'] is not None:
        audiofile.tag.save(encoding='utf-8')
    print("")

def json_add_mutagen(data, music_path, music_type, headers, proxies, header163):
    """ 此函数将音乐添加mutagen元素 """
    # Open the FLAC file
    try: audio = FLAC(music_path)
    except: 
        plog("\n\033[33mMutagen: 打开音乐音乐失败,自动跳过\033[0m")
        return
    # title
    if data['name'] is not None:
        audio['title'] = data['name']
        plog("  已内嵌名称")
    # artist
    if data['artist'] != 'NoneType':
        audio['artist'] = data['artist']
        plog("  已内嵌歌手")
    # image
    if set_download_cover_image_height:
        music_id = url_get_id(data['url'])
        try: 
            ID_add_high_cover(music_id, audio, music_type, header163, proxies)
            plog("  已内嵌高清封面")
        except: 
            try:
                ID_add_high_cover_qq(music_id, audio, music_type, headers, proxies)
                plog("  已内嵌高清封面")
            except:
                json_add_low_cover(data, music_type, audio)
                plog("  已内嵌封面")
    if not set_download_cover_image_height:
        json_add_low_cover(data, music_type, audio)
    # album
    try:
        music_album_name = ID_get_music_album_name(music_id, header163, proxies)
        audio['artist'] = music_album_name
        plog("  已内嵌专辑")
    except: 
        try:
            music_album_name = ID_get_music_album_name_qq(music_id, headers, proxies)
            audio['artist'] = music_album_name
            plog("  已内嵌专辑")
        except: pass
    # public time
    try: 
        ID_add_publish_time(music_id, audio, header163, proxies)
        plog("  已内嵌发行日期")
    except: 
        try: 
            ID_add_publish_time_qq(music_id, audio, headers, proxies)
            plog("  已内嵌发行日期")
        except: pass
    audio.save()















# 此段为贡献代码,提供了下载指定歌手的全部专辑功能
def rsa_no_padding(message, target_length):
    """ Padding method of RSA_NO_PADDING """
    message = message[::-1]
    max_msglength = target_length - 11
    msglength = len(message)

    if msglength > max_msglength:
        # pylint: disable=consider-using-f-string
        raise OverflowError('%i bytes needed for message, but there is only'
                            ' space for %i' % (msglength, max_msglength))
    padding_length = target_length - msglength - 3

    return b''.join([b'\x00\x00',padding_length * b'\x00',b'\x00',message])

def encrypt (data) :
    """ encrypt """
    bs = AES.block_size
    # pylint: disable=unnecessary-lambda-assignment
    aes_pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs) 

    data_encrypted = {}
    data_text = json.dumps(data)
    random_byte_array = secrets.token_bytes(16)
    secret_key = "".join(map(lambda n : g_base62[n%62], random_byte_array))

    # AES encrypt
    preset_chiper = AES.new(key=bytes(g_presetKey, 'utf-8'), mode=AES.MODE_CBC, iv=bytes(g_iv, 'utf-8'))
    preset_encrypted = preset_chiper.encrypt(bytes(aes_pad(data_text), 'utf-8'))
    preset_encrypted_b64 = base64.b64encode(preset_encrypted).decode('ascii')

    secret_chiper = AES.new(key=bytes(secret_key, 'utf-8'), mode=AES.MODE_CBC, iv=bytes(g_iv, 'utf-8'))
    secret_encrypted = secret_chiper.encrypt(bytes(aes_pad(preset_encrypted_b64), 'utf-8'))
    secret_encrypted_b64 = base64.b64encode(secret_encrypted).decode('ascii')

    data_encrypted['params'] = secret_encrypted_b64

    # RSA encrypt
    rsa_pub = rsa.PublicKey.load_pkcs1_openssl_pem(bytes(g_publicKey, 'utf-8'))
    keylength = rsa.common.byte_size(rsa_pub.n)
    padded_message = rsa_no_padding(bytes(secret_key, 'utf-8'), keylength)

    payload = rsa.transform.bytes2int(padded_message)
    encrypted = rsa.core.encrypt_int(payload, rsa_pub.e, rsa_pub.n)
    block = rsa.transform.int2bytes(encrypted, keylength)

    data_encrypted['encSecKey'] = block.hex()

    return data_encrypted

def artist_get_album_list(artist_id):
    """ 通过歌手获取所有专辑 """
    album_list = []
    cookies = {
        '__remember_me': True,
        'NMTID': secrets.token_bytes(16).hex(),
        '_ntes_nuid': secrets.token_bytes(16).hex(),
        'MUSIC_A': g_anonymous_token,
    }
    # url = "https://www.httpbin.org/post"
    url = "https://music.163.com/weapi/artist/albums/" + artist_id
    # print(url)
    limit = 30
    offset = 0
    total = True
    data = { 'limit': limit, 'offset': offset, 'total': total , }
    headers = g_header
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    cookies_val = ''
    for key in cookies:
        cookies_val += (str(key) + '=' + str(cookies[key]) + '; ')
    # print(cookies_val)
    headers['Cookies'] = cookies_val

    # data = {"encSecKey":"1a9e1c34f0f8e3420293845fc24b4a79bae53f150e09b2bad6c88d8db6379781c14dadffe91f12e081abb6e0c7f1efd889c025946e2e855f5b1312806c133451f4ba57afd9ea5b9e4286afc379c6321d882574e68b18436909a646fe89319196a2c37ef2a5730a27e4325bc531e895ecfd9494c9a847e061ce54d3cf47fc6236","params":"9bhq3DTYBbw3wwGUysFiAmSg5AYSq6+EJDcV02bM87rQFR3OFUCPAUfQAEor9HzgiHR+HTtkuylKfUzfe97DTgG8ljRT146dhDY52qZpbVC/7Z/KsTUnMD1sl/FRzSt9"}
    while True:
    # for num in range(2):
        enc_data = encrypt(data)
        r = requests.post(url=url, headers=headers, data=enc_data, timeout=10)
        album = json.loads(r.text)
        # print(r.text)

        hot_album = album['hotAlbums']
        for ab in hot_album:
            album_list.append(ab['id'])

        data['offset'] = data['offset'] + data['limit']
        # print(album['more'])
        # print(data)
        if (album['more'] is False) : break # pylint: disable=superfluous-parens

    return album_list



















def mode_music(api_path, headers, proxies, header163, show_github = True):
    """ 此函数接受api,下载所有歌曲 """
    try: response = requests.get(api_path, headers = headers, proxies = proxies, timeout=10)
    except: 
        print(colored("连接错误:请关闭加速器或检查API服务是否设置正确后重试...", "yellow"))
        return
    data = json.loads(response.text)
    if 'error' in data: 
        split_line()
        print("\033[33m请输入合法ID!\033[0m")
        return 
    counter = 0 + 1
    for data in data:
        plog(str(counter) + " ")
        music_path = json_download_music(data, headers, proxies)
        if music_path == "exist":
            continue
        if music_path == "getsize":
            continue
        if music_path == "exit":
            continue
        music_type = url_get_type(music_path)
        if music_type == 'flac':
            json_add_mutagen(data, music_path, music_type, headers, proxies, header163)
        if music_type == "mp3":
            if g_eyed3_exist:
                json_add_eyed3(data, music_path, music_type, headers, proxies, header163)
        if set_download_lyric:
            json_download_lyric(data, music_path, headers, proxies)
        counter += 1
    if show_github:
        split_line()
        print(colored("Github: https://github.com/Beadd/MusicDownloader", "green"))
        print(colored("下载完成!已下载" + str(counter - 1) + "首歌曲。感谢使用!", "green"))
        print("\033[35m继续或输入 q 以退出\033[0m")

def mode_album(album_id, headers, proxies, header163):
    """ 此函数接受专辑id,调用网易云接口和mode_music """
    api_netease_music = set_api_server + "?type=song&id="
    api_path ="http://music.163.com/api/album/" + str(album_id) +\
            "?ext=true&id=" + str(album_id) + "&offset=0&total=true&limit=10"
    response = requests.get(api_path, headers = header163, 
            proxies = proxies, timeout=10)
    data163 = json.loads(response.text)
    if data163['code'] != 200:
        print("\033[33mAPI调用失败!")
        return
    num = data163['album']['size']
    for i in range(0, num):
        music_id = data163['album']['songs'][i]['id']
        api_path = api_netease_music + str(music_id)
        try: response = requests.get(api_path, headers = headers, 
                proxies = proxies, timeout=10)
        except: 
            print(colored("连接错误:请关闭加速器或检查API服务是否设置正确后重试...", "yellow"))
            return
        data = json.loads(response.text)
        if 'error' in data: return 0
        plog("Album")
        mode_music(api_path, headers, proxies, header163, False)

def mode_setting():
    """ 设置模式,修改全局变量set_ """
    global set_name_add_artist
    global set_artist_add_name
    global set_download_lyric
    global set_download_cover_image_height
    global set_api_server

    split_line()
    plog("歌曲名称后加歌手:")  
    plog(colored("  |  ", "cyan"))
    print("1(" + str(set_name_add_artist) + ")")
    
    plog("歌曲名称前加歌手:")  
    plog(colored("  |  ", "cyan"))
    print("2(" + str(set_artist_add_name) + ")")
    
    plog("歌曲是否下载歌词:")  
    plog(colored("  |  ", "cyan"))
    print("3(" + str(set_download_lyric) + ")")

    plog("歌曲启用高清封面:")  
    plog(colored("  |  ", "cyan"))
    print("4(" + str(set_download_cover_image_height) + ")")

    plog("设置歌曲API服务器:")
    plog(colored(" |  ", "cyan")) 
    print("5(" + set_api_server + ")")

    plog("输入数字自动修改:")
    plog(colored("  |  ", "cyan"))

    option_set = input()
    if option_set == '1':
        set_name_add_artist = not set_name_add_artist
        plog("歌曲名称后加歌手:")  
        plog(colored("  |  ", "cyan"))
        print("1(" + str(set_name_add_artist) + ")") 

    if option_set == '2':
        set_artist_add_name = not set_artist_add_name
        plog("歌曲名称前加歌手:")  
        plog(colored("  |  ", "cyan"))
        print("2(" + str(set_artist_add_name) + ")")

    if option_set == '3':
        set_download_lyric = not set_download_lyric
        plog("歌曲是否下载歌词:")  
        plog(colored("  |  ", "cyan"))
        print("3(" + str(set_download_lyric) + ")")

    if option_set == '4':
        set_download_cover_image_height = not set_download_cover_image_height
        plog("歌曲启用高清封面:")  
        plog(colored("  |  ", "cyan"))
        print("4(" + str(set_download_cover_image_height) + ")")

    if option_set == '5':
        set_api_server = input("设置歌曲API服务器:" + colored(" |  ", "cyan"))
        plog("设置歌曲API服务器:")
        plog(colored(" |  ", "cyan")) 
        print("5(" + set_api_server + ")")
    return 0



















def start_function(music_url = None):
    """ 开始接受输入并下载 """
    api_netease_music = set_api_server + "?type=song&id="
    api_netease_playlist = set_api_server + "?type=playlist&id="
    api_qq_music = set_api_server + "?server=tencent&type=song&id="
    api_qq_playlist = set_api_server + "?server=tencent&type=playlist&id="
    split_line()
    if music_url is None:
        print(colored("输入q退出,输入s进入设置", "cyan"))
        mode = input("请输入歌曲或歌单或歌手或专辑链接：")
    else: mode = music_url
    if mode == 'q' or mode == 'quit' or mode == 'exit': sys.exit()
    if mode == 's' or mode == 'set' or mode == 'setting': 
        mode_setting()
        return
    if url_get_platform(mode) == 'netease_music':
        # 网易云单曲
        api_path = api_netease_music + url_get_id(mode)
        mode_music(api_path, g_header, g_proxies, g_header163)
        return
    if url_get_platform(mode) == 'netease_playlist':
        # 网易云歌单
        api_path = api_netease_playlist + url_get_id(mode)
        mode_music(api_path, g_header, g_proxies, g_header163)
        return
    if url_get_platform(mode) == 'netease_album':
        # 网易云专辑
        album_id = url_get_id(mode)
        mode_album(album_id, g_header, g_proxies, g_header163)
        return
    if url_get_platform(mode) == 'netease_artist':
        # 网易云歌手
        artist_id = url_get_id(mode)
        album_list = artist_get_album_list(artist_id)
        for album_id in album_list:
            mode_album(album_id, g_header, g_proxies, g_header163)
        return
    if url_get_platform(mode) == 'qq_music':
        # QQ音乐单曲
        api_path = api_qq_music + url_get_id(mode)
        mode_music(api_path, g_header, g_proxies, g_header163)
        return
    if url_get_platform(mode) == 'qq_playlist':
        # QQ音乐歌单
        api_path = api_qq_playlist + str(url_get_id(mode))
        mode_music(api_path, g_header, g_proxies, g_header163)
        return
    else: 
        print(colored("请输入完整的URL", "yellow"))

def pure_main():
    """ 无参启动时的主函数 """
    print('''
\033[34m  __  __           _     \033[35m _____                      _                 _           \033[0m
\033[34m |  \/  |         (_)    \033[35m|  __ \                    | |               | |          \033[0m
\033[34m | \  / |_   _ ___ _  ___\033[35m| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ \033[0m
\033[34m | |\/| | | | / __| |/ __\033[35m| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|\033[0m
\033[34m | |  | | |_| \__ \ | (__\033[35m| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   \033[0m
\033[34m |_|  |_|\__,_|___/_|\___\033[35m|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   \033[0m''')
    split_line()
    if g_eyed3_exist: print(colored("✓ ", "green") + "EyeD3元素已启用")
    else: print(colored("✗ ", "red") + "EyeD3元素未启用")
    print(colored("✓ ", "green") + "网易云单曲下载")
    print(colored("✓ ", "green") + "网易云歌单下载")
    print(colored("✓ ", "green") + "网易云专辑下载")
    print(colored("✓ ", "green") + "网易云歌手下载")
    print(colored("✓ ", "green") + "网易云我喜欢的歌曲下载")
    print(colored("✓ ", "green") + "QQ音乐单曲下载")
    print(colored("✓ ", "green") + "QQ音乐歌单下载")
    print(colored("✓ ", "green") + "QQ音乐我喜欢的歌曲下载")
    while True: start_function()

def command_start(args):
    """ 有参启动时主函数 """
    music_url = args.args_url
    start_function(music_url)


def main():
    """ 功能优先添加到此函数中 """
    global set_api_server
    init() # 初始化colorama库
    parser = argparse.ArgumentParser() # 启动参数检测
    parser.add_argument('args_url', nargs='?', help='Music URL')
    parser.add_argument('--args_server', '-s', help='Download Music API Server')
    args = parser.parse_args()
    if args.args_server is not None: set_api_server = args.args_server 
    if args.args_url is None: pure_main()
    else: command_start(args)

if __name__ == "__main__":
    if not os.path.exists(g_music_dir_name): os.mkdir(g_music_dir_name)
    if not os.path.exists(g_log_dir): os.mkdir(g_log_dir)
    logging.basicConfig(filename=g_log_path, level=logging.DEBUG)
    built_in_print = print
    print = print_log # pylint: disable=redefined-builtin
    main()
