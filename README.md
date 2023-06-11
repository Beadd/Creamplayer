<h1 align="center">EyeD3Music</h1>

<p align="center">
<img src="https://img.shields.io/github/last-commit/beadd/musicdownloader.svg?style=flat" alt="last commit">
<img src="https://img.shields.io/github/downloads/beadd/musicdownloader/total?style=flat" alt="downloads">
<img src="https://img.shields.io/github/v/release/beadd/musicdownloader?style=flat" alt="release">
<img src="https://img.shields.io/github/commit-activity/y/beadd/musicdownloader?style=flat" alt="commit activity">
<img src="https://img.shields.io/badge/license-MIT-blue.svg?longCache=true&style=flat" alt="license">
</p>

# Quick Start
## 1.  前往[releases](https://github.com/Beadd/MusicDownloader/releases)下载musicdownloader.exe
下载运行即可，若无法使用请使用下面其他方法

## 2.  命令行模式（需python环境）

```
git clone https://github.com/beadd/musicdownloader/
```
```
cd musicdownloader
```
```
pip install -r requirements.txt
```
```
python musicdownloader.py
```

## 3.  GUI版本（需python环境）

```
git clone -b dev-GUI https://github.com/beadd/musicdownloader/
```
```
cd musicdownloader
```
```
pip install -r requirements.txt
```
```
python EyeD3Music.py
```

# 高级使用
启动前加歌曲链接参数会直接下载，例子：
```
musicdownloader.py https://......song?id=...
musicdownloader.exe https://......playlist?id=...
```
启动前加参数-s {api server} 可直接更换歌曲[API服务器](https://github.com/injahow/meting-api)，例子：
```
musicdownloader.py -s https://example.com/metting/
musicdownloader.exe https://......song?id=... -s http://192.168.1.7/
```
> 能否下载歌曲或会员歌曲及其音质取决于API服务器
> 自建服务器并添加会员Cookie即可解析相关音乐以及无损

# 感谢 Thanks
- [Meting-api](https://github.com/injahow/meting-api)及本项目贡献者
<a href="https://github.com/beadd/musicdownloader/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=beadd/musicdownloader" />
</a>
