<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

import api from '../api'
import { useCounterStore } from '../stores/counter.js'
import { initTheme, updateTheme, setCookie } from '../useDB/setting.js'

// Add Theme Here
import Theme1 from '../themes/play/1.vue';

const router = useRouter()

const props = defineProps({
  songid: [String, Number],
  title: [String, Number],
  artist: [String, Number],
  album: [String, Number],
  cover: [String, Number],
  publishTime: [String, Number],
})
console.log(props)

const playTheme = ref(1) 
const darkTheme = ref(false)

const database = 'CreamPlayer'
const store = 'Setting'
const settingKey = 'playTheme'
const settingDark = 'darkTheme'

const songUrl = ref('')
const songLyrics = ref([])
const audio = ref(null)
const currentHighlight = ref(0)
const isVip = ref(false)

const counterStore = useCounterStore()

const q = counterStore.lastSearch
console.log(q)
function returnSearch() {
  router.push({
    name: 'search',
    params: {
      q: q
    }  
  })
}

function processLyricsTime(lrc) {
  const lyrics = lrc.split('\n')
  const regex = /\[(\d{2}):(\d{2})\.?(\d{2,3})?\](.*)/ 
  return lyrics.map(line => {
    const matches = regex.exec(line)
    if (matches) {
      const min = matches[1]
      const sec = matches[2]
      const msec = ('0.' + matches[3]) || '0'
      const time = parseInt(min) * 60 + parseFloat(sec) + parseFloat(msec)
      // console.log(min, sec, msec, time, matches[4])
      return {
        time,
        text: matches[4]  
      } 
    } else if (line != '') {
      return {
        time: 777404,
        text: line
      }
    }
    return line
  })
}

function audioControl(event) {
  if(event.key === ' ') {
    event.preventDefault();
    if(audio.value.paused) {
      audio.value.play() 
    } else {
      audio.value.pause()
    }
  } else if(event.key === 'ArrowUp') {
    event.preventDefault();
    counterStore.increaseVolume()
    audio.value.volume = counterStore.volume
    console.log(counterStore.volume)
  } else if(event.key === 'ArrowDown') {
    event.preventDefault();
    counterStore.decreaseVolume()
    audio.value.volume = counterStore.volume
    console.log(counterStore.volume)
  } else if(event.key === 'ArrowLeft') {
    audio.value.currentTime -= 3;
  } else if(event.key === 'ArrowRight') { 
    audio.value.currentTime += 3;
  }
}
console.log(counterStore.volume)

onMounted(async () => {
  initTheme(database, store, settingKey, playTheme);
  await initTheme(database, store, settingDark, darkTheme);
  if (darkTheme.value && !document.body.classList.contains('dark')) {
    document.body.classList.toggle('dark');
  }

  api.getSongUrl(props.songid).then(res => {
    try {
      songUrl.value = res['data'][0]['url']
      if (!songUrl.value) throw new Error
    } catch (error) {
      console.log('fail load song url')
      isVip.value = true
    }
  })
  api.getSongLyrics(props.songid).then(res => {
    const lyrics = processLyricsTime(res.lrc.lyric)
    if (lyrics[0].time == null) { 
      songLyrics.value = [{ time: 0, text: lyrics}]
    } else {
      songLyrics.value = lyrics
    }
  })

  window.addEventListener('keydown', audioControl)
  audio.value.volume = counterStore.volume
})
onUnmounted(() => {
  window.removeEventListener('keydown', audioControl)
})

function switchTheme(newValue) {
  updateTheme(database, store, settingKey, playTheme, newValue)
  console.log('Setting')
}

const onTimeUpdate = () => {
  if (!audio.value) { return } 
  const currentTime = audio.value.currentTime
  for (const lyric of songLyrics.value) {
    if (currentTime >= lyric.time) {
      currentHighlight.value = lyric.time
    }
  }
} 

const inputRef = ref(null)
const coockieValue = ref(null)
async function searchEnter() {
  console.log(coockieValue.value)
  await setCookie(coockieValue.value)
  location.reload();
}
function onClick() {
  inputRef.value.focus()
}
</script>
<template>
  <div class="left-return" title="返回" @click="returnSearch"></div>
  <audio id="audio" class="audio" ref="audio" :src="songUrl" @timeupdate="onTimeUpdate" autoplay loop></audio>
  <div v-if="isVip" class="isVip" @click="onClick">
    <input class="cookie-input" placeholder="VIP Cookie" v-model="coockieValue" @keyup.enter="searchEnter" autofocus ref="inputRef"> 
  </div>
  <Theme1 v-else
    :songUrl="songUrl" 
    :songLyrics="songLyrics"
    :title="title"
    :artist="artist"
    :album="album"
    :cover="cover"
    :publishTime="publishTime"
    @switch="switchTheme"
    @return="returnSearch"
    :audio="audio"
    :currentHighlight="currentHighlight"
    v-if="playTheme == 1">
  </Theme1>
  
</template>
<style>
.left-return {
  position: fixed;
  height: 100%;
  width: 22px;
  cursor: pointer;
  z-index: 22;
}
.isVip {  
  z-index: 1;
  height: 100%;
  width: 100%;
  position: fixed;
  background-color: white;
}
body.dark .isVip {
  background-color: black;
}
body.dark .cookie-input {
  background-color: black;
}
.cookie-input {
  color: red;
  border: 1px solid;
  position: absolute;
  top: 50%;
  left: 50%;
  width: 99%;
  transform: translate(-50%, -50%);
  font-size: 7.7vw; 
  text-align: center;
  border-color: transparent;  
  font-family: 'SuperBlack', Arial, sans-serif;
}
.cookie-input:focus {
  outline: none;
  border: none;
}
</style>