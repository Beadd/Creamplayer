<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '../api'
import { getSongLyricsApi, formatTimestamp } from '../api'

const router = useRouter()
const props = defineProps({
  songid: [String, Number],
  title: [String, Number],
  artist: [String, Number],
  album: [String, Number],
  cover: [String, Number],
  publishTime: [String, Number],
  autoFont: Boolean,
  blurCover: Boolean,
})
const song = reactive({
  id: '',
  title: '',
  artist: '',
  album: '',
  cover: '',
  publishTime: '',
})

async function loadSong(songid) {
  try {
    const songGet = api.loadSongDetails(songid)
    song.id = songGet.id
    song.title = songGet.title
    song.artist = songGet.artist
    song.album = songGet.album
    song.cover = songGet.cover
    song.publishTime = songGet.publishTime
  } catch (error) {
    console.error('API request failed:', error);
    setTimeout(() => {
      api.loadSongDetails(songid);
    }, 777);
  }
}

if (props.title && props.artist && props.cover) {
  song.id = props.songid;
  song.title = props.title;
  song.artist = props.artist;
  song.album = props.album;
  song.cover = props.cover;
  song.publishTime = formatTimestamp(props.publishTime);
} else {
  loadSong(props.songid);
  console.log("loadSong");
}

async function downloadSong(event) {
  console.log('Downloading')
  event.stopPropagation();

  let songUrl
  try {
    await api.getSongUrl(song.id).then(res => {
      songUrl = res['data'][0]['url']
    })
  } catch (error) {
    console.error('Get Song URL fail:', error);
    songUrl = 0
  }
  console.log(songUrl)
  
  api.downloadSongFile('netease',
                       songUrl, 
                       song.cover, 
                       getSongLyricsApi(song.id),
                       song.id, 
                       song.title, 
                       song.artist, 
                       song.album, 
                       song.publishTime)
}

function playSong(event) {
  event.stopPropagation()
  router.push({
    name: 'play',
    params: {
      songid: song.id,
      title: song.title,
      artist: song.artist,
      album: song.album,
      cover: song.cover,
      publishTime: song.publishTime,
    }  
  })
}

function getFontSize(text) {
  if(!text) return '10px'
  if(/^\s+$/.test(text)) {
    return '10px'; 
  }

  const maxWidth = '180px'
  let size = 10
  while(true) { 
    const fontSize = String(size) + 'px'
    const result = willTextWrap(text, fontSize, maxWidth)
    if (result) {
      return String(size - 5) + 'px'
    } else {
      size+=5
    }
  }
}

function willTextWrap(text, fontSize, maxWidth) {
  const testEl = document.createElement('div');
  testEl.style.fontSize = fontSize;
  testEl.style.maxWidth = maxWidth;
  testEl.innerText = text;
  testEl.style.fontFamily = "consolas";
  testEl.style.overflowWrap = 'anywhere';
  testEl.style.whiteSpace = 'pre';
  document.body.appendChild(testEl);
  const isWrapped = testEl.scrollWidth > testEl.clientWidth;
  document.body.removeChild(testEl);
  return isWrapped;
}
</script>
<template>
  <div class="song-container">
    <div class="song-cover" @contextmenu.prevent="downloadSong" @click="playSong">
      <img class="song-cover-img" :src="song.cover"/>
    </div>
    <div v-if="blurCover === true" class="song-cover-blur" :style="{backgroundImage: 'url(' + song.cover + ')'}"></div>
    <div class="song-id">{{ song.id }}</div>
    <div v-if="autoFont === true" class="song-title" :style="{fontSize: getFontSize(song.title)}">{{ song.title }}</div>
    <div v-else class="song-title">{{ song.title }}<span class="song-title-artist" style="display: none;"> - {{ song.artist }}</span>
      <span class="song-title-album" style="display: none;"> &lt;{{ song.album }}&gt;</span></div>
    <div class="song-artist">{{ song.artist }}</div>
    <div class="song-album">{{ song.album }}</div>
    <div class="song-publish-time">{{ song.publishTime }}</div>
  </div>
</template>