# coding=UTF-8
# use the word 'music' instead of 'song'

import os
import re
import sys
import json
import time
import requests
'''''''''eyed3'''''''''
g_eyed3_exist = True
try: import eyed3
except ImportError: g_eyed3_exist = False
'''''''''eyed3'''''''''

set_name_add_artist = True
set_download_lyric = True
set_download_cover_image_height = True

g_width = os.get_terminal_size().columns
g_log_dir = "MusicLogB"
g_logfile = g_log_dir + "/" + str(
    time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + ".log"

def Plog(pinfo, if_printf = True):
    if if_printf:
        print(pinfo, end = '')
    if not os.path.exists(g_log_dir):
        os.makedirs(g_log_dir)
    log = open(g_logfile, 'a', encoding='utf-8')
    log.write(str(pinfo) + "\n")
    log.close()

def NameReplace(name):
    for i in "\/:*?\">|":
        if i in name: name = name.replace(i, "-")
    return name

def GetMusicName(data):
    name = data['name']
    name = NameReplace(name)
    if set_name_add_artist:
        artist = data['artist']
        artist = NameReplace(artist)
        name = name + " - " + artist
    return name

def GetMusicPath(name, if_get_music_dir_name = False, name_counter = 0):
    music_dir_name = "MusicB"
    if if_get_music_dir_name:
        return music_dir_name
    music_path = music_dir_name + '/' + name + ".mp3"
    if name_counter != 0:
        music_path = music_dir_name + '/' + name + "(" + str(name_counter) + ")" + ".mp3"
    return music_path

def GetMusicLyricPath(name, if_get_lyric_dir_name = False):
    lyric_dir_name = "MusicB"
    if if_get_lyric_dir_name:
        return lyric_dir_name
    lyric_path  = lyric_dir_name + "/" + name + ".lrc"
    return lyric_path

def GetSid(music_url):
    sid = re.findall(r'id=(.*?)$', music_url) 
    return str(sid[0])

def CheckMusicExist(path, sid, name):
    '''存在返回True,不存在返回path'''
    if not g_eyed3_exist:
        if os.path.exists(path):
            return True
        else: return path
    counter = 1
    while os.path.exists(path):
        try: audiofile = eyed3.load(path)
        except: 
            Plog("\n\033[33m检测音乐eyed3失败,自动跳过\033[0m")
            return True
        try: id = audiofile.tag.copyright 
        except:
            Plog("\n\033[33m检测音乐eyed3失败,自动跳过\033[0m")
            return True
        if id == sid: return True
        path = GetMusicPath(name, False, counter)
    return path


def MusicFileDownload(data, headers, proxies):
    name = GetMusicName(data)
    music_path = GetMusicPath(name)
    music_url = data['url']
    sid = GetSid(music_url)
    Plog(name + '\n')
    # 检测歌曲文件存在
    music_path = CheckMusicExist(music_path, sid, name)
    if music_path == True:
        Plog("\033[33m歌曲已存在,自动跳过\033[0m\n")
        return "exist"
    music_req = requests.get(music_url, headers=headers, proxies=proxies)
    if music_req.content == None:
        Plog("\n\033[33m下载失败,自动跳过\033[0m\n")
        return
    with open(music_path, "wb") as code:
        code.write(music_req.content)
    if not os.path.getsize(music_path):
        Plog('\n\033[33mGetsize失败,自动跳过\033[0m\n')
        return "getsize"
    Plog('  ' + str(os.path.getsize(music_path)) + '字节\n')
    return 

def MusicLyricDownload(data, headers, proxies):
    name = GetMusicName(data)
    lyric_path = GetMusicLyricPath(name)
    lyric_url = data['lrc']
    lyric_response = requests.get(lyric_url, headers=headers, proxies=proxies)
    if lyric_response.text == '':
        Plog('\n\033[33m错误:歌词文件为空,自动跳过\033[0m\n')
        return 
    with open(lyric_path, "wb") as code:
        code.write(lyric_response.content)
    Plog('  歌词已保存至' + GetMusicLyricPath(name, True) + '\n')
    return


def MusicEyed3CoverImageHeight(data, audiofile, header163, proxies):
    url_song_id = data['url']
    song_id = re.findall(r'\d+$', url_song_id)
    song_id  = song_id[-1]
    url163_song_detail = "http://music.163.com/api/song/detail/?id=" + song_id +"&ids=%5B" + song_id + "%5D"
    response_song_detail = requests.get(url163_song_detail, headers=header163, proxies=proxies)
    data163_song_detail = json.loads(response_song_detail.text)
    url_song_image = data163_song_detail['songs'][0]['album']['blurPicUrl']
    audio_Image = requests.get(url_song_image, headers=header163, proxies=proxies)
    if audio_Image.ok == False:
        Plog("  网易云API封面出错")
        return
    type = url_song_image[-3:]
    if type == 'jpg' or type == 'peg':
        audiofile.tag.images.set(3, audio_Image.content, "image/jpeg")
    if type == 'png':
        audiofile.tag.images.set(3, audio_Image.content, "image/png")
    Plog("  已内嵌封面")

def MusicEyed3CoverImageLow(data, audiofile):
    if data['pic'] == None: 
        return
    audio_Image = requests.get(data['pic'])
    if audio_Image.ok != False:
        audiofile.tag.images.set(3, audio_Image.content, "image/jpeg")
        Plog("  已内嵌封面")


def MusicEyed3Add(data, headers, proxies, header163, album_id = 0):
    name = GetMusicName(data)
    music_path = GetMusicPath(name)
    try: audiofile = eyed3.load(music_path)
    except: 
        Plog("\n\033[33mEyed3: 打开音乐音乐失败,自动跳过\033[0m")
        return
    #title
    if data['name'] != None:
        audiofile.tag.title = data['name']
        Plog("  已内嵌名称")
    #artist
    if data['artist'] != 'NoneType':
        audiofile.tag.artist = data['artist']
        Plog("  已内嵌歌手")
    #id
    if data['url'] != 'NoneType':
        sid = GetSid(data['url'])
        audiofile.tag.copyright = str(sid)
        Plog("  已内嵌id")
    #image
    if set_download_cover_image_height:
        try: MusicEyed3CoverImageHeight(data, audiofile, header163, proxies)
        except: MusicEyed3CoverImageLow(data, audiofile)
    if not set_download_cover_image_height:
        MusicEyed3CoverImageLow(data, audiofile)
    #lyrics
    lyric_response = requests.get(data['lrc'], headers=headers, proxies=proxies)
    if lyric_response.text != '':
        audiofile.tag.lyrics.set(lyric_response.text)
        Plog("  已内嵌歌词")
    else:
        Plog("\n\033[33m歌词为空,eyed3嵌入失败,自动跳过\033[0m\n")
    #album
    if not album_id == 0:
        audiofile.tag.album = str(album_id)
        Plog("  已内嵌专辑")
    #save alright
    if data['name'] != None:
        audiofile.tag.save(encoding='utf-8')
        Plog("  已保存ID3信息", False)
    print("")


def MusicMode(api_path, headers, proxies, header163, show_github = True):
    try: response = requests.get(api_path, headers = headers, proxies = proxies)
    except: Plog("连接错误:请关闭加速器后重试...\n");return
    data = json.loads(response.text)
    if 'error' in data: 
        print("=" * g_width, end='')
        print("\033[33m请输入合法ID!\033[0m")
        return 
    counter = 0 + 1
    for data in data:
        Plog(str(counter) + " ")
        result = MusicFileDownload(data, headers, proxies)
        if result == "exist":
            continue
        if result == "getsize":
            continue
        if g_eyed3_exist:
            MusicEyed3Add(data, headers, proxies, header163)
        if set_download_lyric:
            MusicLyricDownload(data, headers, proxies)
        counter += 1
    if show_github:
        print("=" * g_width, end='')
        print("\033[32mGithub: https://github.com/Beadd/MusicDownloader\n\
下载完成!已下载%s首歌曲。感谢使用!\n\
\033[35m继续或输入 q 以退出\033[0m" % (str(counter - 1)))

def AlbumMode(api_path, headers, proxies, header163):
    response = requests.get(api_path, headers = header163, proxies = proxies)
    data163 = json.loads(response.text)
    if data163['code'] != 200:
        print("\033[33mAPI调用失败!")
        return
    num = data163['album']['size']
    for i in range(0, num):
        id = data163['album']['songs'][i]['id']
        api_path = "http://api.injahow.cn/meting/?type=song&id=" + str(id)
        try: response = requests.get(api_path, headers = headers, proxies = proxies)
        except: Plog("连接错误:请关闭加速器后重试...\n");return
        data = json.loads(response.text)
        if 'error' in data: return 0
        Plog("Album")
        MusicMode(api_path, headers, proxies, header163, False)


print('''
\033[34m  __  __           _     \033[35m _____                      _                 _           \033[0m
\033[34m |  \/  |         (_)    \033[35m|  __ \                    | |               | |          \033[0m
\033[34m | \  / |_   _ ___ _  ___\033[35m| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ \033[0m
\033[34m | |\/| | | | / __| |/ __\033[35m| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|\033[0m
\033[34m | |  | | |_| \__ \ | (__\033[35m| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   \033[0m
\033[34m |_|  |_|\__,_|___/_|\___\033[35m|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   \033[0m
''')
print("=" * g_width, end='')
Plog("歌曲自动下载至目录 " + GetMusicPath("", True) + "中\n")
Plog("歌词自动下载至目录 " + GetMusicLyricPath("", True) + "中\n")
Plog("日志保存于文件 " + g_logfile + " 中")
if g_eyed3_exist: print("eyeD3已启用")
else: print("eyeD3未启用")

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
    #'cookie':'NMTID=00O-UfVMage_XYVb01NofLYtGWN81wAAAGA6ROCHA; _ntes_nnid=0026f9a21f511bc7b813bc8257738ed7,1653178475744; _ntes_nuid=0026f9a21f511bc7b813bc8257738ed7; WNMCID=uzisge.1653178476562.01.0; WEVNSM=1.0.0; WM_TID=%2F8H5Vyp5GQxFUQERQRbFEfFcaI581rZl; _iuqxldmzr_=32; WM_NI=PvUHSZ6ODGORWadg5DK7d9SzSwgDNsEV3JehG9upEAJGRraJCFze%2B3Ix2YL4zAo9ukl3%2FPe2aI2kTlTFY9G%2Fgxu6Au7OWvM7p%2BiGGmIwnpbjRkJw9a7fOaUYlUq%2FU88eNlU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed1bc47b5efc0a7c46e95868aa2d84a939b9ab1c54ebced8cd9aa3baeb8bbaff02af0fea7c3b92a94aa9ba9d252f6918ca8ce5a95bfac88b85089e9acdad27291a9a9a5cd79878afdabe86485e7bb91c84b8a999e93e442819ab686aa398ba8febacf40ba9fa1daf861b0ede1b1e83aa397fe8cd768989a97dac625a5a8bbd7c47ff5919997d03db4f5a7a8c6678ba9a291e16292b58698bc6bf5ba8182d853b08bbfd0d834fcbb828dd837e2a3; JSESSIONID-WYYY=bTf0dAu0K3KzvcZDWFId0KCqJfkUUz%2Fnld6U6IhcZ2GBcGnbR%2B6P54Ex4sP%2B5aXIjrwtEDDyIaj%2FG5RM7gozKnk0%5C2cGnPn%2FtobEaEbkoGMTgAWXBWwzoWBkF5k3z1HSWb%5CND2rHARn0Ap7A85W7B%2BQ0D4DO5%2F%2F8Q3%2BjH0mjM%2B9%5CF%2FCq%3A1654302417314'
    'cookie':'JSESSIONID-WYYY=MqngSDeeeN%2FZRbE7Vmz7zZ1g9U3fs5SAD%5CbS23A0eW%2FhqzUHpYMX9jVlVgPosnC5wJdYO7se20QsYn45DoJor%5Cskxna6I%5CQKW733yxHugKPmYvN%2FP0%2BQOpOwkZJumC6t0QCh9rdwbk06t4TnjlMg%2Fa5Ooj1CW4idEdZq4VBMsDsIEhM3%3A1654304708419; _iuqxldmzr_=32; _ntes_nnid=59c0c0c4fc69665b6261b45f5e44fe4a,1654302908431; _ntes_nuid=59c0c0c4fc69665b6261b45f5e44fe4a; NMTID=00O-D3f-9XeBnQh0Ei2qy1d-ULEVSUAAAGBLCI6vA; WEVNSM=1.0.0; WNMCID=tqqzib.1654302908799.01.0; WM_NI=EROpEfsIky5J3M1%2F2Uw0BlLsOXn0anY7%2BSg1r8Y7PB%2B37llD5L2xuZ6sKBgI7WCTj5wOcXoIPycPEUR6dtcJmPPozE646Hv2qifgkQ76N5QKrDtVgERuCcCub6j65tgtVTU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeafdb6aa79efbd5ed6383928eb7d44e878e8e82d54bf4b2a9a5d16da7aba6d6c52af0fea7c3b92a878e8191c86eb197a59ab842f193ffd0b15fb5f08e8dcf798d88a2d1e4669be9e5b4e63bb2e897d8d34ae9edf98def50f794fe99f852f6ad85a3e643f5898db5e93fb591adb9ee4394a7adb1c85f92eaac95e242af90a090f94ff6ecfaa9f53ab3b7aa88ea5bf5ea82d6d441b29cbcb7e64f92ab8d84c27fa2eaa6d7b880a5ac9ab5d837e2a3; WM_TID=Pc31v8zNG7tFVRUUQAKVUgm1GFke%2Fj9Q'
}

