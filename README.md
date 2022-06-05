# 关于 About
识别ID自动调用API并分析json,填入ID自动批量下载,推荐自行下载PYTHON里的main.py运行,但用了requests,不想pip的可以去下载exe打包好的直接用,正在想办法能够下载付费或VIP歌曲以及其他平台,日后一定
- 歌单与单曲选择
- 输入ID自动获取识别json
- 自动创建文件夹并批量下载
- ID检测json检查
# 使用 How
1.  exe下载,前往[releases](https://github.com/Beadd/MusicDownloader/releases)直接下载使用,无法使用请用下面的方法
2.  注:需要requests库支持
```
pip install requests
```
下载zip文件进入
```bash
cd PYTHON
python MusicDownloader.py
```
所下载的文件对应目录,MusicB音频目录,LyricB歌词目录,想更改下载文件夹名可以分别更改全局变量里的MusicDirName和LyricDirName。

# 进度 Progress
还在深挖突破QQ音乐VIP的瓶颈,目前只能下载网易音乐VIP歌曲,如果你有任何的建议可以直接Issues！

- [x] 网易云音乐下载
- [x] 网易云歌单批量下载
- [x] 网易云会员VIP音乐下载
- [x] 网易云我喜欢的歌曲下载 
- [x] 网易云专辑下载
- [x] QQ音乐音乐下载
- [x] QQ音乐歌单批量下载
- [x] QQ音乐我喜欢的歌单下载
- [ ] 网易云歌手下载
- [ ] QQ音乐会员VIP下载
# 感谢 Thanks
- [meting-api](https://github.com/injahow/meting-api)
# 最后 Fine
感谢使用！欢迎issues催,会争取用更少的库,界面以后会用C++重写,欢迎Star！
