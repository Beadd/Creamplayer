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
import json
import os
import re
import secrets
import sys
import time

import binascii
import rsa.core
import rsa.common
import rsa.randnum
import rsa.transform
import rsa
import requests

from Crypto.Cipher import AES
from colorama import init
from termcolor import colored

# 有时eyed3会不太妙，使文件可以脱离eyed3运行
try: import eyed3; g_eyed3_exist = True
except ImportError: g_eyed3_exist = False


# 设置选项，使用set_代替g_，在mode_setting函数里被更改
set_name_add_artist = False
set_artist_add_name = False
set_download_lyric = True
set_download_cover_image_height = True
set_api_server = "http://api.injahow.cn/meting/"

g_music_dir_name = "MusicB"
g_width = os.get_terminal_size().columns # 为了打印一整行的分隔符
g_gui_width = 108 # gui显示窗口大小
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
    #'cookie':'NMTID=00O-UfVMage_XYVb01NofLYtGWN81wAAAGA6ROCHA; _ntes_nnid=0026f9a21f511bc7b813bc8257738ed7,1653178475744; _ntes_nuid=0026f9a21f511bc7b813bc8257738ed7; WNMCID=uzisge.1653178476562.01.0; WEVNSM=1.0.0; WM_TID=%2F8H5Vyp5GQxFUQERQRbFEfFcaI581rZl; _iuqxldmzr_=32; WM_NI=PvUHSZ6ODGORWadg5DK7d9SzSwgDNsEV3JehG9upEAJGRraJCFze%2B3Ix2YL4zAo9ukl3%2FPe2aI2kTlTFY9G%2Fgxu6Au7OWvM7p%2BiGGmIwnpbjRkJw9a7fOaUYlUq%2FU88eNlU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed1bc47b5efc0a7c46e95868aa2d84a939b9ab1c54ebced8cd9aa3baeb8bbaff02af0fea7c3b92a94aa9ba9d252f6918ca8ce5a95bfac88b85089e9acdad27291a9a9a5cd79878afdabe86485e7bb91c84b8a999e93e442819ab686aa398ba8febacf40ba9fa1daf861b0ede1b1e83aa397fe8cd768989a97dac625a5a8bbd7c47ff5919997d03db4f5a7a8c6678ba9a291e16292b58698bc6bf5ba8182d853b08bbfd0d834fcbb828dd837e2a3; JSESSIONID-WYYY=bTf0dAu0K3KzvcZDWFId0KCqJfkUUz%2Fnld6U6IhcZ2GBcGnbR%2B6P54Ex4sP%2B5aXIjrwtEDDyIaj%2FG5RM7gozKnk0%5C2cGnPn%2FtobEaEbkoGMTgAWXBWwzoWBkF5k3z1HSWb%5CND2rHARn0Ap7A85W7B%2BQ0D4DO5%2F%2F8Q3%2BjH0mjM%2B9%5CF%2FCq%3A1654302417314'
    'cookie':'JSESSIONID-WYYY=MqngSDeeeN%2FZRbE7Vmz7zZ1g9U3fs5SAD%5CbS23A0eW%2FhqzUHpYMX9jVlVgPosnC5wJdYO7se20QsYn45DoJor%5Cskxna6I%5CQKW733yxHugKPmYvN%2FP0%2BQOpOwkZJumC6t0QCh9rdwbk06t4TnjlMg%2Fa5Ooj1CW4idEdZq4VBMsDsIEhM3%3A1654304708419; _iuqxldmzr_=32; _ntes_nnid=59c0c0c4fc69665b6261b45f5e44fe4a,1654302908431; _ntes_nuid=59c0c0c4fc69665b6261b45f5e44fe4a; NMTID=00O-D3f-9XeBnQh0Ei2qy1d-ULEVSUAAAGBLCI6vA; WEVNSM=1.0.0; WNMCID=tqqzib.1654302908799.01.0; WM_NI=EROpEfsIky5J3M1%2F2Uw0BlLsOXn0anY7%2BSg1r8Y7PB%2B37llD5L2xuZ6sKBgI7WCTj5wOcXoIPycPEUR6dtcJmPPozE646Hv2qifgkQ76N5QKrDtVgERuCcCub6j65tgtVTU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeafdb6aa79efbd5ed6383928eb7d44e878e8e82d54bf4b2a9a5d16da7aba6d6c52af0fea7c3b92a878e8191c86eb197a59ab842f193ffd0b15fb5f08e8dcf798d88a2d1e4669be9e5b4e63bb2e897d8d34ae9edf98def50f794fe99f852f6ad85a3e643f5898db5e93fb591adb9ee4394a7adb1c85f92eaac95e242af90a090f94ff6ecfaa9f53ab3b7aa88ea5bf5ea82d6d441b29cbcb7e64f92ab8d84c27fa2eaa6d7b880a5ac9ab5d837e2a3; WM_TID=Pc31v8zNG7tFVRUUQAKVUgm1GFke%2Fj9Q'
}


