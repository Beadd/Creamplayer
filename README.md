# 关于 About
一键批量下载网易云/QQ歌单歌曲工具
<br><br>
<img src="https://img.shields.io/badge/license-MIT-blue.svg?longCache=true&style=flat-square" alt="license">
<img src="https://img.shields.io/github/last-commit/beadd/musicdownloader.svg?style=flat-square" alt="last commit">
<img src="https://img.shields.io/github/downloads/beadd/musicdownloader/total?style=flat-square" alt="downloads">
<img src="https://img.shields.io/github/v/release/beadd/musicdownloader?style=flat-square" alt="release">
<img src="https://img.shields.io/github/commit-activity/y/beadd/musicdownloader?style=flat-square" alt="commit activity">
<br>
<img src="https://img.shields.io/github/issues/beadd/musicdownloader?style=flat-square" alt="issues">
<img src="https://img.shields.io/github/issues-closed-raw/beadd/musicdownloader?style=flat-square" alt="closed issues">
<img src="https://img.shields.io/github/forks/beadd/musicdownloader?style=flat-square" alt="forks">
<img src="https://img.shields.io/github/stars/beadd/musicdownloader?style=flat-square" alt="stars">
<img src="https://img.shields.io/github/watchers/beadd/musicdownloader?style=flat-square" alt="watchers">

# 使用 How
## 1.  前往[releases](https://github.com/Beadd/MusicDownloader/releases)下载MusicDownloader.exe
下载运行即可,包含eyed3,无需pip,若无法使用请用下面的方法


## 2.  前往[releases](https://github.com/Beadd/MusicDownloader/releases)下载MusicDownloader.py

```
pip install -r requirements.txt
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

# 感谢 Thanks
- [Meting-api](https://github.com/injahow/meting-api)
## 贡献者 Contributors
<a href="https://github.com/beadd/musicdownloader/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=beadd/musicdownloader" />
</a>
