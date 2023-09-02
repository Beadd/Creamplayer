# 🎵 Creamplayer

<p>
<img src="https://img.shields.io/github/last-commit/beadd/musicdownloader.svg?style=flat" alt="last commit">
<img src="https://img.shields.io/github/downloads/beadd/musicdownloader/total?style=flat" alt="downloads">
<img src="https://img.shields.io/github/v/release/beadd/musicdownloader?style=flat" alt="release">
<img src="https://img.shields.io/github/commit-activity/y/beadd/musicdownloader?style=flat" alt="commit activity">
<img src="https://img.shields.io/badge/license-MIT-blue.svg?longCache=true&style=flat" alt="license">
</p>

# 💡 Quick Start
## [Windows客户端版本](https://github.com/beadd/creamplayer/releases)
- ✔ 网易云单曲下载
- ✔ 网易云歌单批量下载
- ✔ 网易云我喜欢的歌曲批量下载
- ✔ 支持无损与会员
- ✔ 下载的歌曲内嵌封面、歌词、歌手、专辑、发行日期等元数据

## [Python命令行老版本](https://github.com/Beadd/Creamplayer/releases/tag/v2.6.1)
- ✔ 网易云单曲下载
- ✔ 网易云歌单批量下载
- ✔ 网易云专辑批量下载
- ✔ 网易云歌手批量下载
- ✔ 网易云我喜欢的歌曲批量下载
- ✔ QQ音乐单曲下载
- ✔ QQ音乐歌单批量下载
- ✔ QQ音乐我喜欢的歌曲批量下载
- ✔ 支持无损与会员
- ✔ 下载的歌曲内嵌封面、歌词、歌手、专辑、发行日期等元数据

## [服务器版本](https://github.com/Beadd/Creamplayer/tree/server)
- ✔ 网易云单曲下载
- ✔ 支持无损与会员

# 📖 使用文档

### 关于下载
- **下载的音乐在程序目录的\downloads里**
- 如果下载数量不对，再次下载即可

### 首页
- 右键首页切换皮肤
- 中键首页切换暗黑模式
![](https://raw.githubusercontent.com/Beadd/Creamplayer/main/images/home.png)


### 结果页面
- **右击歌曲封面即可下载该歌曲**
- 单击空白返回
- 右击空白切换主题

### 播放界面
- 单击最左侧返回
- 右键切换主题

### 快捷键
- `ctrl` + `shift` + `i` 开发者工具
- `ctrl` + `r` 刷新
- `ctrl` + `+` / `ctrl` + `-` 放大缩小
![](https://raw.githubusercontent.com/Beadd/Creamplayer/main/images/search.png)

### 如何设置Cookie 
- 搜索一首VIP歌曲，进入该歌曲的播放界面即可设置

### 如何获取Cookie 
- 在music.163.com里打开开发者模式
- 在network栏里找到music.163.com并复制其所有Cookie即可
![](https://raw.githubusercontent.com/Beadd/Creamplayer/main/images/cookie.png)

### 关于QQ音乐
- Creamplayer暂时无法下载qq音乐，你可以使用Release里本项目老版本[musicdownloader](https://github.com/Beadd/Creamplayer/releases/tag/v2.6.1)

# 🎨 如何修改主题 Contribute theme
首页、搜索、播放三个界面每个对应一个vue文件，在[src/themes](https://github.com/Beadd/Creamplayer/tree/main/src/themes)里，将其他主题当作模板，修改里面的CSS即可自定义主题，然后创建对于的文件名即可 
### 需要修改的文件
- 修改上一个vue文件changeTheme函数，修改switch后面的数为新增的主题vue文件名(数字)
  ```
  function changeTheme() {
    emit('switch', 1)
  }
  ```
- 在对应的[views](https://github.com/Beadd/Creamplayer/tree/main/src/views)文件里引入新的主题vue文件，例如在Search页面里引入新的主题
  ```
  import Theme16 from '../themes/search/16.vue';
  ...
  ...
  <Theme16 :q="q" @switch="switchTheme" @return="returnHome" v-if="searchTheme == 16"/>
  ```
- 将新主题的changeTheme函数后面的数字改为1，以进入循环

# ⚡ 开发环境搭建
开发环境里无法使用下载功能，使用下载功能请到release里下载发行包，或者手动打包musicdownloader.py为exe放置当前目录里
```
git clone https://github.com/beadd/creamplayer
npm install
npm run electron:serve
```