def plog(pinfo):
    """ 用来输入没有换行符的内容 """
    print(pinfo, end = '')

def split_line(if_gui = False):
    """ 打印分割线 """
    if if_gui:
        print("=" * g_gui_width)
    else:
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

def name_get_music_path(name, name_counter = 0):
    """ 通过名称获取路径 """
    music_path = g_music_dir_name + '/' + name + ".mp3"
    if name_counter != 0:
        music_path = g_music_dir_name + '/' + name + "(" + str(
                name_counter) + ")" + ".mp3"
    return music_path

def path_get_lyric_path(path):
    """ 通过歌曲路径获得音乐路径 """
    lyric_path  = path.replace(".mp3", ".lrc")
    return lyric_path

def path_check_exist(path, sid, name):
    ''' 检测歌曲是否存在,存在返回True,不存在返回path '''
    if not g_eyed3_exist:
        if os.path.exists(path):
            return True
        else: return path
    counter = 1
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
        path = name_get_music_path(name, counter)
        counter += 1
    return path



















def json_download_music(data, headers, proxies):
    """ 此函数接受api json并进行下载,返回path,失败返回错误信息 """
    name = json_get_music_name(data)
    music_path = name_get_music_path(name)
    music_url = data['url']
    sid = apiurl_get_id(music_url)
    print(name)
    # 检测歌曲文件存在
    music_path = path_check_exist(music_path, sid, name)
    if music_path is True:
        print(colored("歌曲已存在,自动跳过", "yellow"))
        return "exist"
    music_req = requests.get(music_url, headers=headers, proxies=proxies, 
            timeout=10)
    if music_req.content is None:
        print(colored("下载失败,自动跳过", "yellow"))
        return
    with open(music_path, "wb") as code:
        code.write(music_req.content)
    if not os.path.getsize(music_path):
        print(colored("getsize失败,自动跳过,可能是vip歌曲", "yellow"))
        return "getsize"
    print('  ' + str(os.path.getsize(music_path)) + '字节')
    return music_path

def json_download_lyric(data, music_path, headers, proxies):
    """  此函数接受api json并进行下载歌词"""
    lyric_path = path_get_lyric_path(music_path)
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

def ID_add_hight_cover(music_id, audiofile, header163, proxies):
    """ 此函数接受id调用网易云接受获取高清封面 """
    music_url163 = "http://music.163.com/api/song/detail/?id=" +\
            music_id +"&ids=%5B" + music_id + "%5D"
    music_url163_response = requests.get(music_url163, headers=header163,
            proxies=proxies, timeout=10)
    music_data163 = json.loads(music_url163_response.text)
    music_cover_url = music_data163['songs'][0]['album']['blurPicUrl']
    audio_image = requests.get(music_cover_url, headers=header163,
            proxies=proxies, timeout=10)
    if audio_image.ok is False:
        print(colored("  网易云API封面出错", "yellow"))
        return
    image_type = music_cover_url[-3:]
    if image_type == 'jpg' or type == 'peg':
        audiofile.tag.images.set(3, audio_image.content, "image/jpeg")
    if image_type == 'png':
        audiofile.tag.images.set(3, audio_image.content, "image/png")
    plog("  已内嵌封面")

def json_add_low_cover(data, audiofile):
    """ 此函数向歌曲添加eyed3元素 """
    if data['pic'] is None: return
    audio_Image = requests.get(data['pic'], timeout=10)
    if audio_Image.ok is not False:
        audiofile.tag.images.set(3, audio_Image.content, "image/jpeg")
        plog("  已内嵌封面")

def json_add_eyed3(data, music_path, headers, proxies, header163, album_id=0):
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
        try: ID_add_hight_cover(music_id, audiofile, header163, proxies)
        except: json_add_low_cover(data, audiofile)
    if not set_download_cover_image_height:
        json_add_low_cover(data, audiofile)
    #lyrics
    lyric_response = requests.get(data['lrc'], headers=headers, 
            proxies=proxies, timeout=10)
    if lyric_response.text != '':
        audiofile.tag.lyrics.set(lyric_response.text)
        plog("  已内嵌歌词")
    else:
        plog("\n\033[33m歌词为空,eyed3嵌入失败,自动跳过\033[0m\n")
    #album
    if album_id != 0:
        audiofile.tag.album = str(album_id)
        plog("  已内嵌专辑")
    #save alright
    if data['name'] is not None:
        audiofile.tag.save(encoding='utf-8')
    print("")



















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



















