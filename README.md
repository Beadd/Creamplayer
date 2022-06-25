# 关于下载 About
识别ID自动调用API分析json进行下载,推荐自行下载MusicDownloader.py运行,用了requests,不想pip的可以去下载exe打包好的直接用,正在想办法能够下载付费或VIP歌曲以及其他平台,日后一定。然后如果你有任何的建议或者其他好用的API可以直接Issues或者pr,欢迎Star！

# 简单使用 Simply use
### 1.  exe下载,前往[releases](https://github.com/Beadd/MusicDownloader/releases)直接下载使用包括EyeD3,若无法使用请用下面的方法
### 2.  前往[releases](https://github.com/Beadd/MusicDownloader/releases)下载MusicDownloader.py需要requests库支持
```
pip install requests
```

注:EyeD3的为有对歌曲添加元数据的版本,需要再安装EyeD3库。想更改下载文件夹名可以分别更改全局变量里的MusicDirName和LyricDirName,默认在同一文件夹MusicB里。
```
pip install eyeD3
```
```bash
python MusicDownloader.py
```

# 目前进度 Progress
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

## 关于EyeD3
- [x] 歌曲封面图片元
- [x] 歌曲专辑ID元
- [x] 歌曲名称元(标题)
- [x] 歌曲歌手元(参与创作的艺术家)

# 感谢 Thanks
- [meting-api](https://github.com/injahow/meting-api)
# 许可证 License
[MIT](https://github.com/Beadd/MusicDownloader/blob/main/LICENSE) license.
# 最后 Fine
感谢使用！

# 一些建议 XiaoShengBiBi
## 关于QQ音乐ID
> 比如这个ID为003eZ03f3yrLl5
> ![avatar](./QQmusicID.png)

## QQ音乐等多平台VIP歌曲下载解决方案
只要是在网页上你能听见的能播放全的未加密的,任何平台此方法都适用
![avatar](./QQvipDownload.png)
1.  按F12或Ctrl+Shift+I打开开发者模式
2.  选择网络(Network)
3.  (打开过滤选项,)选择媒体(media)
4.  刷新网页,播放音频,出现选项(QQ音乐会在未播放前就缓存歌曲)
5.  选中其中一个,在右侧选择headers
6.  复制其中的Request URL
7.  在浏览器打开复制的URL即是音频
- (注意看时间,如果第3步有很多选项注意都看一遍)
- (下载的前提是能播放歌曲,网易云酷狗酷我等各平台同理)
```
  __  __           _      _____                      _                 _           
 |  \/  |         (_)    |  __ \                    | |               | |          
 | \  / |_   _ ___ _  ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 | |\/| | | | / __| |/ __| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |  | | |_| \__ \ | (__| |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |_|  |_|\__,_|___/_|\___|_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
```
