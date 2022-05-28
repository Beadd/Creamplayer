import json
from traceback import print_tb
import requests
import os

from urllib.request import urlopen

string = "\/:*?\">|"
path = "path"
mode = 0

def Start():
    global path
    global mode
    if mode == "1":
        os.system("cls")
        id = input("请输入网易云单曲ID:")
        path = "http://api.injahow.cn/meting/?type=song&id=" + str(id)
    if mode == "2":
        os.system("cls")
        id = input("请输入网易云歌单ID:")
        path = "http://api.injahow.cn/meting/?type=playlist&id=" + str(id)
    if mode == "3":
        os.system("cls")
        id = input("请输入QQ音乐歌单ID:")
        path = "http://api.injahow.cn/meting/?server=tencent&type=playlist&id=" + str(id)
    else:
        return 0
def Music():
    counter = 1
    #    file = open(path, encoding="utf-8")
    #    data = json.load(file)
    with urlopen(path) as response:
        source = response.read()
    data = json.loads(source)
    if 'error' in data:
        return 0;

    # start
    os.system("mkdir MusicB")
    for data in data:
        # os.system("cls")
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
        # os.system("cls")
        print( str(counter) + ' ' + data['name'] + '(歌词)')
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

print("C Beadd")
print("歌曲自动下载至当前目录MusicB中\n歌词自动下载至当前目录LyricB中\n")
while True:
    if mode == 0:
        print("下载网易云单曲\t1")
        print("下载网易云歌单\t2")
        print("下载QQ音乐歌单\t3")
        mode = input("输入数字选择:\t")
    if Start() == 0:
        mode == 0
        print("请输入正确数字")
    else:
        print("开始下载歌曲")
        if Music() == 0:
            print("ID有错误!请检查")
            os.system("pause")
        # print("歌曲下载完成!是否下载歌词?\n取消请直接关闭窗口")
        # os.system("pause")
        else:
            Lyric()
            print("下载完成!感谢使用!\n请直接关闭窗口或继续\n")
            os.system("pause")
