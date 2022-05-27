import json
import requests
import os

from urllib.request import urlopen

string = "\/:*?\">|"
path = "path"
def Start():
    global path
    print("C Beadd\n")
    print("歌曲自动下载至当前目录MusicB中\n歌词自动下载至当前目录LyricB中\n")
    mode = input("下载网易云单曲\t1\n下载网易云歌单\t2\n输入数字选择:\t")
    if mode == "1":
        os.system("cls")
        id = input("请输入单曲ID:")
        path = "https://api.injahow.cn/meting/?type=song&id=" + str(id)
    else:
        os.system("cls")
        id = input("请输入歌单ID:")
        path = "https://api.injahow.cn/meting/?type=playlist&id=" + str(id)

def Music():
    os.system("mkdir MusicB")
    counter = 1
#    file = open(path, encoding="utf-8")
#    data = json.load(file)
    with urlopen(path) as response:
        source = response.read()

    data = json.loads(source)
    for data in data:
        os.system("cls")
        print(counter)

        print(data['name'])
        name = data['name']
        for i in string:
            if i in name:
                name = "NameFalseNo." + str(counter)
        
        name_url = "MusicB/" + name + ".mp3"
        url = data['url']
        req = requests.get(url, verify=False)
        with open(name_url, "wb") as code:
            code.write(req.content)
        counter += 1

def Lyric():
    os.system("mkdir LyricB")
    counter = 1
#    file = open(path, encoding="utf-8")
#    data = json.load(file)
    with urlopen(path) as response:
        source = response.read()

    data = json.loads(source)
    for data in data:
        os.system("cls")
        print(counter)
        print(data['name'])
        name = data['name']
        for i in string:
            if i in name:
                name = "NameFalseNo." + str(counter)
        
        name_url = "LyricB/" + name + ".lrc"
        url = data['lrc']
        req = requests.get(url, verify=False)
        with open(name_url, "wb") as code:
            code.write(req.content)
        counter += 1


Start()
print("开始下载歌曲")
Music()
print("歌曲下载完成!是否下载歌词?\n")
os.system("pause")
Lyric()
print("下载完成!感谢使用!\n")
os.system("pause")
