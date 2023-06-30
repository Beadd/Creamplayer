<h1 align="center">🎵 EyeD3Music</h1>

<p align="center">
<img src="https://img.shields.io/github/last-commit/beadd/musicdownloader.svg?style=flat" alt="last commit">
<img src="https://img.shields.io/github/downloads/beadd/musicdownloader/total?style=flat" alt="downloads">
<img src="https://img.shields.io/github/v/release/beadd/musicdownloader?style=flat" alt="release">
<img src="https://img.shields.io/github/commit-activity/y/beadd/musicdownloader?style=flat" alt="commit activity">
<img src="https://img.shields.io/badge/license-MIT-blue.svg?longCache=true&style=flat" alt="license">
</p>

<p align="center">
<a href="https://github.com/beadd/musicdownloader/releases/latest"><img src="https://raw.githubusercontent.com/Beadd/MusicDownloader/main/images/download_github.png" alt="GitHub download" width=""></a>
</p>

> Netease music and QQ music download tools

# 👉 Quick Start
```
# you can run EyeD3Music.py to start GUI mode
git clone https://github.com/beadd/musicdownloader/
cd musicdownloader
pip install -r requirements.txt
python EyeD3Music.py
# you can also run musicdownloader.py to start the command line mode
```

# ✨ More Usage
Adding``` song URL ```parameters before startup will download directly, for example:

```
musicdownloader.py https://......song?id=...
musicdownloader.exe https://......playlist?id=...
```

Start to add parameters``` -s {server API} ```can directly replace the song [API server](https://github.com/injahow/meting-api), example:

```
musicdownloader.py -s https://example.com/metting/
musicdownloader.exe https://......song?id=... -s http://192.168.1.7/
```

> The ability to download VIP songs and their sound quality depends on the API server.
> You can build your server and add your VIP cookies to get VIP music, this code can't get VIP music.

# 🍰 Thanks
- [Meting-api](https://github.com/injahow/meting-api) and this project contributor
<a href="https://github.com/beadd/musicdownloader/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=beadd/musicdownloader" />
</a>
