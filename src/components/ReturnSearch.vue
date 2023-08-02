<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

import api from '../api'
import ReturnSong from './ReturnSong.vue'

const props = defineProps({
  q: [String, Number],
  autoFont: Boolean,
  blurCover: Boolean,
})

const offset = ref(0)
const songList = ref([])

const q = String(props.q)

let timeout = null

function updatePlaylist() {
  if (timeout !== null) {
    return
  }
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    timeout = null  
  }, 777)
  offset.value += 22
  api.searchDetails(q, 22, offset.value) 
    .then(value => {
      for (let s of value['result']['songs']) {
        const song = {
          id: s.id,
          title: s.name,
          artist: s.ar.map(item => item.name).join('/'),
          album: s.al.name,
          cover: s.al.picUrl,
          publishTime: s.publishTime
        }
        songList.value.push(song)
      }
    })
    .catch(error => {
      console.error('Failed to get search details:', error)
    })
}

onMounted(async () => {
  await api.searchDetails(q, 22, 0)
    .then(value => {
      for (let s of value['result']['songs']) {
        const song = {
          id: s.id,
          title: s.name,
          artist: s.ar.map(item => item.name).join('/'),
          album: s.al.name,
          cover: s.al.picUrl,
          publishTime: s.publishTime
        }
        songList.value.push(song)
      }
    })
    .catch(error => {
      console.error('Failed to get search details:', error)
    })
  
  const handleScroll = () => {
    const scrollPosition = window.innerHeight + window.scrollY
    const pageHeight = document.documentElement.scrollHeight

    if (scrollPosition >= pageHeight - 777) {
      handleBottomReached()
    }
  }
  
  if (document.body.offsetHeight <= window.innerHeight) {
    handleBottomReached()
  }

  window.addEventListener('wheel', handleScroll)
  onUnmounted(() => {
    window.removeEventListener('wheel', handleScroll)
  })
})

const handleBottomReached = () => {
  setTimeout(() => {
    if (offset.value < 100) {
      if (document.body.offsetHeight - 777 <= window.innerHeight) {
        handleBottomReached()
      }
    }
  }, 777)
  updatePlaylist()
}
</script>
<template>
  <ReturnSong 
    v-for="s in songList" 
    :key="s.id" 
    :songid="s.id" 
    :title="s.title"
    :artist="s.artist"
    :album="s.album"
    :cover="s.cover"
    :publishTime="s.publishTime"
    :autoFont="autoFont"
    :blurCover="blurCover">
  </ReturnSong>
</template>