def mode_music(api_path, headers, proxies, header163, gui = False, show_github = True):
    """ 此函数接受api,下载所有歌曲 """
    try: response = requests.get(api_path, headers = headers, proxies = proxies, timeout=10)
    except: 
        print(colored("连接错误:请关闭加速器或检查API服务是否设置正确后重试...", "yellow"))
        return
    data = json.loads(response.text)
    if 'error' in data: 
        split_line(gui)
        if gui:
            print("请输入合法ID!")
        else:
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
        if g_eyed3_exist:
            json_add_eyed3(data, music_path, headers, proxies, header163)
        if set_download_lyric:
            json_download_lyric(data, music_path, headers, proxies)
        counter += 1
    if show_github:
        split_line(gui)
        print(colored("Github: https://github.com/Beadd/MusicDownloader", "green"))
        print(colored("下载完成!已下载" + str(counter - 1) + "首歌曲。感谢使用!", "green"))
        if not gui:
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
    if not os.path.exists(g_music_dir_name): os.mkdir(g_music_dir_name)
    parser.add_argument('args_url', nargs='?', help='Music URL')
    parser.add_argument('--args_server', '-s', help='Download Music API Server')
    args = parser.parse_args()
    if args.args_server is not None: set_api_server = args.args_server 
    if args.args_url is None: pure_main()
    else: command_start(args)

if __name__ == "__main__":
    main()


######################################## GUI相关 ########################################
def gui_main():
    if not os.path.exists(g_music_dir_name): os.mkdir(g_music_dir_name)
    print('''
 __  __           _      _____                      _                 _           
|  \/  |         (_)    |  __ \                    | |               | |          
| \  / |_   _ ___ _  ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
| |\/| | | | / __| |/ __| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
| |  | | |_| \__ \ | (__| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
|_|  |_|\__,_|___/_|\___|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
''')
    split_line(True)
    print("歌曲自动下载至目录 " + g_music_dir_name + "中")
    print("歌词自动下载至目录 " + g_music_dir_name + "中")
    if g_eyed3_exist: print("eyeD3已启用")
    else: print("eyeD3未启用")

def gui_mode_setting(option_num):
    global set_name_add_artist
    global set_artist_add_name
    global set_download_lyric
    global set_download_cover_image_height

    option_set = option_num
    if option_set == 1:
        set_name_add_artist = not set_name_add_artist
        plog("歌曲名称后加歌手:")  
        plog("  |  ")
        print("(" + str(set_name_add_artist) + ")") 

    if option_set == 2:
        set_artist_add_name = not set_artist_add_name
        plog("歌曲名称前加歌手:")  
        plog("  |  ")
        print("(" + str(set_artist_add_name) + ")")

    if option_set == 3:
        set_download_lyric = not set_download_lyric
        plog("歌曲是否下载歌词:")  
        plog("  |  ")
        print("(" + str(set_download_lyric) + ")")

    if option_set == 4:
        set_download_cover_image_height = not set_download_cover_image_height
        plog("歌曲启用高清封面:")  
        plog("  |  ")
        print("(" + str(set_download_cover_image_height) + ")")

    return 0

def gui_get_urlid(input_content):
    music_id = url_get_id(input_content)
    return music_id

def gui_id_isdigit(music_id):
    if music_id.isdigit() == 0: 
        split_line(True)
        print("请输入合法ID!")
        return True
    return False

def gui_download(mode, id):
    if mode == 1:
        # 网易云单曲
        music_id = gui_get_urlid(id)
        if gui_id_isdigit(music_id): return
        api_path = "http://api.injahow.cn/meting/?type=song&id=" + str(music_id)
        mode_music(api_path, g_header, g_proxies, g_header163, True)
    if mode == 2:
        # 网易云歌单
        music_id = gui_get_urlid(id)
        if gui_id_isdigit(music_id): return
        api_path = "http://api.injahow.cn/meting/?type=playlist&id=" + str(music_id)
        mode_music(api_path, g_header, g_proxies, g_header163, True)
    if mode == 3:
        # QQ音乐单曲
        music_id = gui_get_urlid(id)
        api_path = "http://api.injahow.cn/meting/?server=tencent&type=song&id=" + str(music_id)
        mode_music(api_path, g_header, g_proxies, g_header163, True)
    if mode == 4:
        # QQ音乐歌单
        music_id = gui_get_urlid(id)
        api_path = "http://api.injahow.cn/meting/?server=tencent&type=playlist&id=" + str(music_id)
        mode_music(api_path, g_header, g_proxies, g_header163, True)
    if mode == 5:
        # 网易云专辑
        album_id = gui_get_urlid(id)
        if gui_id_isdigit(album_id): return
        mode_album(album_id, g_header, g_proxies, g_header163)
    if mode == 6:
        # 网易云歌手
        artist_id = gui_get_urlid(id)
        if gui_id_isdigit(artist_id): return
        album_list = artist_get_album_list(artist_id)
        for album_id in album_list:
            mode_album(album_id, g_header, g_proxies, g_header163)

def gui_set_api_server(url):
    global set_api_server
    set_api_server = url
