<script setup>
import { reactive, ref, onMounted, onUnmounted } from 'vue'

import api from '../api'
import ReturnSong from '../components/ReturnSong.vue'

const props = defineProps({
  playlistid: [String, Number],
})

const playlist = ref([])
const loadCount = ref(7)
const ids = ref([])

api.getPlaylistDetails(props.playlistid)
  .then(value => {
    ids.value = value['playlist']['trackIds']
  })
  .catch(error => {
    console.error('Failed to get playlist details:', error)
  })

const updatePlaylist = () => {
  playlist.value = ids.value.slice(0, loadCount.value)
}
updatePlaylist()

onMounted(() => {
  const handleScroll = () => {
    const scrollPosition = window.innerHeight + window.scrollY
    const pageHeight = document.documentElement.scrollHeight

    if (scrollPosition >= pageHeight - 300) {
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
  loadCount.value += 7
  setTimeout(() => {
    if (loadCount.value < 1000) {
      if (document.body.offsetHeight - 207 <= window.innerHeight) {
        handleBottomReached()
      }
    }
  }, 77)
  updatePlaylist()
}

</script>

<template>
  <ReturnSong v-for="song in playlist" :key="song.id" :songid="song.id"></ReturnSong>
</template>