def CheckIdFalse(id):
    if id.isdigit() == 0: 
        print("=" * g_width, end='')
        print("\033[33m请输入合法ID!\033[0m")
        return True
    else: return False

def Setting():
    global set_name_add_artist
    global set_download_lyric
    global set_download_cover_image_height
    print("歌曲名称后加歌手:" + "  \033[36m|\033[0m  1" + "(" + str(set_name_add_artist) + ")")
    print("歌曲是否下载歌词:" + "  \033[36m|\033[0m  2" + "(" + str(set_download_lyric) + ")")
    print("歌曲启用高清封面:" + "  \033[36m|\033[0m  3" + "(" + str(set_download_cover_image_height) + ")")
    set = input("输入数字自动修改:  \033[36m|\033[0m  ")
    if set == '1':
        set_name_add_artist = not set_name_add_artist
        print("歌曲名称后加歌手:" + "  \033[36m|\033[0m  1" + "(" + str(set_name_add_artist) + ")")
    if set == '2':
        set_download_lyric = not set_download_lyric
        print("歌曲是否下载歌词:" + "  \033[36m|\033[0m  2" + "(" + str(set_download_lyric) + ")")
    if set == '3':
        set_download_cover_image_height = not set_download_cover_image_height
        print("歌曲启用高清封面:" + "  \033[36m|\033[0m  3" + "(" + str(set_download_cover_image_height) + ")")
    else: return 0

