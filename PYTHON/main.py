import json
from traceback import print_tb
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
    counter = 1
    #    file = open(path, encoding="utf-8")
    #    data = json.load(file)
    with urlopen(path) as response:
        source = response.read()
    data = json.loads(source)
    if 'error' in data:
        print("ID有错误!请检查")
        os.system("pause")
        os._exit(1)

    # start
    os.system("mkdir MusicB")
    for data in data:
        os.system("cls")
        print( str(counter) + ' ' + data['name'])
        name = data['name']
        for i in string:
            if i in name:
                name = "NameFalseNo." + str(counter)
        name_url = "MusicB/" + name + ".mp3"
        url = data['url']
        req = requests.get(url)
        with open(name_url, "wb") as code:
            code.write(req.content)
        counter += 1


def Lyric():
    counter = 1
    #    file = open(path, encoding="utf-8")
    #    data = json.load(file)
    with urlopen(path) as response:
        source = response.read()
    data = json.loads(source)

    # start
    os.system("mkdir LyricB")
    for data in data:
        os.system("cls")
        print( str(counter) + ' ' + data['name'])
        name = data['name']
        for i in string:
            if i in name:
                name = "NameFalseNo." + str(counter)
        name_url = "LyricB/" + name + ".lrc"
        url = data['lrc']
        req = requests.get(url)
        with open(name_url, "wb") as code:
            code.write(req.content)
        counter += 1


while True:
    Start()
    print("开始下载歌曲")
    Music()
    print("歌曲下载完成!是否下载歌词?\n取消请直接关闭窗口")
    os.system("pause")
    Lyric()
    print("下载完成!感谢使用!\n继续再次选择下载\n")
    os.system("pause")
