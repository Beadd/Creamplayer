# coding=UTF-8
# use the word 'music' instead of 'song'

import os
import re
import sys
import json
import time
import requests
import secrets
import base64
from Crypto.Cipher import AES
import rsa
import binascii
import rsa.randnum
import rsa.common
import rsa.transform
import rsa.core
'''''''''eyed3'''''''''
g_eyed3_exist = True
try: import eyed3
except ImportError: g_eyed3_exist = False
'''''''''eyed3'''''''''

set_name_add_artist = True
set_artist_add_name = False
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
    if set_artist_add_name:
        artist = data['artist']
        artist = NameReplace(artist)
        name = artist + " - " + name
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
        counter += 1
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
    return music_path

def MusicLyricDownload(data, music_path, headers, proxies):
    lyric_path = re.sub(r"\.mp3$", ".lrc", music_path)
    lyric_url = data['lrc']
    lyric_response = requests.get(lyric_url, headers=headers, proxies=proxies)
    if lyric_response.text == '':
        Plog('\n\033[33m错误:歌词文件为空,自动跳过\033[0m\n')
        return 
    with open(lyric_path, "wb") as code:
        code.write(lyric_response.content)
    Plog('  歌词已保存至' + GetMusicLyricPath(0, True) + '\n')
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


def MusicEyed3Add(data, music_path, headers, proxies, header163, album_id = 0):
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
        music_path = MusicFileDownload(data, headers, proxies)
        if music_path == "exist":
            continue
        if music_path == "getsize":
            continue
        if g_eyed3_exist:
            MusicEyed3Add(data, music_path, headers, proxies, header163)
        if set_download_lyric:
            MusicLyricDownload(data, music_path, headers, proxies)
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

base62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
iv = '0102030405060708'
presetKey = '0CoJUm6Qyw8W8jud'
publicKey = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgtQn2JZ34ZC28NWYpAUd98iZ37BUrX/aKzmFbt7clFSs6sXqHauqKWqdtLkF2KexO40H1YTX8z2lSgBBOAxLsvaklV8k4cBFK9snQXE9/DDaFt6Rr7iVZMldczhC0JNgTz+SHXT6CBHuX3e9SdB1Ua44oncaTWz7OBGLbCiK45wIDAQAB\n-----END PUBLIC KEY-----'
anonymous_token = "bf8bfeabb1aa84f9c8c3906c04a04fb864322804c83f5d607e91a04eae463c9436bd1a17ec353cf780b396507a3f7464e8a60f4bbc019437993166e004087dd32d1490298caf655c2353e58daa0bc13cc7d5c198250968580b12c1b8817e3f5c807e650dd04abd3fb8130b7ae43fcc5b"
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

    # Padding method of RSA_NO_PADDING
def rsa_no_padding(message, target_length):
    message = message[::-1]
    max_msglength = target_length - 11
    msglength = len(message)
 
    if msglength > max_msglength:
        raise OverflowError('%i bytes needed for message, but there is only'
                            ' space for %i' % (msglength, max_msglength))
    padding_length = target_length - msglength - 3
 
    return b''.join([b'\x00\x00',padding_length * b'\x00',b'\x00',message])

def encrypt (data) :
    bs = AES.block_size
    aes_pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    data_encrypted = {}
    data_text = json.dumps(data)
    random_byte_array = secrets.token_bytes(16)
    secret_key = "".join(map(lambda n : base62[n%62], random_byte_array))

    # AES encrypt
    preset_chiper = AES.new(key=bytes(presetKey, 'utf-8'), mode=AES.MODE_CBC, iv=bytes(iv, 'utf-8'))
    preset_encrypted = preset_chiper.encrypt(bytes(aes_pad(data_text), 'utf-8'))
    preset_encrypted_b64 = base64.b64encode(preset_encrypted).decode('ascii')

    secret_chiper = AES.new(key=bytes(secret_key, 'utf-8'), mode=AES.MODE_CBC, iv=bytes(iv, 'utf-8'))
    secret_encrypted = secret_chiper.encrypt(bytes(aes_pad(preset_encrypted_b64), 'utf-8'))
    secret_encrypted_b64 = base64.b64encode(secret_encrypted).decode('ascii')

    data_encrypted['params'] = secret_encrypted_b64

    # RSA encrypt
    rsa_pub = rsa.PublicKey.load_pkcs1_openssl_pem(bytes(publicKey, 'utf-8'))
    keylength = rsa.common.byte_size(rsa_pub.n)
    padded_message = rsa_no_padding(bytes(secret_key, 'utf-8'), keylength)
 
    payload = rsa.transform.bytes2int(padded_message)
    encrypted = rsa.core.encrypt_int(payload, rsa_pub.e, rsa_pub.n)
    block = rsa.transform.int2bytes(encrypted, keylength)

    data_encrypted['encSecKey'] = block.hex()

    return data_encrypted

    # Get All Albums