if not os.path.exists(GetMusicPath(0, True)): os.mkdir(GetMusicPath(0, True))
if not os.path.exists(GetMusicLyricPath(0, True)) : os.mkdir(GetMusicLyricPath(0, True))

while True:
    print("下载网易云单曲  \033[36m|\033[0m  1")
    print("下载网易云歌单  \033[36m|\033[0m  2")
    print("下载QQ音乐单曲  \033[36m|\033[0m  3")
    print("下载QQ音乐歌单  \033[36m|\033[0m  4")
    print("下载网易云专辑  \033[36m|\033[0m  5")
    print("歌曲下载项设置  \033[36m|\033[0m  6")
    mode = input("输入数字选择:   \033[36m|\033[0m  ")
    if mode == 'q' or mode == 'quit' or mode == 'exit': exit()
    if mode == '1':
        print("=" * g_width, end='')
        id = input("请输入网易云单曲ID:")
        if CheckIdFalse(id): continue
        api_path = "http://api.injahow.cn/meting/?type=song&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == "2":
        print("=" * g_width, end='')
        id = input("请输入网易云歌单ID:")
        if CheckIdFalse(id): continue
        api_path = "http://api.injahow.cn/meting/?type=playlist&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == "3":
        print("=" * g_width, end='')
        id = input("请输入QQ音乐单曲ID:")
        api_path = "http://api.injahow.cn/meting/?server=tencent&type=song&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == "4":
        print("=" * g_width, end='')
        id = input("请输入QQ音乐歌单ID:")
        api_path = "http://api.injahow.cn/meting/?server=tencent&type=playlist&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == '5':
        print("=" * g_width, end='')
        id = input("请输入专辑ID:")
        if CheckIdFalse(id): continue
        api_path ="http://music.163.com/api/album/" + id + "?ext=true&id=" + id + "&offset=0&total=true&limit=10"
        AlbumMode(api_path, g_header, g_proxies, g_header163)
    if mode == '6':
        print("=" * g_width, end='')
        Setting()
    print("=" * g_width, end='')