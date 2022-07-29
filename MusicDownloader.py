# coding:UTF-8


import os
import re
import sys
import json
import time
import requests
'''
eyed3
'''
eyed3exist=True
try:
    import eyed3
except ImportError:
    eyed3exist=False
'''
alright eyed3
'''
mode = 0
path = "path"
string = "\/:*?\">|"
LyricDirName = 'MusicB'#'LyricB'
MusicDirName = 'MusicB'
width = os.get_terminal_size().columns

proxiesB = {"http": None, "https": None}
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    #,'cookie':
}
header163 = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    ,
    #'cookie':'NMTID=00O-UfVMage_XYVb01NofLYtGWN81wAAAGA6ROCHA; _ntes_nnid=0026f9a21f511bc7b813bc8257738ed7,1653178475744; _ntes_nuid=0026f9a21f511bc7b813bc8257738ed7; WNMCID=uzisge.1653178476562.01.0; WEVNSM=1.0.0; WM_TID=%2F8H5Vyp5GQxFUQERQRbFEfFcaI581rZl; _iuqxldmzr_=32; WM_NI=PvUHSZ6ODGORWadg5DK7d9SzSwgDNsEV3JehG9upEAJGRraJCFze%2B3Ix2YL4zAo9ukl3%2FPe2aI2kTlTFY9G%2Fgxu6Au7OWvM7p%2BiGGmIwnpbjRkJw9a7fOaUYlUq%2FU88eNlU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed1bc47b5efc0a7c46e95868aa2d84a939b9ab1c54ebced8cd9aa3baeb8bbaff02af0fea7c3b92a94aa9ba9d252f6918ca8ce5a95bfac88b85089e9acdad27291a9a9a5cd79878afdabe86485e7bb91c84b8a999e93e442819ab686aa398ba8febacf40ba9fa1daf861b0ede1b1e83aa397fe8cd768989a97dac625a5a8bbd7c47ff5919997d03db4f5a7a8c6678ba9a291e16292b58698bc6bf5ba8182d853b08bbfd0d834fcbb828dd837e2a3; JSESSIONID-WYYY=bTf0dAu0K3KzvcZDWFId0KCqJfkUUz%2Fnld6U6IhcZ2GBcGnbR%2B6P54Ex4sP%2B5aXIjrwtEDDyIaj%2FG5RM7gozKnk0%5C2cGnPn%2FtobEaEbkoGMTgAWXBWwzoWBkF5k3z1HSWb%5CND2rHARn0Ap7A85W7B%2BQ0D4DO5%2F%2F8Q3%2BjH0mjM%2B9%5CF%2FCq%3A1654302417314'
    'cookie':'JSESSIONID-WYYY=MqngSDeeeN%2FZRbE7Vmz7zZ1g9U3fs5SAD%5CbS23A0eW%2FhqzUHpYMX9jVlVgPosnC5wJdYO7se20QsYn45DoJor%5Cskxna6I%5CQKW733yxHugKPmYvN%2FP0%2BQOpOwkZJumC6t0QCh9rdwbk06t4TnjlMg%2Fa5Ooj1CW4idEdZq4VBMsDsIEhM3%3A1654304708419; _iuqxldmzr_=32; _ntes_nnid=59c0c0c4fc69665b6261b45f5e44fe4a,1654302908431; _ntes_nuid=59c0c0c4fc69665b6261b45f5e44fe4a; NMTID=00O-D3f-9XeBnQh0Ei2qy1d-ULEVSUAAAGBLCI6vA; WEVNSM=1.0.0; WNMCID=tqqzib.1654302908799.01.0; WM_NI=EROpEfsIky5J3M1%2F2Uw0BlLsOXn0anY7%2BSg1r8Y7PB%2B37llD5L2xuZ6sKBgI7WCTj5wOcXoIPycPEUR6dtcJmPPozE646Hv2qifgkQ76N5QKrDtVgERuCcCub6j65tgtVTU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeafdb6aa79efbd5ed6383928eb7d44e878e8e82d54bf4b2a9a5d16da7aba6d6c52af0fea7c3b92a878e8191c86eb197a59ab842f193ffd0b15fb5f08e8dcf798d88a2d1e4669be9e5b4e63bb2e897d8d34ae9edf98def50f794fe99f852f6ad85a3e643f5898db5e93fb591adb9ee4394a7adb1c85f92eaac95e242af90a090f94ff6ecfaa9f53ab3b7aa88ea5bf5ea82d6d441b29cbcb7e64f92ab8d84c27fa2eaa6d7b880a5ac9ab5d837e2a3; WM_TID=Pc31v8zNG7tFVRUUQAKVUgm1GFke%2Fj9Q'
}



