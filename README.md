<h1 align="center">🎵 Creamplayer</h1>

<p align="center">
<img src="https://img.shields.io/github/last-commit/beadd/musicdownloader.svg?style=flat" alt="last commit">
<img src="https://img.shields.io/github/downloads/beadd/musicdownloader/total?style=flat" alt="downloads">
<img src="https://img.shields.io/github/v/release/beadd/musicdownloader?style=flat" alt="release">
<img src="https://img.shields.io/github/commit-activity/y/beadd/musicdownloader?style=flat" alt="commit activity">
<img src="https://img.shields.io/badge/license-MIT-blue.svg?longCache=true&style=flat" alt="license">
</p>

<p align="center">
<a href="https://github.com/beadd/creamplayer/releases/latest"><img src="https://raw.githubusercontent.com/Beadd/MusicDownloader/main/images/download_github.png" alt="GitHub download" width=""></a>
</p>

# 💡 如何使用 Creamplayer Quick Start
前往[release](https://github.com/beadd/creamplayer/releases/latest)下载即可，但程序里没有任何提示，所以有必要查看此使用文档 There are no prompts in the program, so you need to check the usage documentation

### 首页 Home Page
- 输入框里输入歌曲名或id即可搜索 Enter the song name or id in the input box to search
- 输入框里输入歌曲或歌单链接即可批量下载 Enter the link in the input box to download
- 鼠标右键首页可切换皮肤 Right-click the home page to switch the theme
- 鼠标中键首页可切换暗黑模式 Middle mouse button home page can switch dark mode
![](https://raw.githubusercontent.com/Beadd/Creamplayer/main/images/home.png)

### 关于下载 About download
- 下载目录在程序目录的\downloads
- 默认最高音质 Highest sound quality by default
- 会内嵌封面、歌词、歌手、专辑、发行日期等元数据 Metadata such as covers, lyrics, artists, albums, and release dates are embedded
- 没有设置Cookie的情况下无法下载无损与VIP歌曲 Lossless and VIP songs cannot be downloaded without setting cookies
- 下载时会弹出提示框，里面的数字就是剩余的下载数量 When downloading, a prompt box will pop up, and the number inside is the remaining download quantity
- 数字变红代表下载失败了一首，会弹出下载失败的ID If the number turns red, the download failed. An ID indicating that the download failed is displayed
- 如果歌单多的话有时可能漏掉几首，下载完成后将下载的歌曲数量加下载失败的数量与歌单数量进行比对检查 If the song list is too many, sometimes may miss a few songs, you can compare the number of songs downloaded successfully and those that failed to download, in order to check if your playlist has been fully downloaded
- 如果下载数量不对，保留原先下载的歌曲文件，再次下载此歌单即可 If the number of downloads is not correct, keep the original downloaded song file and download this playlist again

### 搜索结果 Search result Page
- 鼠标单击封面即可进入播放界面 Click the cover to enter the playback interface
- 鼠标右击封面即可下载 Right-click the cover to download
- 鼠标单击空白地方即可返回 Click on a blank space to return
- 鼠标右击空白地方即可切换切换主题 Right-click on the blank area to switch the theme

### 播放界面 Play Page
- 默认最高音质 Highest sound quality by default
- 鼠标单击最左侧即可返回 Click on the far left to return
- 鼠标右键即可切换主题 Right-click to switch the theme

### 快捷键 Shortcut key
- `ctrl` + `shift` + `i` 开发者工具 Developer tools
- `ctrl` + `r` 刷新 Refresh
- `ctrl` + `+` / `ctrl` + `-` 放大缩小 Zoom in and zoom out
![](https://raw.githubusercontent.com/Beadd/Creamplayer/main/images/search.png)

### 如何设置Cookie How to set cookies
- 搜索一首VIP歌曲，进入该歌曲的播放界面即可设置Cookie Search for a VIP song and enter the playing screen of the song to set the Cookie

### 如何获取Cookie How to get cookies
- 在music.163.com里打开开发者模式 Open Developer tools in music.163.com
- 在network栏里找到music.163.com并复制其所有Cookie即可 Find music.163.com in the network and copy all of its cookies
![](https://raw.githubusercontent.com/Beadd/Creamplayer/main/images/cookie.png)

### 关于QQ音乐 About QQ music
- Creamplayer暂时无法下载qq音乐，你可以使用Release里本项目老版本musicdownloader Creamplayer is temporarily unable to download qq music, you can use the old version of this project: musicdownloader

# 🎨 如何贡献主题 Contribute theme
首页、搜索、播放三个界面每个对应一个vue文件，在[src/themes](https://github.com/Beadd/Creamplayer/tree/main/src/themes)里，将其他主题当作模板，修改里面的CSS即可自定义主题，然后创建对于的文件名即可 Home page, search page, play page, three interface, each corresponding to a vue file in [/SRC/themes](https://github.com/Beadd/Creamplayer/tree/main/src/themes), use other theme as a template, modify the CSS to customize the theme, and then create the appropriate file name

### 需要修改的文件 Files that need to be modified
- 修改上一个vue文件changeTheme函数，修改switch后面的数为新增的主题vue文件名(数字) Modify the last vue file changeTheme function, change the number after the "switch" to the new theme vue file name (number)
  ```
  function changeTheme() {
    emit('switch', 1)
  }
  ```
- 在对应的[views](https://github.com/Beadd/Creamplayer/tree/main/src/views)文件里引入新的主题vue文件，例如在Search页面里引入新的主题 import new themes to the corresponding [views](https://github.com/Beadd/Creamplayer/tree/main/src/views) vue file file
  ```
  import Theme16 from '../themes/search/16.vue';
  ...
  ...
  <Theme16 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 16"/>
  ```
- 将新主题的changeTheme函数后面的数字改为1，以进入循环 Change the number after the changeTheme function for the new theme to 1 to enter the loop

# ⚡ 开发环境搭建 Build development environment
开发环境里无法使用下载功能，使用下载功能请到release里下载发行包 The download function is not available in the development environment. To use the download function, please go to Release
```
git clone https://github.com/beadd/creamplayer
npm install
npm run electron:serve
```