def ArtistAlbumList (artist_id) :
    album_list = []
    cookies = {
        '__remember_me': True,
        'NMTID': secrets.token_bytes(16).hex(),
        '_ntes_nuid': secrets.token_bytes(16).hex(),
        'MUSIC_A': anonymous_token,
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
        r = requests.post(url=url, headers=headers, data=enc_data)
        album = json.loads(r.text)
        # print(r.text)

        hot_album = album['hotAlbums']
        for ab in hot_album:
            album_list.append(ab['id'])

        data['offset'] = data['offset'] + data['limit']
        # print(album['more'])
        # print(data)
        if (album['more'] == False) :
            break

    return album_list


def GetMusicID(id):
    if "id=" in id:
        id = re.findall(r'id=(.*?)$', id) 
        return id[0]
    if "songDetail/" in id:
        id = re.findall(r"songDetail/(\w+)", id)
        return id[0]
    if "playlist/" in id:
        id = re.findall(r"playlist/(\w+)", id)
        return id[0]
    return id

def CheckIdFalse(id):
    if id.isdigit() == 0: 
        print("=" * g_width, end='')
        print("\033[33m请输入合法ID!\033[0m")
        return True
    else: return False

def Setting():
    global set_name_add_artist
    global set_artist_add_name
    global set_download_lyric
    global set_download_cover_image_height
    print("歌曲名称后加歌手:" + "  \033[36m|\033[0m  1" + "(" + str(set_name_add_artist) + ")")
    print("歌曲名称前加歌手:" + "  \033[36m|\033[0m  2" + "(" + str(set_artist_add_name) + ")")
    print("歌曲是否下载歌词:" + "  \033[36m|\033[0m  3" + "(" + str(set_download_lyric) + ")")
    print("歌曲启用高清封面:" + "  \033[36m|\033[0m  4" + "(" + str(set_download_cover_image_height) + ")")
    set = input("输入数字自动修改:  \033[36m|\033[0m  ")
    if set == '1':
        set_name_add_artist = not set_name_add_artist
        print("歌曲名称后加歌手:" + "  \033[36m|\033[0m  1" + "(" + str(set_name_add_artist) + ")")
    if set == '2':
        set_artist_add_name = not set_artist_add_name
        print("歌曲名称前加歌手:" + "  \033[36m|\033[0m  2" + "(" + str(set_artist_add_name) + ")")
    if set == '3':
        set_download_lyric = not set_download_lyric
        print("歌曲是否下载歌词:" + "  \033[36m|\033[0m  2" + "(" + str(set_download_lyric) + ")")
    if set == '4':
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
    print("网易云歌手下载  \033[36m|\033[0m  6")
    print("歌曲下载项设置  \033[36m|\033[0m  7")
    mode = input("输入数字选择:   \033[36m|\033[0m  ")
    if mode == 'q' or mode == 'quit' or mode == 'exit': sys.exit()
    if mode == '1':
        print("=" * g_width, end='')
        id = input("请输入网易云单曲ID:")
        id = GetMusicID(id)
        if CheckIdFalse(id): continue
        api_path = "http://api.injahow.cn/meting/?type=song&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == "2":
        print("=" * g_width, end='')
        id = input("请输入网易云歌单ID:")
        id = GetMusicID(id)
        if CheckIdFalse(id): continue
        api_path = "http://api.injahow.cn/meting/?type=playlist&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == "3":
        print("=" * g_width, end='')
        id = input("请输入QQ音乐单曲ID:")
        id = GetMusicID(id)
        api_path = "http://api.injahow.cn/meting/?server=tencent&type=song&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == "4":
        print("=" * g_width, end='')
        id = input("请输入QQ音乐歌单ID:")
        id = GetMusicID(id)
        api_path = "http://api.injahow.cn/meting/?server=tencent&type=playlist&id=" + str(id)
        MusicMode(api_path, g_header, g_proxies, g_header163)
    if mode == '5':
        print("=" * g_width, end='')
        id = input("请输入专辑ID:")
        id = GetMusicID(id)
        if CheckIdFalse(id): continue
        api_path ="http://music.163.com/api/album/" + id + "?ext=true&id=" + id + "&offset=0&total=true&limit=10"
        AlbumMode(api_path, g_header, g_proxies, g_header163)
    if mode == '6':
        print("=" * g_width, end='')
        id = input("请输入歌手专辑页ID:")
        id = GetMusicID(id)
        if CheckIdFalse(id): continue
        album_list = ArtistAlbumList(id)
        for album in album_list:
            api_path ="http://music.163.com/api/album/" + str(album) + "?ext=true&id=" + str(album) + "&offset=0&total=true&limit=10"
            AlbumMode(api_path, g_header, g_proxies, g_header163)
    if mode == '7':
        print("=" * g_width, end='')
        Setting()
    print("=" * g_width, end='')