def Start():
    global path
    global mode
    if mode == 'q' or mode =='quit':
        exit()
    if mode == "1":
        # os.system("cls")
        print("="*width)
        id = input("请输入网易云单曲ID:")
        if id.isdigit() == 0:
            return -1
        path = "http://api.injahow.cn/meting/?type=song&id=" + str(id)
        return 1
    if mode == "2":
        # os.system("cls")
        print("="*width)
        id = input("请输入网易云歌单ID:")
        if id.isdigit() == 0:
            return -1
        path = "http://api.injahow.cn/meting/?type=playlist&id=" + str(id)
        return 1
    if mode == "3":
        # os.system("cls")
        print("="*width)
        id = input("请输入QQ音乐单曲ID:")
        #if id.digit() == 0:
        #    return -1
        path = "http://api.injahow.cn/meting/?server=tencent&type=song&id=" + str(id)
        return 1
    if mode == "4":
        # os.system("cls")
        print("="*width)
        id = input("请输入QQ音乐歌单ID:")
        #if id.digit() == 0:
        #    return -1
        path = "http://api.injahow.cn/meting/?server=tencent&type=playlist&id=" + str(id)
        return 1
    if mode == '5':
        # os.system("cls")
        print("="*width)
        Album()
        #return 5
    else:
        return 0

    
def Music():
    counter = 1
    # file = open(path, encoding="utf-8")# data = json.load(file)#  with urlopen(path) as response:#    source = response.read()
    """source == response"""
    response = requests.get(path, headers=header, proxies=proxiesB)
    data = json.loads(response.text)
    if 'error' in data:
        return 0
    # start
    if (os.path.exists(MusicDirName) == False):
        os.makedirs(MusicDirName)
    # download
    for data in data:
        # os.system("cls")
        print(str(counter) + ' ' + data['name'] + '...')
        name = data['name']
        for i in string:
            if i in name:
                name = "NameFalseNo." + str(counter)
        name_url = MusicDirName + "/" + name + ".mp3"
        url = data['url']
        req = requests.get(url)
        if req.content == None:
            print("\n\033[33m返回为空,自动跳过,不做统计\033[0m\n",end="")
            continue
        with open(name_url, "wb") as code:
            code.write(req.content)
        #download Lyric
        req_lyric = requests.get(data['lrc'], headers=header, proxies=proxiesB)
        if eyed3exist == False and req_lyric.text != '':
            print('  歌词已保存至lrc',end="")
            if (os.path.exists(LyricDirName) == False):
                os.makedirs(LyricDirName)
            lrc_Name_Url  = LyricDirName + "/" + name + ".lrc"
            with open(lrc_Name_Url, "wb") as code:
                code.write(req_lyric.content)
        if req_lyric.text == '':
            print("\n\033[33m序号"+str(counter)+"歌曲歌词为空\033[0m")
        '''
        eyed3
        '''
        if eyed3exist:
            try:
                audiofile = eyed3.load(name_url)
            except:
                print("\n\033[33m打开序号"+str(counter)+"音乐失败,自动跳过\033[0m")
                continue
            #artist
            if data['artist'] != 'NoneType':
                audiofile.tag.artist = data['artist']
                print("  已内嵌歌手",end="")
            #title
            if data['name'] != None:
                audiofile.tag.title = data['name']
                print("  已内嵌名称",end="")
            #image
            if data['pic'] != None:
                audio_Image = requests.get(data['pic'])
                if (os.path.exists(MusicDirName) == False):
                    os.makedirs(MusicDirName)
                with open(MusicDirName+"/pic.jpg", "wb") as code:
                    code.write(audio_Image.content)
                imageDate = open(MusicDirName+"/pic.jpg", "rb").read()
                audiofile.tag.images.set(3, imageDate, "image/jpeg")
                print("  已内嵌封面",end="")
                #delete pic
                if (os.path.exists(MusicDirName+"/pic.jpg") != False):
                    os.remove("./"+MusicDirName+"/pic.jpg")
            #lyrics
            if req_lyric.text != '':
                audiofile.tag.lyrics.set(req_lyric.text)
                print("  已内嵌歌词",end="")
            else:
                print("\n\033[33m歌词为空,eyed3嵌入失败,自动跳过\033[0m")
            #API in not have album 
            #   audiofile.tag.album = data['album']
            if data['name'] != None:
                audiofile.tag.save(encoding='utf-8')
            #save alright
        '''
        alright eyed3
        '''
        print('\n'+'-'*50)
        counter += 1


def MusicLyricDownload(M_id,M_albumId,M_header,M_proxies):
    #url = 'https://api.injahow.cn/meting/?type=url&id=' + str(M_id)
    #req = requests.get(url)
    M_path = 'https://api.injahow.cn/meting/?type=song&id=' + str(M_id)
    response = requests.get(M_path,headers=header163,proxies=proxiesB)
    data1 = json.loads(response.text)
    name = data1[0]['name']
    for i in string:
        if i in name:
            name = "NameFalseId." + str(M_id)
    name_url = MusicDirName + "/" + name + ".mp3"
    url = data1[0]['url']
    req = requests.get(url,proxies=proxiesB)
    if (os.path.exists(MusicDirName) == False):
        os.makedirs(MusicDirName)
    with open(name_url, "wb") as code:
        code.write(req.content)
    url_lyric = data1[0]['lrc']
    req_lyric = requests.get(url_lyric)
    lrc_Name_Url = LyricDirName + "/" + data1[0]['name'] + ".lrc"
    with open(lrc_Name_Url, "wb") as code:
        code.write(req_lyric.content)
    print("\n\033[32m歌词下载完成\033[0m")

    '''
    eyed3
    '''
    if eyed3exist:
        try:
            audiofile = eyed3.load(name_url)
        except:
            print("\n\033[33m打开音乐失败,自动跳过\033[0m")
            return 0
        #歌手
        if data1[0]['artist'] != 'NoneType':
            audiofile.tag.artist = data1[0]['artist']
        #曲名
        if data1[0]['name'] != None:
            audiofile.tag.title = data1[0]['name']
        #封面
        if data1[0]['pic'] != None:
            audio_Image = requests.get(data1[0]['pic'])
            if (os.path.exists(MusicDirName) == False):
                os.makedirs(MusicDirName)
            with open(MusicDirName+"/pic.jpg", "wb") as code:
                code.write(audio_Image.content)
            imageDate = open(MusicDirName+"/pic.jpg", "rb").read()
            audiofile.tag.images.set(3, imageDate, "image/jpeg")
            #delete pic
            if (os.path.exists(MusicDirName+"/pic.jpg") != False):
                os.remove("./"+MusicDirName+"/pic.jpg")
        #歌词
        if req_lyric.text != '':
            audiofile.tag.lyrics.set(req_lyric.text)
            print("  正在将歌词嵌入歌曲中",end="")
        else:
            print("\n\033[33m歌词为空,eyed3嵌入失败,自动跳过\033[0m")
        #专辑
        audiofile.tag.album = str(M_albumId)
        if data1[0]['name'] != None:
            audiofile.tag.save(encoding='utf-8')
    '''
    alright eyed3
    '''


def Album():
    albumId = input("请输入专辑ID:")
    u163API ="http://music.163.com/api/album/"+albumId+"?ext=true&id="+albumId+"&offset=0&total=true&limit=10"
    response = requests.get(u163API, headers=header163, proxies=proxiesB)
    data = json.loads(response.text)
    if data['code'] != 200:
        if(os.path.exists('logB') == False):
            os.makedirs("logB")
        fileName = "logB/" + str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))) + ".log"
        with open(fileName, "wb") as code:
            code.write(response.content)
        print("API调用失败:cookie失效或其他问题,自动将调用日志保存在logB文件夹中")
        # os.system("pause")
        sys.exit(0)
    num = data['album']['size']
    for i in range(0,num):
        print(str(i+1) +" "+ data['album']['songs'][i]['name'] +" "+"下载完成")
        MusicLyricDownload(data['album']['songs'][i]['id'],albumId,header163,proxiesB)
    print("\n\033[32m专辑下载完成,下载至 "+MusicDirName+" \033[0m")


print('''
\033[34m  __  __           _     \033[35m _____                      _                 _           \033[0m
\033[34m |  \/  |         (_)    \033[35m|  __ \                    | |               | |          \033[0m
\033[34m | \  / |_   _ ___ _  ___\033[35m| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ \033[0m
\033[34m | |\/| | | | / __| |/ __\033[35m| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|\033[0m
\033[34m | |  | | |_| \__ \ | (__\033[35m| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   \033[0m
\033[34m |_|  |_|\__,_|___/_|\___\033[35m|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   \033[0m
''')
print("="*width)
print("歌曲自动下载至目录"+MusicDirName+"中\n歌词自动下载至目录"+LyricDirName+"中")
if eyed3exist:
    print("eyeD3已启用")
else:
    print("eyeD3未启用")
print("="*width)
while True:
    if mode == 0:
        print("下载网易云单曲  \033[36m|\033[0m  1")
        print("下载网易云歌单  \033[36m|\033[0m  2")
        print("下载QQ音乐单曲  \033[36m|\033[0m  3")
        print("下载QQ音乐歌单  \033[36m|\033[0m  4")
        print("下载网易云专辑  \033[36m|\033[0m  5")
        mode = input("输入数字选择:   \033[36m|\033[0m  ")
    start = Start()
    if start != 0:
        print("="*width)
        print("\033[32m开始下载歌曲\033[0m")
    if start == -1:
        mode = 0
        # os.system("cls")
        print("="*width)
        print("\033[33m请输入合法ID!\033[0m")
        continue
    if start == 0:
        mode = 0
        # os.system("cls")
        print("="*width)
        print("\033[33m请输入正确数字!\033[0m")
        continue
    if start == 1:
        if Music() == 0:
            print("="*width)
            print("\033[33mID有错误!请检查\033[0m")
        else:
            print("="*width)
            print("\033[32m下载完成!感谢使用!\n\033[35m请直接关闭窗口或继续\033[0m")
            print("="*width)

